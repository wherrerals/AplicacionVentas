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
from infrastructure.models.regiondb import RegionDB
from infrastructure.models.usuariodb import UsuarioDB
from infrastructure.repositories.documentorepository import DocumentoRepository
from infrastructure.serializer.documentSerializer import SerializerDocument
from domain.services.cotizacion import Cotizacion
import json
import requests
from requests.exceptions import RequestException
import urllib3

from domain.services.documento import Documento
from domain.services.socionegocio import SocioNegocio
from domain.services.solicituddevolucion import SolicitudesDevolucion

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
        client = APIClient()
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        filters = SolicitudesDevolucion.construirSolicitudesDevolucion(data)

        print("Filters:", filters)

        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        try:
            data = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip, filters=filters)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    @csrf_exempt
    def detallesDevolucion(self, request):

        docentry = request.GET.get('docentry')

        client = APIClient()
        documentClient = client.detallesRR(docentry)

        if documentClient.get("odata.metadata") == "$metadata#Collection(Edm.ComplexType)" and not documentClient.get("value"):
            documentClient = client.detallesRR2(docentry)

        documentLine = client.detallesRRlineas(docentry)

        quotations_data = documentClient.get('value', [{}])[0].get('ReturnRequest', {})

        print("Quotations Data:", quotations_data)
        print("Document Line:", documentLine)

        cardCode = quotations_data.get('CardCode')
        rut = quotations_data.get('FederalTaxID')

        sn = SocioNegocio(request)
        rr = SolicitudesDevolucion()

        data = {
            "Client": documentClient,
            "DocumentLine": documentLine
        }

        if sn.verificarSocioDB(cardCode):
            lines_data = rr.formatearDatos(data)

            return JsonResponse(lines_data, safe=False)
        else:
            sn.crearYresponderCliente(cardCode, rut)
            lines_data = rr.formatearDatos(data)
            return JsonResponse(lines_data, safe=False)


    @csrf_exempt
    def crearOActualizarDevoluciones(self, request):
        try:
            data = json.loads(request.body)
            docEntry = data.get('DocEntry', '')
            docnum = data.get('DocNum', '')
            id_docu = data.get('id_documento', '')
            aprobacion = data.get('Approve')
            
            if docEntry != '':
                aprobacion = 1
  
            user = request.user
            data['creado_por'] = user.username

            doc = Documento()
            document_db = DocumentoRepository()
            if aprobacion != 1:
                if id_docu:
                    result = doc.update_document_db(id_docu, data)
                    return JsonResponse(result, status=200)
                else:
                    result = doc.create_document_db(data)
                    return JsonResponse(result, status=201)

            if docEntry:
                    repo = SolicitudesDevolucion()
                    result = repo.actualizarDocumento(docnum, docEntry, data)
                    return JsonResponse(result, status=200)
            else:
                repo = SolicitudesDevolucion()
                result = repo.crearDocumento(data)
                if result.get('success'):
                    document_db.update_document_status(id_docu, result.get('docNum'), result.get('docEntry'), 'Aprobado')
                return JsonResponse(result, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        except Exception as e:
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)

        
    def user_data(self, request):
        user = request.user

        codigoVendedor = UsuarioDB.objects.get(usuarios=user).vendedor.codigo
        sucursal = UsuarioDB.objects.get(usuarios=user).sucursal.nombre

        return {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'vendedor': codigoVendedor,
            'sucursal': sucursal
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

            print("Filters:", filters)

            total_records = DocumentoRepository.get_total_documents(
                filtro_id=filters.get('id', None),
                filtro_nombre=filters.get('nombre', None),
                filtro_sucursal=filters.get('sucursal', None),
                filtro_estado=filters.get('estado', None),
                filtro_tipo_devolucion=filters.get('U_LED_TIPDEV', None)
            )

            print("Total Records:", total_records)

            documents = DocumentoRepository.get_document(
                filtro_id=filters.get('id', None),
                filtro_nombre=filters.get('nombre', None),
                filtro_sucursal=filters.get('sucursal', None),
                filtro_estado=filters.get('estado', None),
                filtro_tipo_devolucion=filters.get('U_LED_TIPDEV', None),
                offset=offset,
                limite=limit
            )
            print("Documents:", documents)
            print("Total Records:", total_records)
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

        print("Serialized Data:", serilized_data)

        return JsonResponse(serilized_data, safe=False)