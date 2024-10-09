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
        """
        Sobreescribir el método `dispatch` para manejar las rutas GET y POST
        
        args:
            request: HttpRequest
            args: tuple
            kwargs: dict
        
        return: 
            HttpResponse
        """
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Método POST para manejar las rutas de la API

        args:
            request: HttpRequest

        return:
            JsonResponse con la respuesta de la API
        """

        # Definir un diccionario de rutas a métodos POST
        route_map = {
            '/ventas/agregar_editar_clientes/': self.agregarSocioNegocio,
            #'/ventas/crear_cliente/': self.creacionCionSocioNeocio,
        }

        # Buscar el método basado en la ruta
        handler = route_map.get(request.path)
        if handler:
            return handler(request)
        return JsonResponse({'error': 'Invalid URL'}, status=404)
    
    def get(self, request):
        """
        Método GET para manejar las rutas de la API

        args:
            request: HttpRequest

        return:
            JsonResponse con la respuesta de la API
        """
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
            # Recolectar datos del formulario y pasarlos al service
            datos = {
                'grupoSN': request.POST.get('grupoSN'),
                'rut': request.POST.get('rutSN'),
                'email': request.POST.get('emailSN'),
                'nombre': request.POST.get('nombreSN'),
                'apellido': request.POST.get('apellidoSN'),
                'razon_social': request.POST.get('razonSN'),
                'giro': request.POST.get('giroSN'),
                'telefono': request.POST.get('telefonoSN')
            }
            
            # Crear instancia del socio de negocio y llamar al servicio
            socio_negocio_service = SocioNegocio(request)
            response = socio_negocio_service.crearOActualizarCliente()

            # Manejar la respuesta del service
            if response.get('success'):
                return JsonResponse({'success': True, 'message': 'Cliente creado o actualizado con éxito', 'codigoSN': response.get('codigoSN')}, status=201)
            else:
                return JsonResponse({'success': False, 'message': response.get('error')}, status=400)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
            
        except Exception as e:
            # Loggear el error para depuración
            print(f"Error inesperado: {str(e)}")
            return JsonResponse({'error': 'Error inesperado: {}'.format(str(e))}, status=500)



    """     
    @csrf_exempt  # No recomendado para producción. Preferir csrf_protect
    def creacionCionSocioNeocio(self, request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'JSON inválido'}, status=400)

            # Verificar si 'CardCode' está presente en el JSON
            carcode = data.get('CardCode')
            if not carcode:
                return JsonResponse({'error': 'Falta el campo CardCode'}, status=400)

            # Crear el socio_negocio y verificar si ya existe
            socio_negocio = SocioNegocio(request)
            verificacion = socio_negocio.verificarSocioNegocioSap(carcode)
            if verificacion:
                return JsonResponse({'error': 'Socio de negocio ya existe'}, status=409)  # 409 Conflict

            # Crear el socio de negocio
            creacion = socio_negocio.creacionSocioSAP(data)
            return JsonResponse(creacion, status=201)

        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Manejo de métodos no permitidos 
        """


            
    def busquedaSocioNegocio(self, request):
        """
        Método para buscar un socio de negocio
        
        args: 
            request: HttpRequest

        return:
            JsonResponse con la respuesta de la base de datos
        """
        if request.method == "GET":
            nombre = request.GET.get('nombre')
            numero = request.GET.get('numero')

            if numero or nombre:
                resultados = []

                # Búsqueda por número (rut)
                if numero:
                    resultados_por_numero = SocioNegocio.buscarSocioNegocio(numero)
                    resultados.extend(resultados_por_numero)

                # Búsqueda por nombre
                if nombre:
                    resultados_por_nombre = SocioNegocio.buscarSocioNegocio(nombre, buscar_por_nombre=True)
                    resultados.extend(resultados_por_nombre)

                if resultados:
                    return JsonResponse({'resultadosClientes': resultados})
                else:
                    return JsonResponse({'error': 'No se encontraron resultados para los criterios proporcionados'})

            return JsonResponse({'error': 'No se proporcionó un número o nombre válido'})

        return JsonResponse({'error': 'Método no permitido'}, status=405)


    
        
    def verificarSapSocio(self, request):
        """
        Método para verificar si un socio de negocio existe en SAP

        args:
            request: HttpRequest

        return:
            JsonResponse con la respuesta de la API
        """

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



