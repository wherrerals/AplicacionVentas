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
        if request.method == 'POST':

            print("Agregando Socio de Negocio")
            print(f"Request: {request.POST}")

            try:
                request.POST = request.POST.copy()

                # Crear instancia del socio de negocio y llamar al servicio
                socioNegoService = SocioNegocio(request)

                # Llamar al servicio para crear o actualizar el cliente
                response = socioNegoService.crearOActualizarCliente()

                print(f"Respuesta de crear o actualizar Cliente: {response.content}")

                # Si la respuesta es un JsonResponse, obtenemos su contenido
                response_data = json.loads(response.content)

                # Manejar la respuesta según el valor de 'success'
                if response_data.get('success'):
                    return JsonResponse(
                        {
                            'success': True,
                            'message': response_data.get('message', 'Cliente creado o actualizado con éxito'),
                            'codigoSN': response_data.get('codigoSN')  # Este campo es opcional
                        },
                        status=201
                    )

                else:
                    # Si 'success' es False, enviamos un mensaje de error
                    return JsonResponse(
                        {
                            'success': False,
                            'message': response_data.get('message', 'Error al crear o actualizar el cliente'),
                            'details': response_data.get('details', 'Detalles no disponibles')  # Si hay más detalles
                        },
                        status=400
                    )

            except ValidationError as e:
                # Error de validación, retornamos un mensaje claro
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

            except KeyError as e:
                # Error por campo faltante en la solicitud
                return JsonResponse({'success': False, 'error': f"Falta el campo requerido: {str(e)}"}, status=400)

            except Exception as e:
                # Error inesperado, se loguea y se informa al usuario de forma genérica
                print(f"Error inesperado: {str(e)}")
                return JsonResponse({'success': False, 'error': 'Error inesperado, contacte con soporte'}, status=500)





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



