import logging
import os
from datetime import date, timedelta

import requests
from django.template.loader import render_to_string
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

from domain.exeptions.pdf_exceptions import (
    MiddlewareTimeoutError,
    MiddlewareConnectionError,
    MiddlewareHTTPError,
    ProductoNotFoundError,
)
from domain.services.calculador import CalculadoraTotales
from infrastructure.models.productodb import ProductoDB
from infrastructure.models.sucursaldb import SucursalDB
from infrastructure.models.usuariodb import UsuarioDB
from infrastructure.repositories.contactorepository import ContactoRepository
from infrastructure.repositories.direccionrepository import DireccionRepository
from infrastructure.repositories.socionegociorepository import SocioNegocioRepository

logger = logging.getLogger(__name__)
URL_MW = os.environ.get("URL_MW")


class CotizacionPDFService:

    def generar_pdf(self, data, base_url=None):
        codigoSn = data.get('rut')
        snrepo = SocioNegocioRepository()

        # Dirección
        id_direccion = data.get('direccion')
        address = ''
        if id_direccion and id_direccion != 'No hay direcciones disponibles':
            direcciones = DireccionRepository.obtenerDireccionesID(id_direccion)
            address = f"{direcciones.calleNumero}, {direcciones.comuna.nombre}"

        # Contacto
        contacto_id = data.get('contacto')
        contactos = ''
        if contacto_id and contacto_id != 'No hay contactos disponibles':
            contacto = ContactoRepository.obtenerContacto(contacto_id)
            contactos = contacto.nombreCompleto if contacto.nombre != "1" else ""

        sucursal = data.get('sucursal')
        datossocio = snrepo.obtenerPorCodigoSN2(codigoSn)
        detalle_sucursal = SucursalDB.objects.filter(codigo=sucursal).first()

        # Nombre cliente
        if datossocio.grupoSN.codigo == "105":
            name = f"{datossocio.nombre} {datossocio.apellido or ''}"
        else:
            name = datossocio.razonSocial

        usuarios = UsuarioDB.objects.get(vendedor__codigo=data.get('vendedor'))

        # Fechas
        fecha = data.get('fecha')
        validez = data.get('valido_hasta')

        if fecha:
            fecha = fecha.split("-")
            fecha = f"{fecha[2]}-{fecha[1]}-{fecha[0]}"

            validez = validez.split("-")
            validez = f"{validez[2]}-{validez[1]}-{validez[0]}"
        else:
            today = date.today()
            nueva_fecha = today + timedelta(days=9)
            fecha = f"{nueva_fecha.day}-{nueva_fecha.month}-{nueva_fecha.year}"

        # Productos
        productos = data.get('DocumentLines', [])
        for p in productos:
            descripcion = p.get("descripcion", "")
            if "(descontinuado)" in descripcion.lower():
                p["descripcion"] = descripcion.replace("(Descontinuado)", "(Últimas unidades)") \
                                              .replace("(descontinuado)", "(Últimas unidades)")

        from presentation.views.view import obtener_nombre_documento

        tipo_documento = obtener_nombre_documento(data.get('tipo_documento'))

        cotizacion = {
            "tipo_documento": tipo_documento,
            'numero': data.get('numero'),
            'fecha': fecha,
            'validez': validez,
            'totalNeto': data.get('totalNeto'),
            'iva': data.get('iva'),
            'totalbruto': data.get('totalbruto'),
            'observaciones': data.get('observaciones'),
            'vendedor': {
                'nombre': usuarios.nombre,
                'email': usuarios.email,
                'telefono': usuarios.telefono,
            },
            'cliente': {
                'rut': datossocio.rut,
                'nombre': name,
                'razonSocial': datossocio.razonSocial,
                'giro': datossocio.giro,
                'telefono': datossocio.telefono,
                'tipo': datossocio.grupoSN.codigo,
                'email': datossocio.email,
                'direccion': address,
                'contacto': contactos,
                'sucursal': detalle_sucursal.ubicacion,
            },
            'productos': productos,
            'descuento_por_producto': [
                int(item.get('porcentaje_descuento', 0))
                for item in productos
            ],
        }

        # Totales
        calculadora = CalculadoraTotales(data)
        lineas_neto = calculadora.calcular_linea_neto()

        for i, producto in enumerate(productos):
            producto["linea_neto"] = lineas_neto[i]

        cotizacion["productos"] = productos

        totales = calculadora.calcular_totales()

        # Priorizar los totales calculados en el frontend (productosInteraccion.js),
        # que son los que el usuario ve en pantalla. Llegan ya formateados ("$ 494.820").
        total_neto_front = (data.get('totalNeto') or '').strip()
        iva_front = (data.get('iva') or '').strip()
        total_descuento_front = (data.get('totalDescuento') or '').strip()
        total_bruto_front = (data.get('totalbruto') or '').strip()

        if total_neto_front:
            totales['total_valor_neto'] = total_neto_front
        if iva_front:
            totales['iva'] = iva_front
        if total_descuento_front:  # Total Bruto Con Dcto = Total a Pagar
            totales['total_valor_bruto'] = total_descuento_front
        if total_bruto_front:      # Total Bruto Sin Dcto
            totales['total_sin_descuento_bruto'] = total_bruto_front

        cotizacion["totales"] = totales
        cotizacion["tiene_descuento"] = any(cotizacion["descuento_por_producto"])

        # Template
        template = 'cotizacion_template.html' if data.get('pdf_button') == 2 else 'cotizacion_template2.html'
        html_string = render_to_string(template, {'cotizacion': cotizacion})

        pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

        return pdf_file, tipo_documento, cotizacion["numero"]



