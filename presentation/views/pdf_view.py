import logging
import os
import traceback

import requests
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
URL_MW = os.environ.get("URL_MW")

from infrastructure.models.productodb import ProductoDB

logger = logging.getLogger(__name__)


def generate_ficha_tecnica_pdf(request, sku):
    """
    Genera la ficha técnica en PDF para un SKU dado.

    Mejoras respecto a la versión anterior:
    - Usa logger en lugar de print()
    - base_url apunta a STATIC_ROOT para que WeasyPrint resuelva
      recursos locales (fuentes, imágenes locales, etc.)
    - font_config pasado a write_pdf() para evitar warnings de fuentes
    - Manejo de errores más granular (timeout, conexión, datos)
    - Content-Disposition inline para previsualizar en el browser;
      usa 'attachment' si prefieres descarga directa.
    """

    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # ── 1. Fetch de datos desde el middleware ──────────────────────────
    url = f"{URL_MW}{sku}"
    logger.info("Fetching product data: %s", url)

    try:
        api_response = requests.get(url, timeout=15)
        api_response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Timeout al consultar el middleware para SKU %s", sku)
        return JsonResponse({'error': 'Timeout al obtener el producto'}, status=504)
    except requests.exceptions.ConnectionError:
        logger.error("No se pudo conectar al middleware para SKU %s", sku)
        return JsonResponse({'error': 'No se pudo conectar al middleware'}, status=502)
    except requests.exceptions.HTTPError as e:
        status = api_response.status_code
        logger.warning("HTTP %s para SKU %s: %s", status, sku, e)
        if status == 404:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        return JsonResponse({'error': f'Error del middleware: {status}'}, status=502)
    except Exception as e:
        logger.exception("Error inesperado fetching SKU %s", sku)
        return JsonResponse({'error': str(e)}, status=500)

    # ── 2. Validación de datos ─────────────────────────────────────────
    data = api_response.json()

    print("Data recibida del middleware para SKU", sku, ":", data)  # Debug log para ver la estructura de datos

    producto = data.get('producto')
    header_img = data.get('header_img', '')

    if not producto:
        logger.error("Respuesta sin 'producto' para SKU %s: %s", sku, data)
        return JsonResponse({'error': 'Data incompleta: falta "producto"'}, status=500)

    # ── 3. Transformaciones ────────────────────────────────────────────
    producto['otros_colores'] = _map_otros_colores(
        producto.get('otros_colores', [])
    )

    # Sanitizar campos opcionales para que el template no rompa con None
    producto.setdefault('imagenes_thumb', [])
    producto.setdefault('ficha_tecnica', [])
    producto.setdefault('descripcion', '')
    producto.setdefault('color', '')

    # ── 4. Render HTML ─────────────────────────────────────────────────
    try:
        html_string = render_to_string(
            'ficha_tecnica_template.html',
            {
                'producto': producto,
                'header_img': header_img,
            }
        )
    except Exception:
        logger.exception("Error al renderizar el template para SKU %s", sku)
        return JsonResponse({'error': 'Error al renderizar el template'}, status=500)

    # ── 5. Generar PDF ─────────────────────────────────────────────────
    #
    # base_url: apunta a la raíz estática del servidor para que WeasyPrint
    # resuelva URLs relativas (p.ej. fuentes locales, imágenes locales).
    # Si todas tus imágenes son URLs absolutas externas, puedes dejarlo
    # como request.build_absolute_uri('/').
    #
    # font_config: evita warnings de "FontConfiguration" en logs de WeasyPrint.
    #
    try:
        font_config = FontConfiguration()
        pdf_file = HTML(
            string=html_string,
            base_url=request.build_absolute_uri('/'),
        ).write_pdf(
            font_config=font_config,
            # presentational_hints=True  # descomenta si usas atributos HTML
            #                            # como align="center" en tablas legacy
        )
    except Exception:
        logger.exception("Error al generar el PDF para SKU %s", sku)
        return JsonResponse({'error': 'Error al generar el PDF'}, status=500)

    # ── 6. Response ────────────────────────────────────────────────────
    response = HttpResponse(pdf_file, content_type='application/pdf')
    # Cambia 'inline' a 'attachment' si quieres forzar la descarga
    response['Content-Disposition'] = (
        f'attachment; filename="ficha_tecnica_{sku}.pdf"'
    )
    return response


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _map_otros_colores(otros_colores_skus: list[str]) -> list[dict]:
    """
    Convierte una lista de SKUs a una lista de dicts {codigo, imagen}.
    Filtra entradas sin imagen para evitar <img src="None"> en el template.
    """

    print("Mapping otros_colores SKUs:", otros_colores_skus)
    
    if not otros_colores_skus:
        return []

    productos = ProductoDB.objects.filter(
        codigo__in=otros_colores_skus
    ).values('codigo', 'imagen')

    productos_map = {p['codigo']: p['imagen'] for p in productos}

    resultado = []
    for sku in otros_colores_skus:
        imagen = productos_map.get(sku)
        if imagen:  # omitir colores sin imagen para no romper el layout
            resultado.append({'codigo': sku, 'imagen': imagen})

    print("Mapped otros_colores:", resultado)
    
    return resultado