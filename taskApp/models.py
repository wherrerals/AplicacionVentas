from django.db import models

# Create your models here.
# tasks_app/models.py
from django.db import models
from celery.result import AsyncResult

class CeleryTask(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    task_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), ('STARTED', 'Started'), ('SUCCESS', 'Success'), ('FAILURE', 'Failure')])
    result = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def update_status(self):
        """Actualiza el estado y resultado de la tarea usando AsyncResult."""
        result = AsyncResult(self.task_id)
        if result.ready():
            self.status = result.status
            self.result = result.result if result.successful() else result.traceback
            self.save()
            
class SyncState(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.IntegerField(default=0)
    
    def __str__(self):
        return f"SyncState {self.key} = {self.value}"
