# views/pdf_views.py
import logging
import json
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