from django.http import JsonResponse
from django.views.generic import View
from logicaVentasApp.services.socionegocioservice import SocioNegocioService
from django.core.exceptions import ValidationError

class SocioNegocio(View):

    def post(self, request):
        route_map = {
            '/ventas/agregar_editar_clientes/': self.agregarSocioNegocio,
        }

        handler = route_map.get(request.path)
        if handler:
            return handler(request)
        return JsonResponse({'error': 'Invalid URL'}, status=404)

    def agregarSocioNegocio(self, request):
        try:
            SocioNegocioService.crear_o_actualizar_cliente(request)
            return JsonResponse({'success': 'Cliente creado exitosamente'})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
