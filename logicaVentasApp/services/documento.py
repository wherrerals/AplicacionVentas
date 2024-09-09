from abc import ABC, abstractmethod
import logging

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


    @abstractmethod
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

    @abstractmethod
    def getdocumentlines(self):
        """
        Método abstracto para obtener las líneas del documento.
        Debe ser implementado por las subclases.
        """
        pass
    

    @abstractmethod
    def prepararJsonData(self, data):
        """
        Prepara los datos JSON para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass

    @abstractmethod
    def get_endpoint(self):
        """
        Define el endpoint para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass