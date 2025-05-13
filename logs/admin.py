from django.contrib import admin
from logs.models.documentslogs import DocumentLogDB

# Register your models here.
@admin.register(DocumentLogDB)
class DocumentLogAdmin(admin.ModelAdmin):
    list_display = ('docNum', 'docEntry', 'tipoDoc', 'url', 'created_at', 'estate')
    search_fields = ('docNum', 'tipoDoc')
    list_filter = ('tipoDoc', 'estate')
    readonly_fields = ('docNum', 'docEntry', 'tipoDoc', 'url', 'json', 'response', 'created_at', 'estate')