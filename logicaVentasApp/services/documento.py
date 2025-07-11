from abc import ABC, abstractmethod
import logging

from django.db.models import Sum

from adapters.sl_client import APIClient
from datosLsApp.models.lineadb import LineaDB
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.documentorepository import DocumentoRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.serializer.documentSerializer import SerializerDocument

logger = logging.getLogger(__name__)

class Documento(ABC):
    
    def __init__(self, request=None):
        self.request = request
        self.docEntry = None
        self.docNum = None
        self.folio = None
        self.fechaDocumento = None
        self.fechaEntrega = None
        self.horarioEntrega = None
        self.referencia = None
        self.comentario = None
        self.totalAntesDelDescuento = None
        self.descuento = None
        self.totalDocumento = None
        self.codigoVenta = None
        self.tipo_documento = None
        self.vendedor = None
        self.condi_pago = None
        self.tipoentrega = None
        self.tipoobjetoSap = None
        # Otros atributos comunes a todos los documentos



    def get_endpoint(self):
        """
        Método abstracto para obtener el endpoint específico del documento.
        Debe ser implementado por las subclases.
        """
        pass

    def validarDatosObligatorios(self):
        """
        Método para validar los datos obligatorios del documento.
        Implementa aquí la validación común para todos los documentos.
        """
        if not self.fechaDocumento or not self.fechaEntrega or not self.codigoVenta:
            raise ValueError("Faltan datos obligatorios para el documento.")

    def crearOActualizarDocumento(self):
        """
        Método para crear o actualizar un documento.
        Utiliza `self.docEntry` para decidir si debe crear o actualizar.
        """
        self.validarDatosObligatorios()
        if self.docEntry:
            return self.actualizarDocumento()
        else:
            return self.crearDocumento()

    def crearDocumento(self):
        """
        Método para crear un nuevo documento.
        """
        try:
            json_data = self.preparar_json_data()
            endpoint = self.get_endpoint()
            headers = {"Content-Type": "application/json"}
            result = self.client.post_data(endpoint, data=json_data, headers=headers)
            return result
        except Exception as e:
            logger.error(f"Error al crear el documento: {e}")
            raise

    def actualizarDocumento(self):
        """
        Método para actualizar un documento existente.
        """
        if not self.docEntry:
            raise ValueError("No se puede actualizar un documento sin DocEntry.")
        try:
            json_data = self.preparar_json_data()
            endpoint = f"{self.get_endpoint()}/{self.docEntry}"
            headers = {"Content-Type": "application/json"}
            result = self.client.post_data(endpoint, data=json_data, headers=headers)
            return result
        except Exception as e:
            logger.error(f"Error al actualizar el documento: {e}")
            raise

    def obtenerDocumentoPorDocEntry(self):
        """
        Método para obtener un documento por su DocEntry.
        """
        try:
            endpoint = f"{self.get_endpoint()}/{self.docEntry}"
            result = self.client.getData(endpoint=endpoint)
            return result
        except Exception as e:
            logger.error(f"Error al obtener el documento: {e}")
            raise

    def obtenerDocumentoPorDocNum(self):
        """
        Método para obtener un documento por su DocNum.
        """
        try:
            endpoint = self.get_endpoint()
            filters = {"DocNum": f"eq '{self.docNum}'"}
            result = self.client.getData(endpoint=endpoint, filters=filters)
            return result
        except Exception as e:
            logger.error(f"Error al obtener el documento: {e}")
            raise

    def filtroDocumentos(self):
        """
        Método para filtrar documentos.
        """
        try:
            filters = self.prepare_filters()
            endpoint = self.get_endpoint()
            result = self.client.getData(endpoint=endpoint, filters=filters)
            return result
        except Exception as e:
            logger.error(f"Error al filtrar documentos: {e}")
            raise

    def getdocumentlines(self):
        """
        Método abstracto para obtener las líneas del documento.
        Debe ser implementado por las subclases.
        """
        pass
    

    def prepararJsonData(self, data):
        """
        Prepara los datos JSON para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass

    def get_endpoint(self):
        """
        Define el endpoint para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass

    def validar_check(self, data):
        tiene_marcado = False

        for item in data.get('DocumentLines', []):
            if item.get('EstadoCheck') == 1:
                tiene_marcado = True
                break

        if not tiene_marcado:
            return "Debe marcar al menos un producto para la devolución."
        return ""

    def create_document_db(self, data):

        try:
            errores = self.validar_datos_de_documentos(data)
            errores += self.validar_check(data)

            if errores:
                return {'error': errores}
            
            jsonData = SerializerDocument.document_serializer2(data)
            create_rr = DocumentoRepository.create_document_db(jsonData, data.get('creado_por')) 

            if create_rr:
                id_solicitud = create_rr.id

                return {
                        'success': True,
                        'title': 'Solicitud D. Creada',
                        'message': f'Solicitud D. Creada, Pendiente. N°: {id_solicitud}',
                        'id_solicitud': id_solicitud, 
                        'docNum': "",
                        'docEntry': ""
                        }

            return True
        
        except Exception as e:
            logger.error(f"Error al crear la cotización: {str(e)}")
            return {'error': str(e)}


    def update_document_db(self, id, data):
        print("Updating document in database with data:", data)
        try:

            errores = self.validar_datos_de_documentos(data)
            errores += self.validar_check(data)

            if errores:
                return {'error': errores}
            
            jsonData = SerializerDocument.document_serializer2(data)
            update_rr = DocumentoRepository.update_document_db(id, jsonData)

            if update_rr:
                id_solicitud = update_rr.id

                return {
                        'success': True, 
                        'title': 'Solicitud D. Actualizada',
                        'message': f'Solicitud D. Actualizada, Borrador. N°: {id_solicitud}',
                        'id_solicitud': id_solicitud, 
                        'docNum': "",
                        'docEntry': ""
                        }

            return True
        
        except Exception as e:
            logger.error(f"Error al actualizar el documento: {str(e)}")
            return {'error': str(e)}
        

    def validar_datos_de_documentos(self, data):
        errores = []

        # Verificar que el cardcode esté presente
        if not data.get('CardCode'):
            errores.append("No se a ingresado cliente para la Cotizacion.")

        if not data.get('DocumentLines'):
            errores.append("La cotización debe tener al menos una línea de documento.")

        # Verificar que la cantidad sea válida (mayor que cero)
        for item in data.get('DocumentLines', []):
            cantidad = item.get('Quantity', 0)
            if cantidad <= 0:
                errores.append(f"La cantidad del artículo {item.get('ItemCode')} debe ser mayor a cero.")

        # Verificar que otros campos importantes estén presentes (esto depende de los campos requeridos)
        if not data.get('DocDate'):
            errores.append("La fecha del documento es obligatoria.")

        """ 
        if not data.get('DocDueDate'):
            errores.append("La fecha de vencimiento es obligatoria.")

        """
        
        tipo_devolucion = data.get('U_LED_TIPDEV')
        folio = data.get('Folio')
        if tipo_devolucion != 'INTE' and (not folio or folio.strip() == ''):
            errores.append(f"Folio no ingresado para el tipo de {tipo_devolucion} seleccionado.")

        # Si hay errores, retornarlos como una cadena
        return ' '.join(errores)
    


    def saldo_disponible_linea(docentry_ref, producto_codigo, numLinea):
        lineas = LineaDB.objects.filter(
            docEntryBase=docentry_ref,
            producto__codigo=producto_codigo,
            numLineaBase=numLinea,
            estado_devolucion=1
        )

        if not lineas.exists():
            raise Exception("No hay líneas asociadas a estos criterios.")

        cantidad_original = lineas.values_list('cantidad_solicitada', flat=True).first()
        total_devuelto = lineas.aggregate(total=Sum('cantidad'))['total'] or 0
        saldo = cantidad_original - total_devuelto

        return saldo


