import json
from adapters.sl_client import APIClient
from logicaVentasApp.services.filters import FilterPreparer
from showromVentasApp.views.documentsView import DocumentsView

import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ReturnsView(DocumentsView):

    def get_route_map(self):
        return {
            '/': self.filter_documents,
        }

    def post_route_map(self):
        return {
            '/ventas/listado_solicitudes_devolucion': self.filter_documents,
        }
    
    def get_endpoint(self):
        return 'ReturnRequest'

    def filter_documents(self, request):

        # Conexion con la API de SAP
        contection_service_layer = APIClient()

        try:
            # Obtener los parámetros de la petición
            data = json.loads(request.body)

        except json.JSONDecodeError as e:
            logger.error(f"Error in JSON decode: {str(e)}")
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        

        apply_filters = FilterPreparer.add_filter(data, self.get_endpoint())

        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))

        except ValueError:
            logger.error(f"Error in top/skip values: {str(e)}")
            return JsonResponse({'error': 'Valores inválidos para top/skip'}, status=400)

        try:
            data = contection_service_layer.getData(endpoint=self.get_endpoint(), top=top, skip=skip, filters=apply_filters)
            return JsonResponse(data, safe=False)
        except Exception as e:
            logger.error(f"Error in filter_documents: {str(e)}")
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
            