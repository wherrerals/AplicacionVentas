import json
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from logicaVentasApp.services.documento import Documento
import logging
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
        prepararJsonCotizacion: Prepara los datos JSON específicos de la cotización.
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

        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(Quotations/CardCode,'] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['contains(Quotations/CardName,'] = f"'{car_data}')"

        if data.get('salesEmployeeName'):
            numecode = int(data.get('salesEmployeeName'))
            filters['contains(SalesPersons/SalesEmployeeCode,'] = f"{numecode})" 
        
        #if data.get('DocumentStatus'):
        #   filters['Quotations/DocumentStatus eq'] = f"'{data.get('DocumentStatus')}'"

        #if data.get('cancelled'):
        #    filters['Quotations/Cancelled eq'] = f"'{data.get('cancelled')}'"

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
    
    @staticmethod
    def tipoVentaTipoVendedor(codigo_vendedor):
        """
        Asigna el tipo de venta a la cotización.

        Args:
            tipo_venta (str): Tipo de venta.
        """
        repo = VendedorRepository()
        tipo_vendedor = repo.obtenerTipoVendedor(codigo_vendedor)

        if tipo_vendedor == 'PR':
            return 'PROY'
        elif tipo_vendedor == 'CD':
            return 'ECCO'
        else:
            return 'NA'

    @staticmethod
    def tipoVentaTipoLineas(lineas):
        """
        Asigna el tipo de venta a las líneas de la cotización.

        - Si todas las lineas son del mismo warehouse, se asigna el tipo de venta: TIEN.
        - Si las lineas son de diferentes warehouses, se asigna el tipo de venta: RESE.

        Args:
            lineas (list): Líneas de la cotización.
        """

        warehouses = set(linea.get('WarehouseCode') for linea in lineas)
        return 'TIEN' if len(warehouses) == 1 else 'RESE'
        

    def prepararJsonCotizacion(self, jsonData):
        """
        Prepara los datos JSON específicos de la cotización.

        Args:
            jsonData (dict): Datos de la cotización.
        
        Returns:
            dict: Datos de la cotización preparados para ser enviados a SAP.
        """
            
        # Determinar el tipo de venta basado en el vendedor
        codigo_vendedor = jsonData.get('SalesPersonCode')
        tipo_venta = self.tipoVentaTipoVendedor(codigo_vendedor)
        
        # Si el tipo de venta por vendedor no es válido ('NA'), determinar por líneas
        if tipo_venta == 'NA':
            lineas = jsonData.get('DocumentLines', [])
            tipo_venta = self.tipoVentaTipoLineas(lineas)
        
        #CAPTURAR ADDRES Y ADDRESS2 Y CONSULTAR LA BASE DE DATOS PARA CONCATENAR DIRECCION, COMUNA.nombre /R CIUDAD /R REGION.nombre
        
        adrres = jsonData.get('Address')
        adrres2 = jsonData.get('Address2')
        
        #consultar en base de datos con el id capturado
        
        
        direccion1 = DireccionRepository.obtenerDireccion(adrres)
        direccionRepo2 = DireccionRepository.obtenerDireccion(adrres2)
        
        addresmodif = f"{direccion1.calleNumero} {direccion1.comuna.nombre}\n{direccion1.ciudad}\n{direccion1.region.nombre}"
        addresmodif2 = f"{direccionRepo2.calleNumero} {direccionRepo2.comuna.nombre}\n{direccionRepo2.ciudad}\n{direccionRepo2.region.nombre}"
        
        # Datos de la cabecera
        cabecera = {
            'DocDate': jsonData.get('DocDate'),
            'DocDueDate': jsonData.get('DocDueDate'),
            'TaxDate': jsonData.get('TaxDate'),
            'Address': addresmodif,
            'Address2': addresmodif2,
            'CardCode': jsonData.get('CardCode'),
            'NumAtCard': jsonData.get('NumAtCard'),
            'Comments': jsonData.get('Comments'),
            'PaymentGroupCode': jsonData.get('PaymentGroupCode'),
            'SalesPersonCode': jsonData.get('SalesPersonCode'),
            'TransportationCode': jsonData.get('TransportationCode'),
            #'U_LED_NROPSH': jsonData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': tipo_venta,  # Tipo de venta calculado
            'U_LED_TIPDOC': jsonData.get('U_LED_TIPDOC'), # Tipo de documento boleta o factura
            'U_LED_FORENV': jsonData.get('TransportationCode'), # Forma de envio de la cotización
        }

        # Datos de las líneas
        lineas = jsonData.get('DocumentLines', [])
        lineas_json = [
            {
                'lineNum': linea.get('LineNum'),
                'ItemCode': linea.get('ItemCode'),
                'Quantity': linea.get('Quantity'),
                'ShipDate': linea.get('ShipDate'),
                'FreeText': linea.get('FreeText'),
                'DiscountPercent': linea.get('DiscountPercent'),
                'WarehouseCode': linea.get('WarehouseCode'),
                'CostingCode': linea.get('CostingCode'),
                'ShippingMethod': linea.get('ShippingMethod'),
                'COGSCostingCode': linea.get('COGSCostingCode'),
                'CostingCode2': linea.get('CostingCode2'),
                'COGSCostingCode2': linea.get('COGSCostingCode2'),
            }
            for linea in lineas
        ]

        # Combina cabecera y líneas en un solo diccionario
        return {
            **cabecera,
            'DocumentLines': lineas_json,
        }
    
    def prepararJsonCotizacionAC(self, jsonData):
        """
        Prepara los datos JSON específicos de la cotización.

        Args:
            jsonData (dict): Datos de la cotización.
        
        Returns:
            dict: Datos de la cotización preparados para ser enviados a SAP.
        """

        codigo_vendedor = jsonData.get('SalesPersonCode')
        tipo_venta = self.tipoVentaTipoVendedor(codigo_vendedor)

        if tipo_venta == 'NA':
            lineas = jsonData.get('DocumentLines', [])
            tipo_venta = self.tipoVentaTipoLineas(lineas)

        #CAPTURAR ADDRES Y ADDRESS2 Y CONSULTAR LA BASE DE DATOS PARA CONCATENAR DIRECCION, COMUNA.nombre /R CIUDAD /R REGION.nombre
        
        adrres = jsonData.get('Address')
        adrres2 = jsonData.get('Address2')
        
        #consultar en base de datos con el id capturado
        
        
        direccion1 = DireccionRepository.obtenerDireccion(adrres)
        direccionRepo2 = DireccionRepository.obtenerDireccion(adrres2)
        
        addresmodif = f"{direccion1.calleNumero} {direccion1.comuna.nombre}\n{direccion1.ciudad}\n{direccion1.region.nombre}"
        addresmodif2 = f"{direccionRepo2.calleNumero} {direccionRepo2.comuna.nombre}\n{direccionRepo2.ciudad}\n{direccionRepo2.region.nombre}"
        
      
        cabecera = {
            'DocDate': jsonData.get('DocDate'),
            'DocDueDate': jsonData.get('DocDueDate'),
            'TaxDate': jsonData.get('TaxDate'),
            'Address': addresmodif,
            'Address2': addresmodif2,
            'CardCode': jsonData.get('CardCode'),
            'NumAtCard': jsonData.get('NumAtCard'),
            'Comments': jsonData.get('Comments'),
            'PaymentGroupCode': jsonData.get('PaymentGroupCode'),
            'SalesPersonCode': jsonData.get('SalesPersonCode'),
            'TransportationCode': jsonData.get('TransportationCode'),
            #'U_LED_NROPSH': jsonData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': tipo_venta,  # Tipo de venta calculado
            'U_LED_TIPDOC': jsonData.get('U_LED_TIPDOC'), # Tipo de documento boleta o factura
            'U_LED_FORENV': jsonData.get('TransportationCode'), # Forma de envio de la cotización
        }

        # Datos de las líneas
        lineas = jsonData.get('DocumentLines', [])
        lineas_json = [
            {
                'lineNum': linea.get('LineNum'),
                'ItemCode': linea.get('ItemCode'),
                'Quantity': linea.get('Quantity'),
                'ShipDate': linea.get('ShipDate'),
                'FreeText': linea.get('FreeText'),
                'DiscountPercent': linea.get('DiscountPercent'),
                'WarehouseCode': linea.get('WarehouseCode'),
                'CostingCode': linea.get('CostingCode'),
                'ShippingMethod': linea.get('ShippingMethod'),
                'COGSCostingCode': linea.get('COGSCostingCode'),
                'CostingCode2': linea.get('CostingCode2'),
                'COGSCostingCode2': linea.get('COGSCostingCode2'),
            }
            for linea in lineas
        ]

        # Combina cabecera y líneas en un solo diccionario
        return {
            **cabecera,
            'DocumentLines': lineas_json,
        }

    def actualizarDocumento(self,docnum, docentry, data):
        
        docentry = docentry

        try:
            docentry = int(docentry)
            jsonData = self.prepararJsonCotizacionAC(data)
            
            response = self.client.actualizarCotizacionesSL(docentry, jsonData)

            if 'success' in response:
                return {
                    'success': 'Cotización creada exitosamente',
                    'docNum': docnum,
                    'docEntry': docentry
                }

        
        except Exception as e:
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
            jsonData = self.prepararJsonCotizacion(data)
            
            # Realizar la solicitud a la API
            response = self.client.crearCotizacionSL(self.get_endpoint(), jsonData)
            
            # Verificar si response es un diccionario
            if isinstance(response, dict):
                # Si contiene DocEntry, es un éxito
                if 'DocEntry' in response:
                    doc_num = response.get('DocNum')
                    doc_entry = response.get('DocEntry')
                    return {
                        'success': 'Cotización creada exitosamente',
                        'docNum': doc_num,
                        'docEntry': doc_entry

                    }
                
                # Si contiene un mensaje de error, manejarlo
                elif 'error' in response:
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
        print("Actualizando estado de la cotización...")
        try:
            response = self.client.actualizarEstadoDocumentoSL(self.get_endpoint(), docNum, estado)
            return response
        except Exception as e:
            logger.error(f"Error al actualizar el estado de la cotización: {str(e)}")
            return {'error': str(e)}
        
    def formatearDatos(self, json_data):
        # Extraer y limpiar la información del cliente
        client_info = json_data["Client"]["value"][0]
        quotations = client_info.get("Quotations", {})
        salesperson = client_info.get("SalesPersons", {})
        contact_employee = client_info.get("BusinessPartners/ContactEmployees", {})

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
                "InternalCode": contact_employee.get("InternalCode"),
                "FirstName": contact_employee.get("FirstName"),
            }
        }

        # Extraer y limpiar la información de líneas de documento
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