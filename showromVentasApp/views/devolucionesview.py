import logging
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from adapters.sl_client import APIClient
from datosLsApp.models.regiondb import RegionDB
from datosLsApp.models.usuariodb import UsuarioDB
from logicaVentasApp.services.cotizacion import Cotizacion
import json
import requests
from requests.exceptions import RequestException
import urllib3

from logicaVentasApp.services.socionegocio import SocioNegocio
from logicaVentasApp.services.solicituddevolucion import SolicitudesDevolucion

# Desactivar las advertencias de SSL inseguro (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ReturnsView(View):

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            docEntry = kwargs.get('DocEntry')
            if docEntry:
                return self.quotate_items(request, docEntry)

            route_handler = self.get_route_map().get(request.path.rstrip('/'), None)
            if route_handler is None:
                return JsonResponse({'error': 'Ruta no válida'}, status=404)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in GET method: {str(e)}")
            return self.handle_error(e)
        
    def post(self, request, *args, **kwargs):
        try:
            path = request.path
            route_handler = self.post_route_map().get(path) or self.post_route_map().get(path.rstrip('/'))
            if route_handler is None:
                return JsonResponse({'error': 'Ruta no válida'}, status=404)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in POST method: {str(e)}")
            return self.handle_error(e)

    def get_route_map(self):
        return {
            '/': self.filtrarCotizaciones,
        }

    def post_route_map(self):
        return {
            '/ventas/listado_solicitudes_devolucion': self.filtrarCotizaciones,
        }
    
    def handle_invalid_route(self, request):
        return JsonResponse({'error': 'Ruta inválida'}, status=404)
    
    def handle_error(self, exception):
        if isinstance(exception, json.JSONDecodeError):
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        if isinstance(exception, RequestException):
            return JsonResponse({'error': 'Error de conexión con el servidor externo'}, status=503)
        logger.exception("Unexpected error")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)


    def get_endpoint(self):
        return 'ReturnRequest'

    def filtrarCotizaciones(self, request):
        """
        Maneja la solicitud para filtrar cotizaciones, delegando la lógica de construcción de filtros a una función separada.
        """        
        client = APIClient()

        try:
            data = json.loads(request.body)
            print(f"datos datos datos: {data}")
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Construir filtros usando la lógica de negocio
        filters = SolicitudesDevolucion.construirSolicitudesDevolucion(data)

        # Validar los parámetros de paginación
        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        # Manejar la solicitud de datos
        try:
            data = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip, filters=filters)
            print(f"datos datos datos: {data}")
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            