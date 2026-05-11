import json
import logging

from django.contrib.auth import authenticate
from adapters.sl_client import APIClient
from api_go.serializers.document_serializer import CotizacionSerializer
from api_go.utils.documents_utils import CotizacionPayloadBuilder
from domain.services.cotizacion import Cotizacion
from domain.services.pdf_services import CotizacionPDFService, FichaTecnicaPDFService
from presentation.views.cotizacionview import CotizacionView
from rest_framework.views import APIView
from rest_framework.response import Response
from infrastructure.repositories.productorepository import ProductoRepository
from taskApp.tasks import sync_products_task
from django.test import RequestFactory
from rest_framework import status
from django.http import HttpResponse

from domain.exeptions.pdf_exceptions import (
    MiddlewareTimeoutError,
    MiddlewareConnectionError,
    MiddlewareHTTPError,
    ProductoNotFoundError,
)

logger = logging.getLogger(__name__)


class ProductsAPIView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        auth_data = request.data.get("auth")
        products = request.data.get("products")

        if not auth_data:
            return Response({"error": "auth is required"}, status=400)

        if not isinstance(products, list):
            return Response({"error": "products must be a list"}, status=400)

        user = authenticate(
            username=auth_data.get("username"),
            password=auth_data.get("password"),
        )

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        task = sync_products_task.delay(products)

        return Response(
            {
                "status": "ok",
                "executed_by": user.username,
                "processed": len(products),
                "result": task.id,
            },
            status=200,
        )
    

class DocumentAPIView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        auth_data = request.data.get("auth")    
        data = request.data.get("data")

        if not auth_data or not data:
            return Response({"success": False, "error": "Se requieren los campos 'auth' y 'data'"},status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=auth_data.get("username"),password=auth_data.get("password"))

        if user is None:
            return Response({"success": False, "error": "Credenciales inválidas"},status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"success": False, "error": "Usuario inactivo"},status=status.HTTP_403_FORBIDDEN)

        payload = CotizacionPayloadBuilder.build(data)
        factory = RequestFactory()
 
        try:

            # Creacion de cotización
            quotate = Cotizacion()
            quotate_response = quotate.crearDocumento(payload)
            result = quotate_response
            docEntry = result.get("docEntry")


            if not docEntry:
                return Response({"success": False, "error": "No se obtuvo docEntry"},status=status.HTTP_400_BAD_REQUEST)

            # Pendiente por refactorizar (inicio)
            get_request = factory.get(f'/ventas/detalles_cotizacion/?docentry={docEntry}')
            get_request.user = user
            detalle_view = CotizacionView()
            detalle_response = detalle_view.detallesCotizacion(get_request)
            detalle_result = json.loads(detalle_response.content)
            # Pendiente por refactorizar (fin)

            serializer = CotizacionSerializer(detalle_result)
            pdf_service = CotizacionPDFService()
            pdf_file, tipo_documento, numero = pdf_service.generar_pdf(serializer.data)

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{tipo_documento}_{numero}.pdf"'

            return response  # <-- ESTO FALTA

        except Exception as e:
            return Response(
                {"success": False, "error": f"Error interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class TechnicalSheetAPIView(APIView):
    http_method_names = ["post"]

    def post(self, request):

        print(f"Recibiendo solicitud para Ficha Técnica: {request.data}")
        
        auth_data = request.data.get("auth")
        data = request.data.get("data", {})
        skus = data.get("skus", [])
        
        if not auth_data or not skus:
            return Response({"success": False, "error": "Se requieren los campos 'auth' y 'data'"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=auth_data.get("username"), password=auth_data.get("password"))

        if user is None:
            return Response({"success": False, "error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({"success": False, "error": "Usuario inactivo"},status=status.HTTP_403_FORBIDDEN)

    
        skus = [str(s).strip() for s in skus if str(s).strip()]
        return self._procesar(request, skus)
    # ── Lógica principal ────────────────────────────────────────────

    def _procesar(self, request, skus: list[str]):
        if not skus:
            return Response(
                {"error": "Se requiere al menos un SKU"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(skus) == 1:
            return self._respuesta_single(request, skus[0])

        service = FichaTecnicaPDFService()
        base_url = request.build_absolute_uri("/")
        
        from weasyprint import Document as WeasyDocument  # Evitar confusión con xml.dom.minidom.Document

        documentos: list[WeasyDocument] = []   # ← WeasyPrint Documents, no bytes
        skus_fallidos: dict[str, str] = {}

        for sku in skus:
            try:
                doc = service.generar_documento(sku=sku, base_url=base_url)  # ← nuevo método
                documentos.append(doc)
            except Exception as e:
                skus_fallidos[sku] = self._mensaje_error(e)
                logger.warning("SKU %s falló en lote: %s", sku, e)

        if not documentos:
            return Response(
                {
                    "error": "Ningún SKU pudo generarse correctamente",
                    "detalle": skus_fallidos,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Merge nativo WeasyPrint: el primer Document absorbe las páginas del resto
        documento_combinado = documentos[0].copy(
            [page for doc in documentos for page in doc.pages]
        )
        pdf_combinado = documento_combinado.write_pdf()

        nombre_archivo = f"fichas_tecnicas_{'_'.join(skus[:3])}.pdf"
        response = HttpResponse(pdf_combinado, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'

        if skus_fallidos:
            response["X-Skus-Failed"] = ",".join(skus_fallidos.keys())
            response["X-Skus-Failed-Detail"] = str(skus_fallidos)

        return response

    # ── Helpers ────────────────────────────────────────────────────

    @staticmethod
    def _respuesta_single(request, sku: str) -> HttpResponse:
        """Delega en el servicio y retorna idéntico a FichaTecnicaPDFView."""
        service = FichaTecnicaPDFService()
        try:
            pdf_file = service.generar_pdf(
                sku=sku,
                base_url=request.build_absolute_uri("/"),
            )
        except MiddlewareTimeoutError:
            return Response(
                {"error": "Timeout al obtener el producto"},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except MiddlewareConnectionError:
            return Response(
                {"error": "No se pudo conectar al middleware"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except MiddlewareHTTPError as e:
            http_status = (
                status.HTTP_404_NOT_FOUND
                if e.status_code == 404
                else status.HTTP_502_BAD_GATEWAY
            )
            return Response({"error": str(e)}, status=http_status)
        except ProductoNotFoundError:
            return Response(
                {"error": 'Data incompleta: falta "producto"'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.exception("Error inesperado para SKU %s", sku)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="ficha_tecnica_{sku}.pdf"'
        return response



    @staticmethod
    def _mensaje_error(exc: Exception) -> str:
        if isinstance(exc, MiddlewareTimeoutError):
            return "timeout"
        if isinstance(exc, MiddlewareConnectionError):
            return "connection_error"
        if isinstance(exc, MiddlewareHTTPError):
            return f"http_{exc.status_code}"
        if isinstance(exc, ProductoNotFoundError):
            return "producto_not_found"
        return str(exc)