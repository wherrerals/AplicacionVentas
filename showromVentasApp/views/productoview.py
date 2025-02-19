from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json

from datosLsApp.repositories.productorepository import ProductoRepository

class Productos(View):

    @method_decorator(csrf_exempt)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Definir un diccionario de rutas a métodos
        route_map = {
            '/ventas/pendiente/': self.prueba,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)
        if handler:
            return handler(request)
        return JsonResponse({'error': 'Invalid URL'}, status=404)

    def post(self, request):
        # Definir un diccionario de rutas a métodos
        route_map = {
            '/ventas/productos/': self.listado_productos,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)
        if handler:
            return handler(request)
        return JsonResponse({'error': 'Invalid URL'}, status=404)

    def listado_productos(self, request):
        print('listado_productos')

        try:
            data = json.loads(request.body)
            filters = data.get('filters', {})
            page = data.get('page', 1)
            limit = data.get('top', 20)
            offset = (page - 1) * limit

            # Primero obtener el total de registros sin paginación
            total_records = ProductoRepository.obtener_total_productos(
                filtro_nombre=filters.get('nombre', None),
                filtro_codigo=filters.get('codigo', None)
            )

            # Luego obtener los productos paginados
            productos = ProductoRepository.obtener_productos(
                filtro_nombre=filters.get('nombre', None),
                filtro_codigo=filters.get('codigo', None),
                offset=offset,
                limite=limit
            )

            return JsonResponse({
                "data": {
                    "value": productos,
                },
                "totalRecords": total_records,  # Usar el total real de registros
                "page": page,
                "limit": limit
            }, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    
    def prueba(self, request):
        pass