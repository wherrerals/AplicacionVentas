import json
import math
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
from datosLsApp.models.productodb import ProductoDB
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.repositories.stockbodegasrepository import StockBodegasRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from datosLsApp.serializer.documentSerializer import SerializerDocument
from logicaVentasApp.services.documento import Documento
from taskApp.tasks import update_components_task
import logging


from logs.services.documentlog import DocumentsLogs
logger = logging.getLogger(__name__)

class Cotizacion(Documento):

    """
    Clase para manejar las cotizaciones en la aplicación.

    Attributes:
        request (dict): Datos de la cotización.
        client (APIClient): Cliente de la API.
        cliente (dict): Datos del cliente.
        items (list): Líneas de la cotización.
    
    Methods:
        get_endpoint: Obtiene el endpoint específico de la cotización.
        validarDatosObligatorios: Valida los datos obligatorios de la cotización.
        crearOActualizarCotizacion: Crea o actualiza una cotización.
        validarDatosObligatorios: Valida los datos obligatorios de la cotización.
        construirFiltrosCotizaciones: Construye los filtros para la consulta de cotizaciones.
        buscarDocumentosCotizacion: Busca los detalles de una cotización basada en el DocEntry.
        prepararLineasInternas: Prepara las líneas de documento de la cotización para ser mostradas en la vista de detalle.
        crearDocumento: Crea una nueva cotización y maneja las excepciones según el código de respuesta.
        eliminarDocumento: Elimina una cotización.
        actualizarEstadoDocumento: Actualiza el estado de una cotización.
    """
    
    def __init__(self, request=None):
        
        """
        Inicializa una nueva instancia de la clase Cotizacion.

        Args:
            request (dict): Datos de la cotización.
        """

        super().__init__(request)
        self.client = APIClient()
        self.cliente = None
        self.items = []
    

    def get_endpoint(self):
        """
        Obtiene el endpoint específico de la cotización.

        args:
            None

        Returns:
            str: Endpoint de la cotización.
        """
        return 'Quotations'
    
    def validarDatosObligatorios(self):
        """
        Valida los datos obligatorios de la cotización.

        args:
            request (dict): Datos de la cotización.

        Raises:
            ValueError: Si faltan datos obligatorios.
        """
        super().validarDatosObligatorios()
        if not self.cliente or not self.items:
            raise ValueError("Faltan datos obligatorios para la cotización.")
    
        
    
    
    def validarDatosObligatorios(self, data, required_fields):
        """
        Valida que los datos obligatorios estén presentes en la solicitud.

        Args:
            data (dict): Datos de la solicitud.
            required_fields (list): Campos requeridos.

        Raises:
            ValueError: Si faltan campos requeridos en la solicitud.
        """
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")
    
    def construirFiltrosCotizaciones(data):
        """
        Construye los filtros para la consulta de cotizaciones basados en los datos proporcionados.

        Args:
            data (dict): Datos de la consulta.

        Returns:
            dict: Filtros para la consulta de cotizaciones.
        """

        filters = {}

        name = data.get('carData')
        name_mayus = name.upper() if name else None
        name_minus = name.lower() if name else None
        name_title = name.title() if name else None

        if data.get('fecha_doc'):
            filters['Quotations/DocDate ge'] = str(f"'{data.get('fecha_doc')}'")
            filters['Quotations/DocDate le'] = str(f"'{data.get('fecha_doc')}'")
        if data.get('fecha_inicio'):
            filters['Quotations/DocDate ge'] = str(f"'{data.get('fecha_inicio')}'")
        if data.get('fecha_fin'):
            filters['Quotations/DocDate le'] = str(f"'{data.get('fecha_fin')}'")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Quotations/DocNum,'] = f"{docum})"

        # Modificación para el filtro de CardName con múltiples opciones de formato
        # Mantener la lógica original para carData
        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(Quotations/CardCode,'] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['(contains(Quotations/CardName,'] = f"'{name_mayus}') or contains(Quotations/CardName, '{name_minus}') or contains(Quotations/CardName, '{name_title}'))"

        if data.get('salesEmployeeName'):
            numecode = int(data.get('salesEmployeeName'))
            filters['contains(SalesPersons/SalesEmployeeCode,'] = f"{numecode})" 
        
        if data.get('DocumentStatus'):
            document_status = data.get('DocumentStatus')

            if document_status == 'O':
                filters['Quotations/DocumentStatus eq'] = "'O'"
            elif document_status == 'C':
                filters['Quotations/DocumentStatus eq'] = "'C'"
                filters['Quotations/Cancelled eq'] = "'N'"
                
            else:
                filters['Quotations/Cancelled eq'] = "'Y'"

        if data.get('docTotal'):
            docTotal = float(data.get('docTotal'))
            filters['Quotations/DocTotal eq'] = f"{docTotal}"

        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters
        
    @staticmethod
    def buscarDocumentosCotizacion(doc_entry):
        """
        Busca los detalles de una cotización basada en el DocEntry.

        Args:
            doc_entry (str): DocEntry de la cotización.
        
        Returns:
            tuple: Líneas de documento de la cotización, mensaje de error.
        """
        try:
            client = APIClient() 
            data = client.obtenerCotizacionesDE('Quotations', doc_entry)

            if 'value' not in data:
                return None, 'No se encontraron datos de cotización'
            
            quotations = data['value']

            try:
                doc_entry_int = int(doc_entry)

            except ValueError:
                return None, f'El valor de DocEntry proporcionado ({doc_entry}) no es un número válido'
            
            # Filtramos las líneas de documento que coinciden con el DocEntry
            matching_lines = [
                q['Quotations/DocumentLines'] 
                for q in quotations 
                if q['Quotations/DocumentLines']['DocEntry'] == doc_entry_int
            ]

            if not matching_lines:
                return None, f'No se encontró la cotización con el DocEntry {doc_entry}'
            
            lines_data = Cotizacion.prepararLineasInternas(matching_lines)

            return lines_data, None

        except APIClient.ConnectionError as e:
            logger.error(f"Error de conexión al obtener detalles de la cotización: {str(e)}")
            return None, 'Error de conexión al servidor'
        except APIClient.TimeoutError as e:
            logger.error(f"Tiempo de espera agotado al obtener detalles de la cotización: {str(e)}")
            return None, 'Tiempo de espera agotado en la solicitud al servidor'
        except Exception as e:
            logger.error(f"Error inesperado al obtener detalles de la cotización: {str(e)}")
            return None, 'Error interno del servidor'


    @staticmethod
    def prepararLineasInternas(documentLines):
        """
        Prepara las líneas de documento de la cotización para ser mostradas en la vista de detalle.

        Args:
            documentLines (list): Líneas de documento de la cotización.

        Returns:
            list: Líneas de documento preparadas para ser mostradas en la vista de detalle.
        """
        return [
            {
                'docEntry': line.get('DocEntry'),
                'LineNum': line.get('LineNum'),
                'ItemCode': line.get('ItemCode'),
                'WarehouseCode': line.get('WarehouseCode'),
                'Quantity': line.get('Quantity'),
                'UnitPrice': line.get('UnitPrice'),
                "GrossPrice": line.get('GrossPrice'),
                "DiscountPercent": line.get('DiscountPercent'),
                "Price": line.get('Price'),
                "PriceAfterVAT": line.get('PriceAfterVAT'),
                "LineTotal": line.get('LineTotal'),
                "GrossTotal": line.get('GrossTotal'),
                "ShipDate": line.get('ShipDate'),
                "Address": line.get('Address'),
                "ShippingMethod": line.get('ShippingMethod'),
                "FreeText": line.get('FreeText'),
                "BaseType": line.get('BaseType'),
                "GrossBuyPrice": line.get('GrossBuyPrice'),
                "BaseEntry": line.get('BaseEntry'),
                "BaseLine": line.get('BaseLine'),
                "LineStatus": line.get('LineStatus'),
            }
            for line in documentLines
        ]
        

    def actualizarDocumento(self,docnum, docentry, data):
        
        docentry = docentry

        try:
            docentry = int(docentry)
            jsonData = SerializerDocument.document_serializer(data)
            print("jsonData", jsonData)
            #hay_receta = any(item.get('TreeType') == 'iSalesTree' for item in jsonData.get('DocumentLines', []))
            #if hay_receta:
            json_data = SerializerDocument.document_serializer(data)
            json_sin_linea_uno = json_data

            if json_sin_linea_uno['DocumentLines']:
                json_sin_linea_uno['DocumentLines'].clear()
                json_sin_linea_uno['DocumentLines'] = [{
                
                        "ItemCode": "LM",
                        "Quantity": 1,
                        "UnitPrice": 0,
                        "TreeType": "iNotATree"
                }]

                response = self.client.actualizarCotizacionesSL(docentry, json_sin_linea_uno)

            response = self.client.actualizarCotizacionesSL(docentry, jsonData)

            if 'success' in response:
                doc_num = docnum
                doc_entry = docentry
                # Guardar el log de la cotización

                rise = self.update_components(jsonData, doc_entry, type_document='Quotations')
                print("rise", rise)
                DocumentsLogs.register_logs(docNum=doc_num, docEntry=doc_entry, tipoDoc='Cotizacion', url="", json=jsonData, response=response, estate='Update')
                return {
                    'success': 'Cotización creada exitosamente',
                    'docNum': docnum,
                    'docEntry': docentry
                }

        except Exception as e:
            DocumentsLogs.register_logs(docNum=docnum, docEntry=docentry, tipoDoc='Cotizacion', url="", json=jsonData, response=response, estate='UpdateError')
            logger.error(f"Error al actualizar la cotización: {str(e)}")
            return {'error': str(e)}

    def crearDocumento(self, data):
        """
        Crea una nueva cotización y maneja las excepciones según el código de respuesta.

        Args:
            data (dict): Datos de la cotización.

        Returns:
            dict: Respuesta de la API.
        """
        try:
            # Verificar los datos antes de preparar el JSON
            errores = self.validarDatosCotizacion(data)
            if errores:
                return {'error': errores}

            # Preparar el JSON para la cotización
            jsonData = SerializerDocument.document_serializer(data)
            
            # Realizar la solicitud a la API
            response = self.client.crearCotizacionSL(self.get_endpoint(), jsonData)
            
            # Verificar si response es un diccionario
            if isinstance(response, dict):
                # Si contiene DocEntry, es un éxito
                if 'DocEntry' in response:
                    doc_num = response.get('DocNum')
                    doc_entry = response.get('DocEntry')
                    salesPersonCode = response.get('SalesPersonCode')
                    name_vendedor = VendedorRepository.obtenerNombreVendedor(salesPersonCode)
                    # Guardar el log de la cotización
                    self.update_components(response, doc_entry, type_document='Quotations')
    
                    DocumentsLogs.register_logs(docNum=doc_num, docEntry=doc_entry, tipoDoc='Cotizacion', url="", json=jsonData, response=response, estate='Create')
                    
                    return {
                        'success': 'Cotización creada exitosamente',
                        'docNum': doc_num,
                        'docEntry': doc_entry,
                        'salesPersonCode': salesPersonCode,
                        'salesPersonName': name_vendedor
                    }
                
                # Si contiene un mensaje de error, manejarlo
                elif 'error' in response:
                    DocumentsLogs.register_logs(docNum=None, docEntry=None, tipoDoc='Cotizacion', url="", json=jsonData, response=response, estate='CreateError')
                    error_message = response.get('error', 'Error desconocido')
                    return {'error': f"Error: {error_message}"}
                else:
                    return {'error': 'Respuesta inesperada de la API.'}
            
            else:
                return {'error': 'La respuesta de la API no es válida.'}
        
        except Exception as e:
            # Manejo de excepciones generales
            logger.error(f"Error al crear la cotización: {str(e)}")
            return {'error': str(e)}
    
    def update_components(self, data, doc_entry, type_document):
        document_line = data.get('DocumentLines')
        print("document_line", document_line)

        if 'TreeType' in document_line[0]:
            print("Enviando tarea para actualizar componentes...")
            try:
                return update_components_task.delay(doc_entry, type_document)
            except Exception as e:
                logger.error(f"Error al encolar la tarea de actualización de componentes: {str(e)}")
        
    def validarDatosCotizacion(self, data):
        """
        Verifica que los datos de la cotización sean correctos.

        Args:
            data (dict): Datos de la cotización.

        Returns:
            str: Mensajes de error si hay problemas con los datos, o vacío si son correctos.
        """
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

        if not data.get('DocDueDate'):
            errores.append("La fecha de vencimiento es obligatoria.")

        # Si hay errores, retornarlos como una cadena
        return ' '.join(errores)

    def eliminarDocumento(self, docEntry):
        """
        Elimina una cotización.

        Args:
            docEntry (str): DocEntry de la cotización a eliminar.

        Returns:
            dict: Respuesta de la API.
        """
        try:
            response = self.client.eliminarDocumentoSL(self.get_endpoint(), docEntry)
            return response
        except Exception as e:
            logger.error(f"Error al eliminar la cotización: {str(e)}")
            return {'error': str(e)}

    def actualizarEstadoDocumento(self, docNum, estado):
        """
        Actualiza el estado de una cotización.

        Args:
            docNum (str): Número de documento de la cotización.
            estado (str): Estado de la cotización.  
        
        Returns:
            dict: Respuesta de la API.
        """
        try:
            response = self.client.actualizarEstadoDocumentoSL(self.get_endpoint(), docNum, estado)
            return response
        except Exception as e:
            logger.error(f"Error al actualizar el estado de la cotización: {str(e)}")
            return {'error': str(e)}
        
    def formatearDatos(self, json_data):
        # Extraer y limpiar la información del cliente

        bodegas = ["ME", "LC", "PH"]

        client_info = json_data["Client"]["value"][0]
        quotations = client_info.get("Quotations", {})
        salesperson = client_info.get("SalesPersons", {})
        contact_employee = client_info.get("BusinessPartners/ContactEmployees", {})
        vendedor_repo = VendedorRepository()
        tipo_vendedor = vendedor_repo.obtenerTipoVendedor(salesperson.get("SalesEmployeeCode"))

        # Formatear los datos de cliente
        cliente = {
            "Quotations": {
                "DocEntry": quotations.get("DocEntry"),
                "DocNum": quotations.get("DocNum"),
                "CardCode": quotations.get("CardCode"),
                "CardName": quotations.get("CardName"),
                "TransportationCode": quotations.get("TransportationCode"),
                "Address": quotations.get("Address"),
                "Address2": quotations.get("Address2"),
                "DocDate": quotations.get("DocDate"),
                # si los comentarios son none se asigna un string vacio
                "Comments": quotations.get("Comments") if quotations.get("Comments") else "",
                "DocumentStatus": quotations.get("DocumentStatus"),
                "Cancelled": quotations.get("Cancelled"),
                "U_LED_TIPVTA": quotations.get("U_LED_TIPVTA"),
                "U_LED_TIPDOC": quotations.get("U_LED_TIPDOC"),
                "U_LED_NROPSH": quotations.get("U_LED_NROPSH"),
                "NumAtCard": quotations.get("NumAtCard"),
                "VatSum": quotations.get("VatSum"),
                "DocTotal": quotations.get("DocTotal"),
                "DocTotalNeto": quotations.get("DocTotalNeto"),
            },
            "SalesPersons": {
                "SalesEmployeeCode": salesperson.get("SalesEmployeeCode"),
                "SalesEmployeeName": salesperson.get("SalesEmployeeName"),
                "U_LED_SUCURS": salesperson.get("U_LED_SUCURS"),
            },
            "ContactEmployee": {
                "InternalCode": contact_employee.get("InternalCode") if contact_employee.get("InternalCode") else "No hay contactos disponibles",
                "FirstName": contact_employee.get("FirstName") if contact_employee.get("FirstName") else "No hay contactos disponibles",
            }
        }

        # Extraer y limpiar la información de líneas de documento
        document_lines = []
        for line_info in json_data["DocumentLine"]["value"]:
            line = line_info.get("Quotations/DocumentLines", {})
            warehouse_info = line_info.get("Items/ItemWarehouseInfoCollection", {})
            
            # obtener imagen por medio del codigo en la tabla de productos
            
            sku = line.get("ItemCode")
            bodega = line.get("WarehouseCode")
            if bodega not in bodegas:
                bodega = "ME"

            imagen = ProductoRepository.obtenerImagenProducto(sku)
            marca = ProductoRepository.obtenerMarcaProducto(sku)
            descuentoMax = ProductoRepository.descuentoMax(sku)
            priceList = ProductoRepository.obtenerPrecioLista(sku)

            

            stock_bodega = StockBodegasRepository.consultarStockPorBodega(sku, bodega)
            
            if tipo_vendedor == 'P':
                if marca == "LST":
                    descuentoMax =  math.floor(min(descuentoMax * 100, 25))
                else:
                    descuentoMax = math.floor(min(descuentoMax * 100, 15))
            else:
                if marca == "LST":
                    descuentoMax = math.floor(min(descuentoMax * 100, 15))
                else:
                    descuentoMax = math.floor(min(descuentoMax * 100, 10))
            
            # Construye la línea
            document_line = {
                "DocEntry": line.get("DocEntry"),
                "LineNum": line.get("LineNum"),
                "imagen": imagen,
                "ItemCode": line.get("ItemCode"),
                "ItemDescription": line.get("ItemDescription"),
                "WarehouseCode": line.get("WarehouseCode"),
                "Quantity": line.get("Quantity"),
                "UnitPrice": line.get("UnitPrice"),
                "GrossPrice": line.get("GrossPrice"),
                "DiscountPercent": line.get("DiscountPercent"),
                "Price": line.get("Price"),
                "PriceAfterVAT": line.get("PriceAfterVAT"),
                "LineTotal": line.get("LineTotal"),
                "GrossTotal": line.get("GrossTotal"),
                "ShipDate": line.get("ShipDate"),
                "Address": line.get("Address"),
                "ShippingMethod": line.get("ShippingMethod"),
                "FreeText": line.get("FreeText"),
                "BaseType": line.get("BaseType"),
                "GrossBuyPrice": line.get("GrossBuyPrice"),
                "BaseEntry": line.get("BaseEntry"),
                "BaseLine": line.get("BaseLine"),
                "LineStatus": line.get("LineStatus"),
                "DescuentoMax": descuentoMax,
                "PriceList": priceList,
                "StockBodega": stock_bodega,
                "WarehouseInfo": {
                    "WarehouseCode": warehouse_info.get("WarehouseCode"),
                    "InStock": warehouse_info.get("InStock"),
                    "Committed": warehouse_info.get("Committed"),
                    "SalesStock": warehouse_info.get("SalesStock"),
                }
            }
            
            # Agrega la línea solo si el Price es mayor a 0
            if document_line["Price"] and document_line["Price"] > 0:
                document_lines.append(document_line)


        # Formar el diccionario final
        resultado = {
            "Cliente": cliente,
            "DocumentLines": document_lines
        }

        return resultado

    def formataearDatosSoloLineas(self, json_data):
        document_lines = []
        for line_info in json_data["DocumentLine"]["value"]:
            line = line_info.get("Quotations/DocumentLines", {})
            warehouse_info = line_info.get("Items/ItemWarehouseInfoCollection", {})
            
            # Construye la línea
            document_line = {
                "DocEntry": line.get("DocEntry"),
                "LineNum": line.get("LineNum"),
                "ItemCode": line.get("ItemCode"),
                "ItemDescription": line.get("ItemDescription"),
                "WarehouseCode": line.get("WarehouseCode"),
                "Quantity": line.get("Quantity"),
                "UnitPrice": line.get("UnitPrice"),
                "GrossPrice": line.get("GrossPrice"),
                "DiscountPercent": line.get("DiscountPercent"),
                "Price": line.get("Price"),
                "PriceAfterVAT": line.get("PriceAfterVAT"),
                "LineTotal": line.get("LineTotal"),
                "GrossTotal": line.get("GrossTotal"),
                "ShipDate": line.get("ShipDate"),
                "Address": line.get("Address"),
                "ShippingMethod": line.get("ShippingMethod"),
                "FreeText": line.get("FreeText"),
                "BaseType": line.get("BaseType"),
                "GrossBuyPrice": line.get("GrossBuyPrice"),
                "BaseEntry": line.get("BaseEntry"),
                "BaseLine": line.get("BaseLine"),
                "LineStatus": line.get("LineStatus"),
                "WarehouseInfo": {
                    "WarehouseCode": warehouse_info.get("WarehouseCode"),
                    "InStock": warehouse_info.get("InStock"),
                    "Committed": warehouse_info.get("Committed"),
                    "SalesStock": warehouse_info.get("SalesStock"),
                }
            }
            
            # Agrega la línea solo si el Price es mayor a 0
            if document_line["Price"] and document_line["Price"] > 0:
                document_lines.append(document_line)

        return document_lines
    

    def reemplazarQuotationsPorOrders(self, formatear_datos_result):
        def replace_keys(data):
            if isinstance(data, dict):
                # Crear un nuevo diccionario con las claves modificadas
                return {
                    (key.replace("Quotations", "Orders") if "Quotations" in key else key): replace_keys(value)
                    for key, value in data.items()
                }
            elif isinstance(data, list):
                # Aplicar la función a cada elemento de la lista
                return [replace_keys(item) for item in data]
            else:
                # Devolver los valores que no sean dict ni list sin cambios
                return data

        # Reemplazar las claves en la estructura recibida
        return replace_keys(formatear_datos_result)
