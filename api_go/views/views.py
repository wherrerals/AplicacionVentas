import json
from django.contrib.auth import authenticate
from adapters.sl_client import APIClient
from presentation.views.cotizacionview import CotizacionView
from rest_framework.views import APIView
from rest_framework.response import Response
from infrastructure.repositories.productorepository import ProductoRepository
from taskApp.tasks import sync_products_task
from django.test import RequestFactory
from rest_framework import status

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
        # 1. Validar que existan los bloques requeridos
        auth_data = request.data.get("auth")
        data = request.data.get("data")

        if not auth_data or not data:
            return Response(
                {"success": False, "error": "Se requieren los campos 'auth' y 'data'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Autenticar y validar usuario
        user = authenticate(
            username=auth_data.get("username"),
            password=auth_data.get("password"),
        )

        if user is None:
            return Response(
                {"success": False, "error": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"success": False, "error": "Usuario inactivo"},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Construir request sintético para CotizacionView
        factory = RequestFactory()
        synthetic_request = factory.post(
            '/documents/',
            data=json.dumps(data),
            content_type='application/json'
        )
        synthetic_request.user = user  # ← inyectar usuario autenticado

        # 4. Llamar a la vista con el request sintético
        try:
            view_instance = CotizacionView()
            json_response = view_instance.crearOActualizarCotizacion(synthetic_request)

            # JsonResponse → dict para poder retornarlo en DRF
            result = json.loads(json_response.content)

            return Response(
                {"success": True, "result": result},
                status=json_response.status_code
            )

        except Exception as e:
            return Response(
                {"success": False, "error": f"Error interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )