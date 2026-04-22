import json
from django.contrib.auth import authenticate
from adapters.sl_client import APIClient
from api_go.serializers.document_serializer import CotizacionSerializer
from api_go.utils.documents_utils import CotizacionPayloadBuilder
from domain.services.cotizacion import Cotizacion
from domain.services.pdf_services import CotizacionPDFService
from presentation.views.cotizacionview import CotizacionView
from rest_framework.views import APIView
from rest_framework.response import Response
from infrastructure.repositories.productorepository import ProductoRepository
from taskApp.tasks import sync_products_task
from django.test import RequestFactory
from rest_framework import status
from django.http import HttpResponse

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