class FichaTecnicaPDFService:

    def generar_pdf(self, sku: str, base_url: str) -> bytes:
        """Comportamiento original — sin cambios."""
        producto, header_img = self._fetch_producto(sku)
        producto = self._transformar_producto(producto)
        return self._render_pdf(sku, producto, header_img, base_url)

    def generar_documento(self, sku: str, base_url: str):
        """
        Igual que generar_pdf pero devuelve el Document de WeasyPrint
        en lugar de bytes, para poder mergearlo con otros documentos.
        """
        producto, header_img = self._fetch_producto(sku)
        producto = self._transformar_producto(producto)
        return self._render_documento(sku, producto, header_img, base_url)

    # ── Pasos privados ──────────────────────────────────────────────────

    def _render_pdf(self, sku, producto, header_img, base_url) -> bytes:
        """Renderiza y escribe el PDF directamente a bytes."""
        font_config = FontConfiguration()
        return self._build_html(producto, header_img, base_url).write_pdf(
            font_config=font_config
        )

    def _render_documento(self, sku, producto, header_img, base_url):
        """Renderiza y devuelve el Document (sin escribir a bytes aún)."""
        font_config = FontConfiguration()
        return self._build_html(producto, header_img, base_url).render(
            font_config=font_config
        )

    def _build_html(self, producto, header_img, base_url) -> HTML:
        """Factoriza la construcción del objeto HTML de WeasyPrint."""

        print(f"producto: {producto}")
        html_string = render_to_string(
            "ficha_tecnica_template.html",
            {"producto": producto, "header_img": header_img},
        )
        return HTML(string=html_string, base_url=base_url)

    # ... _fetch_producto, _transformar_producto, _map_otros_colores sin cambios ...


    def _fetch_producto(self, sku: str) -> tuple[dict, str]:
        """Consulta el middleware y devuelve (producto, header_img)."""
        url = f"{URL_MW.strip().rstrip('/')}/{sku}"        
        print(f"URL: {url}")
        logger.info("Fetching product data: %s", url)

        try:
            api_response = requests.get(url, timeout=15)
            print(f"Response: {api_response}")
            api_response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.error("Timeout al consultar el middleware para SKU %s", sku)
            raise MiddlewareTimeoutError()
        except requests.exceptions.ConnectionError as e:
            logger.exception(
                "No se pudo conectar al middleware para SKU %s. Error: %s",
                sku,
                str(e)
            )
            raise MiddlewareConnectionError()
        except requests.exceptions.HTTPError as e:
            code = api_response.status_code
            logger.warning("HTTP %s para SKU %s: %s", code, sku, e)
            raise MiddlewareHTTPError(code)

        data = api_response.json()
        logger.debug("Data recibida del middleware para SKU %s: %s", sku, data)

        producto = data.get('producto')
        if not producto:
            logger.error("Respuesta sin 'producto' para SKU %s: %s", sku, data)
            raise ProductoNotFoundError(f"Sin campo 'producto' para SKU {sku}")

        return producto, data.get('header_img', '')
    

    def _transformar_producto(self, producto: dict) -> dict:
        """Enriquece y sanitiza el dict de producto."""
        producto['otros_colores'] = self._map_otros_colores(
            producto.get('otros_colores', [])
        )
        producto.setdefault('imagenes_thumb', [])
        producto.setdefault('ficha_tecnica', [])
        producto.setdefault('descripcion', '')
        producto.setdefault('color', '')
        return producto
    
    @staticmethod
    def _map_otros_colores(otros_colores_skus: list[str]) -> list[dict]:
        """Convierte lista de SKUs a lista de dicts {codigo, imagen}."""
        if not otros_colores_skus:
            return []

        productos = ProductoDB.objects.filter(
            codigo__in=otros_colores_skus
        ).values('codigo', 'imagen')

        productos_map = {p['codigo']: p['imagen'] for p in productos}

        return [
            {'codigo': sku, 'imagen': imagen}
            for sku in otros_colores_skus
            if (imagen := productos_map.get(sku))
        ]

