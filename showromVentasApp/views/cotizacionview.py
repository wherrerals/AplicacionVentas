import logging
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from adapters.sl_client import APIClient
from datosLsApp.models.regiondb import RegionDB
from datosLsApp.models.usuariodb import UsuarioDB
from logicaVentasApp.services.cotizacion import Cotizacion
import json
import requests
from requests.exceptions import RequestException
import urllib3

from logicaVentasApp.services.socionegocio import SocioNegocio

# Desactivar las advertencias de SSL inseguro (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class CotizacionView(View):
    
    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            docEntry = kwargs.get('DocEntry')
            if docEntry:
                return self.quotate_items(request, docEntry)

            route_handler = self.get_route_map().get(request.path.rstrip('/'), None)
            if route_handler is None:
                return JsonResponse({'error': 'Ruta no válida'}, status=404)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in GET method: {str(e)}")
            return self.handle_error(e)
        
    def post(self, request, *args, **kwargs):
        try:
            path = request.path
            route_handler = self.post_route_map().get(path) or self.post_route_map().get(path.rstrip('/'))
            if route_handler is None:
                return JsonResponse({'error': 'Ruta no válida'}, status=404)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in POST method: {str(e)}")
            return self.handle_error(e)
    
    def get_endpoint(self):
        return 'Quotations'
    
    def get_route_map(self):
        return {
            '/ventas/listado_Cotizaciones': self.listarCotizaciones, # Listado de cotizaciones, no es necesaria se deja para ver si es usada en otra parte del codigo. 
            '/ventas/detalles_cotizacion': self.detallesCotizacion,
            '/ventas/duplicar_cotizacion': self.duplicarCotizacion,
            '/ventas/copiar_a_odv': self.copiarAODV,
        }

    def post_route_map(self):
        
        return {
            '/ventas/listado_Cotizaciones_filtrado': self.filtrarCotizaciones,
            '/ventas/crear_cotizacion': self.crearOActualizarCotizacion,
            '/ventas/cambiar_estado_cotizacion': self.actualizarEstadosCotizacion,
        }

    def handle_invalid_route(self, request):
        return JsonResponse({'error': 'Ruta inválida'}, status=404)
    
    def handle_error(self, exception):
        if isinstance(exception, json.JSONDecodeError):
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        if isinstance(exception, RequestException):
            return JsonResponse({'error': 'Error de conexión con el servidor externo'}, status=503)
        logger.exception("Unexpected error")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

    def listarCotizaciones(self, request):
        try:
            client = APIClient()
            top = int(request.GET.get('top', 20))
            skip = int(request.GET.get('skip', 0))
            data = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip)
            return JsonResponse(data, safe=False)
        except ValueError as e:
            logger.error(f"Invalid parameters: {str(e)}")
            return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Error listing quotations: {str(e)}")
            return self.handle_error(e)
        
    def filtrarCotizaciones(self, request):
        """
        Maneja la solicitud para filtrar cotizaciones, delegando la lógica de construcción de filtros a una función separada.
        """        
        client = APIClient()

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Construir filtros usando la lógica de negocio
        filters = Cotizacion.construirFiltrosCotizaciones(data)

        # Validar los parámetros de paginación
        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        # Manejar la solicitud de datos
        try:
            data = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip, filters=filters)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @csrf_exempt
    def crearOActualizarCotizacion(self, request):
        try:
            data = json.loads(request.body)
            users_data = self.user_data(request)
            docEntry = data.get('DocEntry')
            docnum = data.get('DocNum')
            cotizacion = Cotizacion()

            if docEntry:
                if self.validar_vendedor(users_data['vendedor'], data['SalesPersonCode']) == True:
                    actualizacion = cotizacion.actualizarDocumento(docnum, docEntry, data)
                    return JsonResponse(actualizacion, status=200)
        
                else:
                    #actualizar el SalesPersonCode
                    data['SalesPersonCode'] = users_data['vendedor']
                    creacion = cotizacion.crearDocumento(data)
                    return JsonResponse(creacion, status=201)
            else:
                creacion = cotizacion.crearDocumento(data)
                return JsonResponse(creacion, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)
        
    def user_data(self, request):
        user = request.user

        codigoVendedor = UsuarioDB.objects.get(usuarios=user).vendedor.codigo

        return {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'vendedor': codigoVendedor
        }
    
    def validar_vendedor(self, vendedor1, vendedor2):
        if vendedor1 == vendedor2:
            return True
        else:
            return False

        

    def actualizarEstadosCotizacion(self, request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                docNum = data.get('DocNum')
                estado = data.get('Estado')
                if docNum is None or estado is None:
                    return JsonResponse({'error': 'Faltan parámetros'}, status=400)
                cotizacion = Cotizacion()
                cambio = cotizacion.actualizarEstadoDocumento(docNum, estado)
                return JsonResponse(cambio, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    def detallesCotizacion(self, request):
        # Obtener el parámetro 'docentry' de la solicitud
        docentry = request.GET.get('docentry')
        client = APIClient()

        # Llamar al método para obtener los detalles del cliente
        documentClient = client.detalleCotizacionCliente(docentry)

        if documentClient.get("odata.metadata") == "$metadata#Collection(Edm.ComplexType)" and not documentClient.get("value"):
            documentClient = client.detalleCotizacionCliente2(docentry)

        documentLine = client.detalleCotizacionLineas(docentry)

        # Extraer los datos de la clave 'value', asegurándose de manejar la estructura correctamente
        quotations_data = documentClient.get('value', [{}])[0].get('Quotations', {})
        cardCode = quotations_data.get('CardCode')
        rut = quotations_data.get('FederalTaxID')

        sn = SocioNegocio(request)
        
        # Preparar la estructura de datos para enviar como respuesta
        data = {
            "Client": documentClient,
            "DocumentLine": documentLine
        }

        # Verificar si el socio de negocio ya existe en la base de datos
        if sn.verificarSocioDB(cardCode):
            cotiza = Cotizacion()
            lines_data = cotiza.formatearDatos(data)

            return JsonResponse(lines_data, safe=False)
        else:
            # Crear el cliente en caso de que no exista y responder
            sn.crearYresponderCliente(cardCode, rut)
            cotiza = Cotizacion()
            lines_data = cotiza.formatearDatos(data)
            return JsonResponse(lines_data, safe=False)
        
    def copiarAODV(self, request):
        # Obtener el parámetro 'docentry' de la solicitud
        docentry = request.GET.get('documento_copiado')
        client = APIClient()

        # Llamar al método para obtener los detalles del cliente
        documentClient = client.detalleCotizacionCliente(docentry)
        documentLine = client.detalleCotizacionLineas(docentry)
        
        # Preparar la estructura de datos para enviar como respuesta
        data = {
            "Client": documentClient,
            "DocumentLine": documentLine
        }

        cotiza = Cotizacion()
        datosQuotations = cotiza.formatearDatos(data)

        lines_data = cotiza.reemplazarQuotationsPorOrders(datosQuotations)

        return JsonResponse(lines_data, safe=False)

        
    def duplicarCotizacion(self, request):
        
        docentry = request.GET.get('docentry')
        client = APIClient()        
        lineasDocumento = client.detalleCotizacionLineas(docentry)
        
        data = {
            "DocumentLine": lineasDocumento
        }
                
        cotiza = Cotizacion()
        lines_data = cotiza.formataearDatosSoloLineas(data)
                
        return JsonResponse(lines_data, safe=False)
        
