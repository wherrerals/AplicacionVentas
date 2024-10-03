from django.http import JsonResponse
from django.views.generic import View, FormView
from logicaVentasApp.services.socionegocio import SocioNegocio
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json


class SocioNegocioView(FormView):

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        # Definir un diccionario de rutas a métodos POST
        route_map = {
            '/ventas/agregar_editar_clientes/': self.agregarSocioNegocio,
            '/ventas/crear_cliente/': self.creacionCionSocioNeocio,
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
            '/ventas/verificar_cliente/': self.verificarSapSocio,
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
    
        
    def verificarSapSocio(self, request):

        print("Verificando Socio de Negocio")

        if request.method == "GET":
            cardCode = request.GET.get('data-rut')  # Usar en producción
            #cardCode = "10880683C"     
            # Valor por defecto para pruebas

            if cardCode:
                socio_existe = SocioNegocio.verificarSocioNegocioSap(cardCode) 


                if socio_existe == True:
                    return JsonResponse({"success": True, "message": "Socio de negocio encontrado."})
                else:
                    return JsonResponse({"success": False, "message": "Socio de negocio no encontrado."})
            
            return JsonResponse({"success": False, "message": "Código de socio no proporcionado."}, status=400)
        
        return JsonResponse({"error": "Método no permitido."}, status=405)

    @csrf_exempt
    def creacionCionSocioNeocio(self, request):
        print("probando Creacion")
        if request.method == 'POST':
            try:
                other = None
                data = json.loads(request.body)
                socio_negocio = SocioNegocio(request)
                creacion = socio_negocio.creacionSocioSAP(data)
                print("Creacion:", creacion)
                return JsonResponse(creacion, status=201)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'JSON inválido'}, status=400)

