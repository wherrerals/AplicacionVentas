from django.http import JsonResponse
from django.views.generic import View
from adapters.sl_client import APIClient

class Productos(View):

    def get(self, request):
        # Definir un diccionario de rutas a métodos
        route_map = {
            '/listado_productos/': self.listadoProductos,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)

        if handler:
            return handler(request)
        else:
            return JsonResponse({'error': 'Invalid URL'}, status=404)
    
    def listadoProductos(self, request):
        client = APIClient()

        try:
            data = client.getData(endpoint='Quotations')
            return JsonResponse(data, safe=False)
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)


