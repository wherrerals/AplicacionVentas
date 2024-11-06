from django.http import JsonResponse
from django.views.generic import View, FormView
from adapters.sl_client import APIClient
from logicaVentasApp.services.socionegocio import SocioNegocio
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
import logging
import json


logger = logging.getLogger(__name__)

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
            '/ventas/informacion_cliente/': self.informacionCliente
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

    def informacionCliente(self, request):
        """
        Redirige a la página de creación de clientes, manteniendo el RUT en la URL.
        """
        if request.method != 'GET':
            return JsonResponse({'error': 'Método no permitido'}, status=405)

        rut = request.GET.get('rut')

        print("RUT: ", rut)
        if not rut:
            return JsonResponse({'error': 'No se proporcionó un RUT de socio de negocio'}, status=400)

        try:
            # Crear instancia del servicio y verificar si el cliente existe en el DB
            print("ruta: ", rut )
            print("Buscando información del cliente")

            socio_negocio_service = SocioNegocio(request)


            cardCode = rut + "C"

            print("CardCode: ", cardCode)


            sn_existe = socio_negocio_service.verificarSocioDB(cardCode)

            print("SN Existe: ", sn_existe)

            if sn_existe:

                resultados = socio_negocio_service.infoCliente(rut)

                if resultados:
                    return JsonResponse(resultados, status=200, safe=False)  # safe=False permite serializar objetos no 'dict'
                else:
                    return JsonResponse({'error': 'No se encontraron resultados para el RUT especificado'}, status=404)
                
            else:
                client = APIClient() 
                sn = SocioNegocio(request)
                data = client.getInfoSN(cardCode)
                conversion = sn.convertirJsonObjeto(data)
                dataCreacion = sn.procesarDatosSocionegocio(conversion) 
                creacion = sn.guardarClienteCompleto(dataCreacion)
                
                try:
                    if creacion:
                        resultados = socio_negocio_service.infoCliente(rut)
                        if resultados:
                            return JsonResponse(resultados, status=200, safe=False)
                        else:
                            return JsonResponse({'error': 'No se encontraron resultados para el RUT especificado'}, status=404)
                    else:
                        return JsonResponse({'error': 'Error al crear el cliente'}, status=500)
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  