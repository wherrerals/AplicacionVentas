import logging
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from adapters.sl_client import APIClient
from logicaVentasApp.services.cotizacion import Cotizacion
import json
import requests
from requests.exceptions import RequestException
import urllib3

# Desactivar las advertencias de SSL inseguro (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class CotizacionView(View):
    
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
    
    def get_endpoint(self):
        return 'Quotations'
    
    def get_route_map(self):
        return {
            '/ventas/listado_Cotizaciones': self.listarCotizaciones,
            '/ventas/obtener_detalles_cotizacion': self.obtenerDetallesCotizacion,
        }

    def post_route_map(self):
        return {
            '/ventas/listado_Cotizaciones_filtrado': self.filtrarCotizaciones,
            '/ventas/crear_cotizacion': self.crearCotizacion,
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

    def listarCotizaciones(self, request):
        try:
            client = APIClient()
            top = int(request.GET.get('top', 20))
            skip = int(request.GET.get('skip', 0))
            data = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip)
            return JsonResponse(data, safe=False)
        except ValueError as e:
            logger.error(f"Invalid parameters: {str(e)}")
            return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Error listing quotations: {str(e)}")
            return self.handle_error(e)
        
    def filtrarCotizaciones(self, request):
        """
        Maneja la solicitud para filtrar cotizaciones, delegando la lógica de construcción de filtros a una función separada.
        """
        print("Request body:", request.body)  # Verifica el cuerpo de la solicitud JSON recibida
        
        client = APIClient()

        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Verifica los datos JSON recibidos
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Construir filtros usando la lógica de negocio
        filters = Cotizacion.construirFiltrosCotizaciones(data)

        # Validar los parámetros de paginación
        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        print("Applying filters:", filters)  # Verifica los filtros aplicados
        print("-" * 10)  
        print(filters)

        # Manejar la solicitud de datos
        try:
            data = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip, filters=filters)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            print("Error:", e)  # Verifica el error específico que está ocurriendo
            return JsonResponse({'error': str(e)}, status=500)


    """      
    def obtenerDetallesCotizacion(self, request, *args, **kwargs):
        docEntry = kwargs.get('docEntry')
        print("DocEntry:", docEntry)
        
        if not docEntry:
            return JsonResponse({'error': 'DocEntry no proporcionado'}, status=400)
        
        # Llamar al servicio de cotización
        lines_data, error = Cotizacion.buscarDocumentosCotizacion(docEntry)
        
        # Verificar si se encontró un error
        if error:
            return JsonResponse({'error': error}, status=404 if 'No se encontró' in error else 500)
        
        # Devolver los datos si no hay error
        #return JsonResponse({'DocumentLines': lines_data}, status=200)
        render (request, 'cotizacion.html', {'DocumentLines': lines_data}) 
        """
    
    def obtenerDetallesCotizacion(self, request, *args, **kwargs):
        docEntry = kwargs.get('docEntry')
        print("DocEntry:", docEntry)
        
        if not docEntry:
            return JsonResponse({'error': 'DocEntry no proporcionado'}, status=400) 
        
        # Llamar al servicio de cotización
        lines_data, error = Cotizacion.buscarDocumentosCotizacion(docEntry)

        print("*" * 10)
        print("Lines data:", lines_data)  # Verificar los datos de las líneas de documento
        
        # Verificar si se encontró un error
        if error:
            return render(request, 'error.html', {'error': error}, status=404 if 'No se encontró' in error else 500)
        
        print("*" * 10)
        print(lines_data)
        
        # Renderizar la página HTML con los datos
        #return JsonResponse({'DocumentLines': lines_data}, status=200)
        return render(request,'cotizacion.html', {'DocumentLines': lines_data})

    @csrf_exempt
    def crearCotizacion(self, request):
        print("probando")
        if request.method == 'POST':
            try:
                other = None
                data = json.loads(request.body)
                cotizacion = Cotizacion()
                creacion = cotizacion.crearDocumento(data)
                print("Creacion:", creacion)
                return JsonResponse(creacion, status=201)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'JSON inválido'}, status=400)
    
