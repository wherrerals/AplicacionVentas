from adapters.serializador import Serializador
from adapters.sl_client import APIClient
from datosLsApp.repositories.productorepository import ProductoRepository
from taskApp.models import SyncState
from django.db import transaction
import pika


class Producto:

    def sync(self):
        state, created = SyncState.objects.get_or_create(key='product_sync_skip', defaults={'value': 0})
        skip = state.value
        total_synced = 0

        while True:
            # Obtener productos de la API de Sales Layer
            re = APIClient()
            productos = re.obtenerProductosSL(skip=skip)
            if not productos:  # Si no hay más productos, se detiene la sincronización
                break

            # Serializar y guardar productos
            serialcer = Serializador('json')
            jsonserializado = serialcer.formatearDatos(productos)
            repo = ProductoRepository()
            creacion = repo.sync_products_and_stock(jsonserializado)

            if creacion:
                synced_count = len(jsonserializado)
                total_synced += synced_count
                # Actualizar el estado de `skip` para la siguiente llamada
                state.value += synced_count
                state.save()

            # Incrementar `skip` en función de la cantidad de productos procesados
            skip += len(productos)

        return f"{total_synced} productos sincronizados exitosamente"
        
"""

            #if creacion is not None:
                # Si la sincronización fue exitosa, incrementar el valor de `skip`

            print(f"Skip antes de incrementar: {state.value}")
            state.value += 1
            print(f"Skip después de incrementar: {state.value}")
            state.save()  # Guardar el nuevo valor de `skip`
            print(f"Productos obtenidos: {jsonserializado}")

            return "Productos Sincronizados"
"""
