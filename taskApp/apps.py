""" from django.apps import AppConfig


class TaskappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taskApp'
 """
# taskApp/apps.py
from django.apps import AppConfig

class TaskAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taskApp'

    def ready(self):
        import taskApp.signals  # Importar signals
