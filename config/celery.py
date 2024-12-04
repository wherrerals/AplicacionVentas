# config/celery.py
from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab

# Configuración del entorno de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Asegúrate de que el nombre del proyecto sea correcto

# Crear la aplicación Celery
app = Celery('taskApp')

# Cargar la configuración desde el archivo settings.py de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrir tareas en aplicaciones instaladas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.update(
    task_create_missing_queues=True,
    worker_pool='solo',  # Intenta usar 'solo' para evitar problemas de concurrencia
)


# Configuración de beat_schedule para ejecutar múltiples tareas
app.conf.beat_schedule = {
    "sync-products-every-minute": {
        "task": "taskApp.tasks.sync_products1",  # Ruta correcta a la tarea
        #"schedule": crontab(minute="*/1"),  # Ejecutar cada minuto
        "schedule": timedelta(seconds=5),  # Ejecutar cada 10 segundos
    },
    
    "data-product": {
        "task": "taskApp.tasks.sync_products",  # Ruta correcta a la tarea
        #"schedule": crontab(minute="*/1"),  # Ejecutar cada minuto
        "schedule": timedelta(seconds=5),  # Ejecutar cada 10 segundos
    },
}
