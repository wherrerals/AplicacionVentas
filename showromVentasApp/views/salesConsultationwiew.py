import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Importing modules
from logicaVentasApp.context.user_context import UserContext
from logicaVentasApp.services.valitadionApp import ValitadionApp

logger = logging.getLogger(__name__)



class SalesConsultationView(View):

    # this method dispatches the request to the appropriate handler based on the HTTP method
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
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
        pass

    def get_route_map(self):

        return {
            '/ventas/consulta-ventas': self.sales_consultation,
        }
    
    def sales_consultation(self, request):

        authenticated_user = ValitadionApp.user_autentication(request)
        context = UserContext.user_context(authenticated_user, request)

        return render(request, 'salesConsultation.html', context)