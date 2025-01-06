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
            '/ventas/filtrar_socios_negocio/': self.filtrarSociosNegocio,
            '/ventas/listado_socios_negocio/': self.listarSociosNegocio,

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
            '/ventas/listado_socios_negocio/': self.listarSociosNegocio,
            '/ventas/verificar_cliente/': self.verificarSapSocio,
            '/ventas/informacion_cliente/': self.informacionCliente,
        }

        # Buscar el método basado en la ruta 
        handler = route_map.get(request.path)
        if handler:
            return handler(request)
        return JsonResponse({'error': 'Invalid URL'}, status=404)



    def agregarSN(self, request):

        if request.method == 'POST':
            

            pass

    def agregarSocioNegocio(self, request):
        
        if request.method == 'POST':

            try:
                socioNegoService = SocioNegocio(request)

                response = socioNegoService.crearOActualizarCliente()

                response_data = json.loads(response.content)

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
                    return JsonResponse(
                        {
                            'success': False,
                            'message': response_data.get('message', 'Error al crear o actualizar el cliente'),
                            'details': response_data.get('details', 'Detalles no disponibles')  # Si hay más detalles
                        },
                        status=400
                    )

            except ValidationError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

            except KeyError as e:
                return JsonResponse({'success': False, 'error': f"Falta el campo requerido: {str(e)}"}, status=400)

            except Exception as e:
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
                    # Limpiar la "C" al final del número si existe
                    numero = numero.rstrip('C')
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
        Método para obtener la información de un cliente
        
        args:
            request: HttpRequest
        
        return:
            JsonResponse con la información del cliente, o un mensaje de error
        """

        if request.method != 'GET':
            return JsonResponse({'error': 'Método no permitido'}, status=405)
        
        rut = request.GET.get('rut')
        print("RUT:", rut)

        if not rut:
            return JsonResponse({'error': 'No se proporcionó un RUT de socio de negocio'}, status=400)
        try:

            socio_negocio_service = SocioNegocio(request)

            print("obtener info cliente")
            cardCode = socio_negocio_service.generarCardCode(rut)

            print("CardCode:", cardCode)

            if socio_negocio_service.verificarSocioDB(cardCode):
                return socio_negocio_service.responderInfoCliente(rut)
            else:
                return socio_negocio_service.crearYresponderCliente(cardCode, rut)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

    def listarSociosNegocio(self, request):
        try:
            client = APIClient()
            top = int(request.GET.get('top', 20))
            skip = int(request.GET.get('skip', 0))
            data = client.getDataSN(top=top, skip=skip)
            return JsonResponse(data, safe=False)
        except ValueError as e:
            logger.error(f"Invalid parameters: {str(e)}")
            return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Error listing quotations: {str(e)}")
            return self.handle_error(e)

    def filtrarSociosNegocio(self, request):
        """
        Método para filtrar los socios de negocio
        
        args:
            request: HttpRequest
            
            return:
                JsonResponse con los datos de los socios de negocio, o un mensaje de error
        """
        print("Request body:", request.body)  # Verifica el cuerpo de la solicitud JSON recibida
        
        client = APIClient()

        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Verifica los datos JSON recibidos
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Construir filtros usando la lógica de negocio
        filters = SocioNegocio.construirFiltrosSociosNegocio(data)

        # Validar los parámetros de paginación
        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        print("Applying filters:", filters)  # Verifica los filtros aplicados
        print("-" * 10)  
        print(filters)

        # Manejar la solicitud de datos
        try:
            data = client.getDataSN(top=top, skip=skip, filters=filters)
            return JsonResponse(data, safe=False)
        except Exception as e:
            print("Error:", e)  # Verifica el error específico que está ocurriendo
            return JsonResponse({'error': str(e)}, status=500)


