from adapters.serializador import Serializador
from adapters.sl_client import APIClient
from datosLsApp.repositories.productorepository import ProductoRepository
from taskApp.models import SyncState
from django.db import transaction

class Producto:

    def sync(self):
        # Obtener el valor de `skip` de la base de datos, si no existe, lo crea en 0
        state, created = SyncState.objects.get_or_create(key='product_sync_skip', defaults={'value': 0})

        with transaction.atomic():
            skip = state.value

            # Obtener datos desde SAP
            apiConect = APIClient()
            jsonProductos = apiConect.obtenerProductosSL(skip=skip)

            # Serializar los productos
            serialcer = Serializador('json')
            jsonserializado = serialcer.formatearDatos(jsonProductos)

            # Guardar productos en la base de datos
            repo = ProductoRepository()
            creacion = repo.sync_products_and_stock(jsonserializado)

            #if creacion is not None:
                # Si la sincronización fue exitosa, incrementar el valor de `skip`

            print(f"Skip antes de incrementar: {state.value}")
            state.value += 1
            print(f"Skip después de incrementar: {state.value}")
            state.save()  # Guardar el nuevo valor de `skip`
            print(f"Productos obtenidos: {jsonserializado}")

            return "Productos Sincronizados"

