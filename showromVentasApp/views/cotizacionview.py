import logging
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
    @method_decorator(login_required)
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
            '/ventas/crear_cotizacion': self.crearDocumento,
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
        print("Request body:", request.body)  # Verifica el cuerpo de la solicitud JSON recibida
        
        client = APIClient()

        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Verifica los datos JSON recibidos
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        filters = {}

        # Agregar filtros solo si se proporcionan datos válidos
        if data.get('fecha_inicio'):
            filters['Quotations/DocDate ge'] = f"'{data.get('fecha_inicio')}')"
        if data.get('fecha_fin'):
            filters['Quotations/DocDate le'] = f"'{data.get('fecha_fin')}')"
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Quotations/DocNum,'] = f"{docum})"
        if data.get('carCode'):
            filters['contains(Quotations/CardCode,'] = f"'{data.get('carCode')}'"
        if data.get('cardNAme'):
            filters['contains(Quotations/CardName,'] = f"'{data.get('cardNAme')}')"
        if data.get('salesEmployeeName'):
            filters['contains(SalesPersons/SalesEmployeeName,'] = f"'{data.get('salesEmployeeName')}'"
        if data.get('DocumentStatus'):
            filters['Quotations/DocumentStatus eq'] = f"'{data.get('DocumentStatus')}'"
        if data.get('docTotal'):
            filters['contains(Quotations/DocTotal,'] = data.get('docTotal')
        if data.get('cancelled'):
            filters['Quotations/Cancelled eq'] = f"'{data.get('cancelled')}'"

        # Limpiar los filtros vacíos o con valores inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        print("Applying filters:", filters)# Verifica los filtros aplicados
        print("-" * 10)  
        print(filters)
        

        try:
            data = client.getData(top=top, skip=skip, filters=filters)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            print("Error:", e)  # Verifica el error específico que está ocurriendo
            return JsonResponse({'error': str(e)}, status=500)

    def obtenerDetallesCotizacion(self, request, docEntry):
        try:
            client = APIClient()
            doc_num_int = int(docEntry)
            all_quotations = Cotizacion.obtenerCotizaciones(client, docEntry)
            found_quotation = next((q for q in all_quotations if q.get('docEntry') == doc_num_int), None)

            if not found_quotation:
                logger.warning(f"No se encontró la cotización con DocEntry: {docEntry}")
                return JsonResponse({'error': 'No se encontró la cotización especificada'}, status=404)

            document_lines = found_quotation.get('DocumentLines', [])
            lines_data = Cotizacion.prepararLineasItemas(document_lines)
            return JsonResponse({'DocumentLines': lines_data}, status=200)
        except ValueError as e:
            logger.error(f"Error de valor: {str(e)}")
            return JsonResponse({'error': 'DocEntry inválido'}, status=400)
        except Exception as e:
            logger.error(f"Error al obtener detalles de cotización: {str(e)}")
            return self.handle_error(e)

    def quotate_items(self, request, docNum):
        try:
            client = APIClient()
            data = client.get_quotations_items('Quotations')
            if 'value' not in data:
                logger.warning("No se encontraron datos de cotizaciones")
                return JsonResponse({'error': 'No se encontraron datos de cotizaciones'}, status=404)

            quotations = data['value']
            doc_num_int = int(docNum)
            found_quotation = next((q for q in quotations if q.get('DocNum') == doc_num_int), None)

            if not found_quotation:
                logger.warning(f"No se encontró la cotización con DocNum: {docNum}")
                return JsonResponse({'error': 'No se encontró la cotización especificada'}, status=404)

            document_lines = found_quotation.get('DocumentLines', [])
            lines_data = Cotizacion.prepararLineasItemas(document_lines)
            return JsonResponse({'DocumentLines': lines_data}, status=200)
        except ValueError as e:
            logger.error(f"Error de valor: {str(e)}")
            return JsonResponse({'error': 'DocNum inválido'}, status=400)
        except Exception as e:
            logger.error(f"Error al cotizar items: {str(e)}")
            return self.handle_error(e)

    def crearDocumento(self, request):
        try:
            data = json.loads(request.body)
            cotizacion = Cotizacion()
            result = cotizacion.crearDocumento(data, self.get_endpoint())
            return JsonResponse(result, safe=False)
        except json.JSONDecodeError as e:
            logger.error(f"JSON inválido: {str(e)}")
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Error al crear documento: {str(e)}")
            return self.handle_error(e)