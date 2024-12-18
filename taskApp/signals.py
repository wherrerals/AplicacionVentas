# taskApp/signals.py
from celery.signals import task_postrun, task_prerun
from taskApp.models import CeleryTask

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, *args, **kwargs):
    """Antes de ejecutar la tarea, actualiza el estado a STARTED."""
    CeleryTask.objects.filter(task_id=task_id).update(status='STARTED')

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, state=None, *args, **kwargs):
    """Después de ejecutar la tarea, actualiza el estado y resultado."""
    try:
        task_record = CeleryTask.objects.get(task_id=task_id)
        task_record.status = state
        if state == 'SUCCESS':
            task_record.result = kwargs.get('retval', 'Resultado no disponible')
        elif state == 'FAILURE':
            task_record.result = kwargs.get('exception', 'Error no especificado')
        task_record.save()
    except CeleryTask.DoesNotExist:
        pass  # Si no se encuentra, no hacemos nada
