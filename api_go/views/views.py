import json
from django.contrib.auth import authenticate
from adapters.sl_client import APIClient
from rest_framework.views import APIView
from rest_framework.response import Response
from infrastructure.repositories.productorepository import ProductoRepository
from taskApp.tasks import sync_products_task


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