# taskApp/tasks.py
from celery import shared_task, states
from celery.result import AsyncResult
from logicaVentasApp.services.socionegocio import SocioNegocio
from taskApp.models import CeleryTask
from logicaVentasApp.services.producto import Producto

# tasks.py
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

@shared_task(bind=True)
def sync_products(self):
    # Registrar la tarea en la base de datos al iniciar
    task = CeleryTask.objects.create(
        task_id=self.request.id,
        task_name=self.name,
        status=states.PENDING
    )
    
    try:
        print("Sincronizando productos...")
        service = Producto()
        result_message = service.sync()  # Captura el retorno de sync()

        # Actualizar el estado y guardar el resultado
        task.status = states.SUCCESS
        task.result = result_message  # Guarda el mensaje retornado
        return result_message
    
    except Exception as e:
        # Manejo de errores
        task.status = states.FAILURE
        task.result = str(e)
        raise
    finally:
        task.save()

@shared_task(bind=True)
def syncUser(self):
    # Registrar la tarea en la base de datos al iniciar
    task2 = CeleryTask.objects.create(
        task_id=self.request.id,
        task_name=self.name,
        status=states.PENDING
    )
    
    try:
        print("Sincronizando usuarios...")
        # Llamada al servicio de sincronización
        service = SocioNegocio(request=None)
        result_message = service.syncBusinessPartners()  # Captura el retorno de sync()

        # Actualizar el estado y guardar el resultado
        task2.status = states.SUCCESS
        task2.result = "Usuarios sincronizados"  # Guarda el mensaje retornado
        return result_message
    
    except Exception as e:
        # Manejo de errores y actualización de la tarea
        task2.status = states.FAILURE
        task2.result = str(e)
        raise
    finally:
        task2.save()
        



@shared_task(queue='q_pdf_generation')
def generar_pdf_async(cotizacion_id, cotizacion_data, absolute_uri):

    print(cotizacion_id, cotizacion_data, absolute_uri)
    # Renderizar el HTML
    print("PASO 2")
    html_string = render_to_string('cotizacion_template2.html', {'cotizacion': cotizacion_data})
    
    print("PASO 3")
    # Generar el PDF
    pdf_file = HTML(string=html_string, base_url=absolute_uri).write_pdf()
    
    print("PASO 4")
    # Guardar el PDF en un almacenamiento (por ejemplo, S3 o sistema de archivos)
    file_name = f"cotizacion_{cotizacion_id}.pdf"
    default_storage.save(file_name, ContentFile(pdf_file))
    
    print("PASO FINAL GENERACION")
    return file_name  # Retorna el nombre del archivo para su descarga