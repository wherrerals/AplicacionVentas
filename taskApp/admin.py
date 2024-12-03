from django.contrib import admin

# Register your models here.
# tasks_app/admin.py
from django.contrib import admin
from .models import CeleryTask

@admin.register(CeleryTask)
class CeleryTaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_id', 'status', 'timestamp', 'result')
    search_fields = ('task_id', 'task_name')
    list_filter = ('status',)
    readonly_fields = ('task_id', 'task_name', 'status', 'result', 'timestamp')

    def get_queryset(self, request):
        """Filtra las tareas para mostrar solo las relevantes."""
        return super().get_queryset(request).order_by('-timestamp')
