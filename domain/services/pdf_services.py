# services/pdf/cotizacion_pdf_service.py

import json
from datetime import date, timedelta
from django.template.loader import render_to_string
from domain.services.calculador import CalculadoraTotales
from infrastructure.models.sucursaldb import SucursalDB
from infrastructure.models.usuariodb import UsuarioDB
from infrastructure.repositories.contactorepository import ContactoRepository
from infrastructure.repositories.direccionrepository import DireccionRepository
from infrastructure.repositories.socionegociorepository import SocioNegocioRepository
from presentation.views.view import obtener_nombre_documento
from weasyprint import HTML

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
        cotizacion["totales"] = calculadora.calcular_totales()
        cotizacion["tiene_descuento"] = any(cotizacion["descuento_por_producto"])

        # Template
        template = 'cotizacion_template.html' if data.get('pdf_button') == 2 else 'cotizacion_template2.html'
        html_string = render_to_string(template, {'cotizacion': cotizacion})

        pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

        return pdf_file, tipo_documento, cotizacion["numero"]