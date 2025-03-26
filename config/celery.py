# config/celery.py
from datetime import timedelta
import os
from celery import Celery
from celery.schedules import crontab

# Configuración del entorno de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

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
    # Gestión de tareas y colas
    task_create_missing_queues=True,
    task_acks_late=True,  # Confirmar tarea después de completarla
    worker_prefetch_multiplier=1,  # Controlar la cantidad de tareas tomadas por worker
    
    # Configuraciones de resultados
    result_backend_max_results=10000,  # Aumentar número de resultados retenidos
    result_expires=172800,  # Resultados expiran después de 24 horas
    
    # Manejo de errores y reintentos
    task_retry_max=3,  # Número máximo de reintentos
    task_retry_delay=5,  # Retraso entre reintentos (en segundos)
    task_track_started=True,  # Rastrear cuando una tarea comienza
    
    # Configuraciones de rendimiento
    worker_cancel_long_running_tasks_on_connection_loss=True,
    task_time_limit=300,  # Límite de tiempo para tareas (5 minutos)
    task_soft_time_limit=240,  # Límite suave de tiempo (4 minutos)
)

# Configuración de beat_schedule para ejecutar múltiples tareas
app.conf.beat_schedule = {
    "data-product": {
        "task": "taskApp.tasks.sync_products",  # Ruta correcta a la tarea
        #"schedule": crontab(minute="*/1"),  # Ejecutar cada minuto
        "schedule": timedelta(seconds=10),  # Ejecutar cada 10 segundos
    },
    
    "data-user": {
        "task": "taskApp.tasks.syncUser",  # Ruta correcta a la tarea
        #"schedule": crontab(minute="*/1"),  # Ejecutar cada minuto
        "schedule": timedelta(seconds=10),  # Ejecutar cada 10 segundos
    },
}
