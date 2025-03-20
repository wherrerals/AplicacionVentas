# taskApp/tasks.py
from venv import logger
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
        



""" @shared_task(queue='q_pdf_generation')
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
    return file_name  # Retorna el nombre del archivo para su descarga """

# In tasks.py - Optimize the task to be more efficient
@shared_task(queue='q_pdf_generation')
def generar_pdf_async(cotizacion_id, cotizacion_data, absolute_uri):
    try:
        # Log start of PDF generation
        logger.info(f"Iniciando generación de PDF para cotización {cotizacion_id}")
        
        # Renderizar el HTML
        html_string = render_to_string('cotizacion_template2.html', {'cotizacion': cotizacion_data})
        
        # Configurar opciones para optimizar la generación del PDF
        pdf_options = {
            'quiet': True,  # Reduce logging output
            'print-media-type': True,  # Use print media type
            'page-size': 'Letter',  # Standard page size
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
        }
        
        # Generar el PDF con opciones optimizadas
        pdf_file = HTML(string=html_string, base_url=absolute_uri).write_pdf(stylesheets=[], **pdf_options)
        
        # Codificar el PDF en base64 para transmitirlo como JSON
        import base64
        pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')
        
        # Log completion
        logger.info(f"PDF generado exitosamente para cotización {cotizacion_id}")
        
        # Retornar el contenido codificado y el nombre del archivo
        return {
            'pdf_content': pdf_base64,
            'file_name': f"cotizacion_{cotizacion_id}.pdf"
        }
    except Exception as e:
        logger.error(f"Error generando PDF para cotización {cotizacion_id}: {str(e)}")
        # Re-raise the exception to mark the task as failed
        raise

""" 
pdf_options = {
    'quiet': True,  # Reduce logging output
    'print-media-type': False,  # No usar media type para impresión
    'page-size': 'A4',  # Usar A4, más estándar y puede reducir tamaño
    'dpi': 72,  # Reducir la resolución de renderizado (por defecto suele ser 300)
    'image-quality': 50,  # Reducir la calidad de imágenes (de 0 a 100)
    'grayscale': True,  # Convertir a escala de grises (reduce tamaño)
    'lowquality': True,  # Genera un PDF con menor calidad
    'margin-top': '0.5in',
    'margin-right': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'encoding': 'UTF-8',
}
 """