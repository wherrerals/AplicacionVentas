from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configuración del entorno de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Ajusta 'config.settings' al nombre correcto de tu proyecto

app = Celery('AplicacionVentas')

# Carga la configuración desde el archivo settings.py de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubre tareas definidas en aplicaciones instaladas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
