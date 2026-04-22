# views/pdf_views.py

import json
from django.http import HttpResponse
from domain.services.pdf_services import CotizacionPDFService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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