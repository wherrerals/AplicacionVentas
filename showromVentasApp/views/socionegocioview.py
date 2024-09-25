from django.http import JsonResponse
from django.views.generic import View, FormView
from logicaVentasApp.services.socionegocio import SocioNegocio
from django.core.exceptions import ValidationError

class SocioNegocioView(FormView):

    def post(self, request):
        # Definir un diccionario de rutas a métodos POST
        route_map = {
            '/ventas/agregar_editar_clientes/': self.agregarSocioNegocio,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)
        if handler:
            return handler(request)
        return JsonResponse({'error': 'Invalid URL'}, status=404)
    
    def get(self, request):
        # Definir un diccionario de rutas a métodos GET
        route_map = {
            '/ventas/buscar_clientes/': self.busquedaSocioNegocio,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)
        if handler:
            return handler(request)
        return JsonResponse({'error': 'Invalid URL'}, status=404)

    def agregarSocioNegocio(self, request):
        try:
            # Obtener los datos del formulario
            datos = {
                'grupoSN': request.POST.get('grupoSN'),
                'rut': request.POST.get('rutSN'),
                'email': request.POST.get('emailSN'),
                'nombre': request.POST.get('nombreSN'),
                'apellido': request.POST.get('apellidoSN'),
                'razon_social': request.POST.get('grupoSN'),
                'giro': request.POST.get('giroSN'),
                'telefono': request.POST.get('telefonoSN')
            }

            socio_negocio = SocioNegocio(request)
            # Llamar al método y devolver directamente el JsonResponse generado
            response = socio_negocio.crearOActualizarCliente()
            return response
            print(f"Response: {response}")

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Error inesperado: {}'.format(str(e))}, status=500)

    def busquedaSocioNegocio(self, request):
        if request.method == "GET":
            numero = request.GET.get('numero')
            if numero:
                resultados_formateados = SocioNegocio.buscarSocioNegocio(numero)
                return JsonResponse({'resultadosClientes': resultados_formateados})
            return JsonResponse({'error': 'No se proporcionó un número válido'})
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    