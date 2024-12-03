from adapters import sl_client
from adapters.serializador import Serializador
from datosLsApp.repositories import ProductoRepository

class Producto:
    def __init__(self):
        self.adapter = sl_client()
        self.serializer = Serializador()
        self.repository = ProductoRepository()

    def sync(self):
        # Obtener datos desde SAP
        products_data = self.adapter.fetch_products()
        stock_data = self.adapter.fetch_stock()
        prices_data = self.adapter.fetch_prices()

        # Serializar datos
        products = self.serializer.serialize_products(products_data)
        stock = self.serializer.serialize_stock(stock_data)

        # Crear o actualizar productos y stock
        self.repository.sync_products(products)
        self.repository.sync_stock(stock)
