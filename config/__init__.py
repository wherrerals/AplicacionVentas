from __future__ import absolute_import, unicode_literals

# Esto asegura que Celery se inicialice cuando inicie Django
from .celery import app as celery_app

__all__ = ('celery_app',)
