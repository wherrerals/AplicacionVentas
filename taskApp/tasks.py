# logicaVentasApp/tasks.py
from celery import shared_task
from logicaVentasApp.services.producto import Producto



# Tarea Celery para sincronizar productos
@shared_task
def sync_products1():
    print("Sincronizando productos...")

@shared_task
def sync_products():
    service = Producto()
    service.sync()  # Llama al método de sincronización de productos

    