from adapters.serializador import Serializador
from adapters.sl_client import APIClient
from datosLsApp.repositories.productorepository import ProductoRepository

class Producto:


    def sync(self):
        # Obtener datos desde SAP
        apiConect = APIClient()
        jsonProductos = apiConect.obtenerProductosSL()

        # Serializar datos
        serialcer = Serializador('json')
        jsonserializado = serialcer.formatearDatos(jsonProductos)

        # Guardar productos en la base de datos
        repo = ProductoRepository()
        creacion = repo.sync_products_and_stock(jsonserializado)


        if creacion:
            return "Productos Sincronizados"

        print(f"Productos obtenidos: {jsonserializado}")