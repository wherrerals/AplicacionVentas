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
from datosLsApp.repositories.documentorepository import DocumentoRepository
from datosLsApp.serializer.documentSerializer import SerializerDocument
from logicaVentasApp.services.cotizacion import Cotizacion
import json
import requests
from requests.exceptions import RequestException
import urllib3

from logicaVentasApp.services.documento import Documento
from logicaVentasApp.services.socionegocio import SocioNegocio
from logicaVentasApp.services.solicituddevolucion import SolicitudesDevolucion

# Desactivar las advertencias de SSL inseguro (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ReturnsView(View):

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

    def get_route_map(self):
        return {
            '/': self.filtrarCotizaciones,
            '/ventas/detalles_devolucion': self.detallesDevolucion,
            '/ventas/detalles_devolucion_pendiente': self.details_rr_pending,


        }

    def post_route_map(self):
        return {
            '/ventas/listado_solicitudes_devolucion': self.filtrarCotizaciones,
            '/ventas/crear_devolucion': self.crearOActualizarDevoluciones,
            '/ventas/solicitudes_pendientes': self.rr_pending_list,
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

    @csrf_exempt
    def get_endpoint(self):
        return 'ReturnRequest'
    
    @csrf_exempt
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
        filters = SolicitudesDevolucion.construirSolicitudesDevolucion(data)

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
    def detallesDevolucion(self, request):
        # Obtener el parámetro 'docentry' de la solicitud
        docentry = request.GET.get('docentry')
        client = APIClient()

        # Llamar al método para obtener los detalles del cliente
        documentClient = client.detallesRR(docentry)

        if documentClient.get("odata.metadata") == "$metadata#Collection(Edm.ComplexType)" and not documentClient.get("value"):
            documentClient = client.detallesRR2(docentry)

        documentLine = client.detallesRRlineas(docentry)

        # Extraer los datos de la clave 'value', asegurándose de manejar la estructura correctamente
        quotations_data = documentClient.get('value', [{}])[0].get('ReturnRequest', {})
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
            rr = SolicitudesDevolucion()
            lines_data = rr.formatearDatos(data)

            return JsonResponse(lines_data, safe=False)
        else:
            # Crear el cliente en caso de que no exista y responder
            sn.crearYresponderCliente(cardCode, rut)
            rr = SolicitudesDevolucion()
            lines_data = rr.formatearDatos(data)
            return JsonResponse(lines_data, safe=False)


    @csrf_exempt
    def crearOActualizarDevoluciones(self, request):
        try:
            data = json.loads(request.body)
            users_data = self.user_data(request)
            docEntry = data.get('DocEntry')
            docnum = data.get('DocNum')
            id_docu = data.get('id_documento')
            aprobacion = data.get('Approve')

            doc = Documento()
            rr = SolicitudesDevolucion()
            
            print("docEntry:", docEntry)

            if docEntry != '':
                aprobacion = 1

            if aprobacion != 1:
                if id_docu != '':
                    update_db = doc.update_document_db(id_docu, data)
                    return JsonResponse(update_db, status=200)
                
                else:
                    create_db = doc.create_document_db(data)
                    return JsonResponse(create_db, status=201)
                
            else:
                if docEntry:
                    if self.validar_vendedor(users_data['vendedor'], data['SalesPersonCode']) == True:
                        
                        actualizacion = rr.actualizarDocumento(docnum, docEntry, data)
                        
                        print("Actualización de documento:", actualizacion)


                        return JsonResponse(actualizacion, status=200)
            
                    else:
                        data['SalesPersonCode'] = users_data['vendedor']
                        creacion = rr.crearDocumento(data)
                        return JsonResponse(creacion, status=201)
                else:
                    creacion = rr.crearDocumento(data)
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
    
    def rr_pending_list(self, request):

        try:
            data = json.loads(request.body)
            filters = data.get('filters', {})
            page = data.get('page', 1)
            limit = data.get('top', 20)
            offset = (page - 1) * limit

            total_records = DocumentoRepository.get_total_documents(
                filtro_id=filters.get('id', None),
                filtro_nombre=filters.get('nombre', None),
                filtro_sucursal=filters.get('sucursal', None),
                filtro_estado=filters.get('estado', None)
            )

            documents = DocumentoRepository.get_document(
                filtro_id=filters.get('id', None),
                filtro_nombre=filters.get('nombre', None),
                filtro_sucursal=filters.get('sucursal', None),
                filtro_estado=filters.get('estado', None),
                offset=offset,
                limite=limit
            )

            return JsonResponse({
                "data": {
                    "value": documents,
                },
                "totalRecords": total_records,
                "page": page,
                "limit": limit
            }, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

    def details_rr_pending(self, request):

        id = request.GET.get('id')
        documents_data = DocumentoRepository.get_document_data_lines(filtro_id=id)
        serilized_data = SerializerDocument.serialize_documento_completo(documents_data)
        
        return JsonResponse(serilized_data, safe=False)