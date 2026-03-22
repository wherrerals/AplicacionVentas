import requests
import logging
from django.utils import timezone

from infrastructure.models.productodb import ProductoDB
from presentation.views.pdf_view import URL_MW

logger = logging.getLogger(__name__)

DEFAULT_IMAGE_URL = "https://ledstudiocl.vtexassets.com/assets/vtex.file-manager-graphql/images/14ecba9f-2814-4029-9e0e-e5e6b9e2869c___b2a5497dbc81c0adc5576c48b2eeb27b.jpg"

REQUEST_TIMEOUT = 5


def _is_out_of_time():
    now = timezone.localtime()
    return now.hour >= 6


def procesar_chunk(codigos):

    productos = {
        p.codigo: p.imagen
        for p in ProductoDB.objects.filter(codigo__in=codigos)
        .exclude(imagen=DEFAULT_IMAGE_URL)
        .only("codigo", "imagen")
    }

    updates_status = []
    updates_image = []

    for idx, (codigo, url) in enumerate(productos.items(), start=1):

        if _is_out_of_time():
            logger.warning("Corte de chunk por horario")
            break

        status_code = _validar_url(url)

        if status_code != 200:
            nueva_url = _get_new_image_url(codigo)

            if nueva_url and nueva_url != DEFAULT_IMAGE_URL:
                updates_image.append((codigo, nueva_url))

        updates_status.append((codigo, str(status_code)))

        if idx % 20 == 0:
            logger.info(f"Procesados {idx}/{len(productos)} en chunk")

    _bulk_update_status(updates_status)
    _bulk_update_images(updates_image)

def _validar_url(url):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT, stream=True)
        return response.status_code
    except requests.RequestException:
        return "error"
    
def _get_new_image_url(codigo):
    try:
        response = requests.get(f"{URL_MW}{codigo}", timeout=3)
        response.raise_for_status()

        data = response.json()
        return data.get("producto", {}).get("imagen_principal")

    except requests.RequestException:
        logger.error(f"Error obteniendo imagen para {codigo}")
        return None

def _bulk_update_status(updates):
    for codigo, status in updates:
        ProductoDB.objects.filter(codigo=codigo).update(
            imagenStatusHttp=status
        )


def _bulk_update_images(updates):
    for codigo, url in updates:
        ProductoDB.objects.filter(codigo=codigo).update(
            imagen=url
        )