import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

# Importing modules
from adapters.sl_client import APIClient
from logicaVentasApp.context.user_context import UserContext
from logicaVentasApp.services.cotizacion import Cotizacion
from logicaVentasApp.services.valitadionApp import ValitadionApp

logger = logging.getLogger(__name__)


class SalesConsultationView(View):

    # this method dispatches the request to the appropriate handler based on the HTTP method
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def __init__(self):
        self.api_get_way_sl = APIClient() # Initialize the API client
    
    def get(self, request, *args, **kwargs):
        try:
            route_handler = self.get_route_map().get(request.path.rstrip('/'), None)
        
            if route_handler is None:
                return JsonResponse({'error': 'Ruta no válida'}, status=404)
            
            return route_handler(request, *args, **kwargs)
        
        except Exception as e:
            logger.error(f"Error in GET method: {str(e)}")
            return JsonResponse({'error': 'Ocurrió un error en el servidor'}, status=500)

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

    def post_route_map(self):
        return {
            '/ventas/obtener-ventas': self.get_sales_view,
        }

    def get_route_map(self):

        return {
            '/ventas/consulta-ventas': self.sales_consultation,
            '/ventas/lista-ventas': self.sales_list_view,
        }
    
    def sales_consultation(self, request):

        authenticated_user = ValitadionApp.user_autentication(request)
        context = UserContext.user_context(authenticated_user, request)

        return render(request, 'salesConsultation.html', context)
    
    def sales_list_view(self, request):

        authenticated_user = ValitadionApp.user_autentication(request)
        context = UserContext.user_context(authenticated_user, request)

        return render(request, 'list_sales_global.html', context)

    def get_sales_view(self, request):

        print("get_sales_view")

        type_sales = request.get('typeSales')
    
        build_filters = Cotizacion.build_query_filters(request, type_sales)
        get_sales = self.api_get_way_sl.get_sales_sl(build_filters, type_sales)

        print(f"get_sales {get_sales}")
