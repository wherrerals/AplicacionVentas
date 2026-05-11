# views/pdf_views.py
import logging
import json
from xml.dom.minidom import Document
from django.http import HttpResponse
from domain.exeptions.pdf_exceptions import (
    MiddlewareTimeoutError,
    MiddlewareConnectionError,
    MiddlewareHTTPError,
    ProductoNotFoundError,
)
from domain.services.pdf_services import CotizacionPDFService, FichaTecnicaPDFService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class CotizacionPDFView(APIView):

    def post(self, request, cotizacion_id):
        try:
            data = request.data

            service = CotizacionPDFService()
            pdf_file, tipo_documento, numero = service.generar_pdf(
                data,
                base_url=request.build_absolute_uri()
            )

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{tipo_documento}_{numero}.pdf"'

            return response

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class FichaTecnicaPDFView(APIView):
    def get(self, request, sku):
        service = FichaTecnicaPDFService()
        try:
            pdf_file = service.generar_pdf(
                sku=sku,
                base_url=request.build_absolute_uri('/')
            )
        except MiddlewareTimeoutError:
            return Response({"error": "Timeout al obtener el producto"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except MiddlewareConnectionError:
            return Response({"error": "No se pudo conectar al middleware"}, status=status.HTTP_502_BAD_GATEWAY)
        except MiddlewareHTTPError as e:
            http_status = status.HTTP_404_NOT_FOUND if e.status_code == 404 else status.HTTP_502_BAD_GATEWAY
            return Response({"error": str(e)}, status=http_status)
        except ProductoNotFoundError:
            return Response({"error": 'Data incompleta: falta "producto"'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception("Error inesperado generando ficha técnica para SKU %s", sku)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ficha_tecnica_{sku}.pdf"'
        return response


class FichaTecnicaMultiplePDFView(APIView):
    """
    GET  /api/fichas/?skus=SKU1,SKU2,SKU3
    POST /api/fichas/  body: {"skus": ["SKU1", "SKU2"]}

    - 1 SKU  → mismo comportamiento de FichaTecnicaPDFView
    - N SKUs → genera cada ficha, concatena los PDFs válidos.
               Los SKUs fallidos se reportan en la cabecera X-Skus-Failed
               sin abortar el lote.
    """

    def get(self, request):
        raw = request.query_params.get("skus", "")
        skus = [s.strip() for s in raw.split(",") if s.strip()]
        return self._procesar(request, skus)

    def post(self, request):
        skus = request.data.get("skus", [])
        if not isinstance(skus, list):
            return Response(
                {"error": '"skus" debe ser una lista'},
                status=status.HTTP_400_BAD_REQUEST,
            )
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