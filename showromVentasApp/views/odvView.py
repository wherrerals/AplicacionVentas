import logging
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from adapters.sl_client import APIClient
import json
from requests.exceptions import RequestException
import urllib3
from logicaVentasApp.services.odv import OrdenVenta
from logicaVentasApp.services.socionegocio import SocioNegocio
# Desactivar las advertencias de SSL inseguro (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class OdvView(View):

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            docEntry = kwargs.get("DocEntry")
            if docEntry:
                return self.quotate_items(request, docEntry)

            route_handler = self.get_route_map().get(request.path.rstrip("/"), None)
            if route_handler is None:
                return JsonResponse({"error": "Ruta no válida"}, status=404)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in GET method: {str(e)}")
            return self.handle_error(e)

    def post(self, request, *args, **kwargs):
        try:
            path = request.path
            route_handler = self.post_route_map().get(
                path
            ) or self.post_route_map().get(path.rstrip("/"))
            if route_handler is None:
                return JsonResponse({"error": "Ruta no válida"}, status=404)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in POST method: {str(e)}")
            return self.handle_error(e)

    def get_route_map(self):
        return {
            "/ventas/detalles_ODV": self.detallesODV,
        }

    def post_route_map(self):

        return {
            "/ventas/crear_odv": self.crearOActualizarODV,
            "/ventas/listado_odv": self.filtrarODV,
        }

    def handle_invalid_route(self, request):
        return JsonResponse({"error": "Ruta inválida"}, status=404)

    def handle_error(self, exception):
        if isinstance(exception, json.JSONDecodeError):
            return JsonResponse({"error": "JSON inválido"}, status=400)
        if isinstance(exception, RequestException):
            return JsonResponse(
                {"error": "Error de conexión con el servidor externo"}, status=503
            )
        logger.exception("Unexpected error")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)

    def filtrarODV(self, request):
        """
        Maneja la solicitud para filtrar cotizaciones, delegando la lógica de construcción de filtros a una función separada.
        """
        client = APIClient()

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        filters = OrdenVenta.construirFiltrosODV(data)

        try:
            top = int(data.get("top", 20))
            skip = int(data.get("skip", 0))
        except ValueError:
            return JsonResponse({"error": "Invalid parameters"}, status=400)
        try:
            data = client.getODV(top=top, skip=skip, filters=filters)
            return JsonResponse({"data": data}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


    def detallesODV(self, request):

        docentry = request.GET.get("docentry")
        client = APIClient()

        documentClient = client.detallesOrdenVentaCliente(docentry)

        if documentClient.get("odata.metadata") == "$metadata#Collection(Edm.ComplexType)" and not documentClient.get("value"):
            documentClient = client.detallesOrdenVentaCliente2(docentry)

        documentLine = client.detallesOrdenVentaLineas(docentry)
        

        quotations_data = documentClient.get("value", [{}])[0].get("Orders", {})
        cardCode = quotations_data.get("CardCode")
        rut = quotations_data.get("FederalTaxID")

        sn = SocioNegocio(request)

        data = {"Client": documentClient, "DocumentLine": documentLine}

        # Verificar si el socio de negocio ya existe en la base de datos
        if sn.verificarSocioDB(cardCode):
            odv = OrdenVenta()
            lines_data = odv.formatearDatos(data)

            return JsonResponse(lines_data, safe=False)
        else:
            # Crear el cliente en caso de que no exista y responder
            sn.crearYresponderCliente(cardCode, rut)
            odv = OrdenVenta()
            lines_data = odv.formatearDatos(data)
            return JsonResponse(lines_data, safe=False)

    @csrf_exempt
    def crearOActualizarODV(self, request):
        try:
            data = json.loads(request.body)
            docEntry = data.get("DocEntry")
            docnum = data.get("DocNum")

            odv = OrdenVenta()

            if docEntry:
                actualizacion = odv.actualizarDocumento(docnum, docEntry, data)
                return JsonResponse(actualizacion, status=200)
            else:
                creacion = odv.crearDocumento(data)
                return JsonResponse(creacion, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
