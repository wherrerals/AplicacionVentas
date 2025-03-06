from unittest.mock import patch, MagicMock
from django.test import TestCase
from adapters.sl_client import APIClient
from datosLsApp.repositories.productorepository import ProductoRepository
from logicaVentasApp.services.producto import Producto
from taskApp.models import SyncState



class ProductoSyncTest(TestCase):

    def setUp(self):
        """Configuración inicial: Crear un estado de sincronización en la BD"""
        self.state = SyncState.objects.create(key='product_sync_skip', value=0)
        self.producto = Producto()

    @patch.object(APIClient, 'contarProductos')
    def test_sync_falla_cuando_api_no_retorna_datos_validos(self, mock_contarProductos):
        """Debe retornar error si la API no devuelve datos válidos"""
        mock_contarProductos.return_value = {}  # Respuesta inválida

        resultado = self.producto.sync()

        self.assertEqual(resultado, "Error: El método contarProductos no retornó datos válidos.")

    @patch.object(APIClient, 'contarProductos')
    @patch.object(APIClient, 'obtenerProductosSL')
    def test_sync_no_actualiza_skip_si_no_hay_productos(self, mock_obtenerProductosSL, mock_contarProductos):
        """Debe mantener el mismo `skip` si no hay productos"""
        mock_contarProductos.return_value = {'value': [{'ItemsCount': 100}]}  # Hay 100 productos en API
        mock_obtenerProductosSL.return_value = []  # No se devuelven productos

        skip_inicial = self.state.value
        resultado = self.producto.sync()

        self.state.refresh_from_db()
        self.assertEqual(self.state.value, skip_inicial)  # `skip` no cambia
        self.assertEqual(resultado, "0 productos sincronizados exitosamente")

    @patch.object(APIClient, 'contarProductos')
    @patch.object(APIClient, 'obtenerProductosSL')
    @patch.object(ProductoRepository, 'sync_products_and_stock')
    def test_sync_actualiza_skip_despues_de_sincronizacion(self, mock_sync_products, mock_obtenerProductosSL, mock_contarProductos):
        """Debe incrementar `skip` después de sincronizar productos correctamente"""
        mock_contarProductos.return_value = {'value': [{'ItemsCount': 100}]}  # 100 productos en API
        mock_obtenerProductosSL.return_value = [{'id': 1}, {'id': 2}, {'id': 3}]  # Devuelve 3 productos
        mock_sync_products.return_value = True  # Simula sincronización exitosa

        resultado = self.producto.sync()

        self.state.refresh_from_db()
        self.assertEqual(self.state.value, 3)  # `skip` se incrementa en 3
        self.assertEqual(resultado, "3 productos sincronizados exitosamente")

    @patch.object(APIClient, 'contarProductos')
    @patch.object(APIClient, 'obtenerProductosSL')
    def test_sync_reinicia_skip_si_supera_total(self, mock_obtenerProductosSL, mock_contarProductos):
        """Debe reiniciar `skip` cuando alcanza el total de productos"""
        self.state.value = 100  # `skip` ya está en 100
        self.state.save()

        mock_contarProductos.return_value = {'value': [{'ItemsCount': 100}]}  # Total de productos = 100
        mock_obtenerProductosSL.return_value = []  # No importa la respuesta, debería reiniciar `skip`

        self.producto.sync()

        self.state.refresh_from_db()
        self.assertEqual(self.state.value, 0)  # `skip` debe reiniciarse a 0
