from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from adapters.sl_client import APIClient
from abc import ABC, abstractmethod
import requests
import re
import json
import logging

logger = logging.getLogger(__name__)

class Documento(View, ABC):
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            route_handler = self.get_route_map().get(request.path, self.handle_invalid_route)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in GET method: {str(e)}")
            return self.handle_error(e)

    def post(self, request, *args, **kwargs):
        try:
            route_handler = self.get_route_map().get(request.path, self.handle_invalid_route)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in POST method: {str(e)}")
            return self.handle_error(e)

    @abstractmethod
    def get_route_map(self):
        """
        Define el mapa de rutas para la clase.
        Debe ser implementado por las clases hijas.
        """
        pass

    def handle_invalid_route(self, request):
        return JsonResponse({'error': 'Ruta inválida'}, status=404)

    def handle_error(self, exception):
        if isinstance(exception, json.JSONDecodeError):
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        # Agrega más manejo de errores específicos aquí
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def validate_required_fields(self, data, required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")

    def crear(self, request):
        client = APIClient()
        try:
            data = json.loads(request.body)
            self.validate_required_fields(data, self.get_required_fields())
            json_data = self.prepare_json_data(data)
            endpoint = self.get_endpoint()
            headers = {"Content-Type": "application/json"}
            result = client.post_data(endpoint, data=json_data, headers=headers)
            return JsonResponse(result, safe=False)
        except Exception as e:
            logger.error(f"Error en crear: {str(e)}")
            return self.handle_error(e)

    @abstractmethod
    def get_required_fields(self):
        """
        Define los campos requeridos para crear un documento.
        Debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def prepare_json_data(self, data):
        """
        Prepara los datos JSON para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def get_endpoint(self):
        """
        Define el endpoint para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass