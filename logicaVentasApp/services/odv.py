import json
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from logicaVentasApp.services.documento import Documento
import logging
logger = logging.getLogger(__name__)

class OrdenVenta(Documento):


    def construirFiltrosODV(data):

        """
        Construye los filtros para la consulta de cotizaciones basados en los datos proporcionados.

        Args:
            data (dict): Datos de la consulta.

        Returns:
            dict: Filtros para la consulta de cotizaciones.
        """

        filters = {}

        if data.get('fecha_doc'):
            filters['Orders/DocDate ge'] = str(f"'{data.get('fecha_doc')}'")
            filters['Orders/DocDate le'] = str(f"'{data.get('fecha_doc')}'")
        if data.get('fecha_inicio'):
            filters['Orders/DocDate ge'] = str(f"'{data.get('fecha_inicio')}'")
        if data.get('fecha_fin'):
            filters['Orders/DocDate le'] = str(f"'{data.get('fecha_fin')}'")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Orders/DocNum,'] = f"{docum})"

        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(Orders/CardCode,'] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['contains(Orders/CardName,'] = f"'{car_data}')"

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
                filters['Orders/DocumentStatus eq'] = "'O'"
            elif document_status == 'C':
                filters['Orders/DocumentStatus eq'] = "'C'"
                filters['Orders/Cancelled eq'] = "'N'"
                
            else:
                filters['Orders/Cancelled eq'] = "'Y'"

        if data.get('docTotal'):
            docTotal = float(data.get('docTotal'))
            filters['Orders/DocTotal eq'] = f"{docTotal}"


        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters

    def formatearDatos(self, json_data):
        # Extraer y limpiar la información del cliente

        print("JSON DATA:", json_data)
        client_info = json_data["Client"]["value"][0]
        quotations = client_info.get("Orders", {})
        salesperson = client_info.get("SalesPersons", {})
        contact_employee = client_info.get("BusinessPartners/ContactEmployees", {})

        # Formatear los datos de cliente
        cliente = {
            "Orders": {
                "DocEntry": quotations.get("DocEntry"),
                "DocNum": quotations.get("DocNum"),
                "CardCode": quotations.get("CardCode"),
                "CardName": quotations.get("CardName"),
                "TransportationCode": quotations.get("TransportationCode"),
                "Address": quotations.get("Address"),
                "Address2": quotations.get("Address2"),
                "DocDate": quotations.get("DocDate"),
                "DocDueDate": quotations.get("DocDueDate"),
                "Comments": quotations.get("Comments"),
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
            line = line_info.get("Orders/DocumentLines", {})
            warehouse_info = line_info.get("Items/ItemWarehouseInfoCollection", {})
            
            sku = line.get("ItemCode")
            
            imagen = ProductoRepository.obtenerImagenProducto(sku)
            
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
                "ShipDate": str(line.get("ShipDate")),
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
            document_lines.append(document_line)

        # Formar el diccionario final
        resultado = {
            "Cliente": cliente,
            "DocumentLines": document_lines
        }

        return resultado

    def actualizarDocumento(self,docnum, docentry, data):
        
        docentry = docentry

        try:
            docentry = int(docentry)
            jsonData = self.prepararJsonODV(data)
            
            client = APIClient()

            response = client.actualizarODVSL(docentry, jsonData)

            if 'success' in response:
                return {
                    'success': 'Orden Venta creada exitosamente',
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
        print("Creando documento")

        try:
            # Verificar los datos antes de preparar el JSON
            errores = self.validarDatosODV(data)
            if errores:
                return {'error': errores}

            # Preparar el JSON para la cotización
            jsonData = self.prepararJsonODV(data)

            sl = APIClient()
            
            # Realizar la solicitud a la API
            response = sl.crearODV(jsonData)
            
            # Verificar si response es un diccionario
            if isinstance(response, dict):
                # Si contiene DocEntry, es un éxito
                if 'DocEntry' in response:
                    doc_num = response.get('DocNum')
                    doc_entry = response.get('DocEntry')
                    return {
                        'success': 'Orden Venta creada exitosamente',
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

    def validarDatosODV(self, data):
        """
        Verifica que los datos de la cotización sean correctos.

        Args:
            data (dict): Datos de la cotización.

        Returns:
            str: Mensajes de error si hay problemas con los datos, o vacío si son correctos.
        """
        print(f"Validando datos: {data}")
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
    
    def prepararJsonODV(self, jsonData):

        codigo_vendedor = jsonData.get('SalesPersonCode')
        tipo_venta = self.tipoVentaTipoVendedor(codigo_vendedor)
        
        if tipo_venta == 'NA':
            lineas = jsonData.get('DocumentLines', [])
            tipo_venta = self.tipoVentaTipoLineas(lineas)
            
            
        adrres = jsonData.get('Address')
        adrres2 = jsonData.get('Address2')
        
        idContacto = jsonData.get('ContactPersonCode')
        
        contacto = ContactoRepository.obtenerContacto(idContacto)
        numerocontactoSAp = contacto.codigoInternoSap
        
        direccion1 = DireccionRepository.obtenerDireccion(adrres)
        direccionRepo2 = DireccionRepository.obtenerDireccion(adrres2)
        
        addresmodif = f"{direccion1.calleNumero} {direccion1.comuna.nombre}\n{direccion1.ciudad}\n{direccion1.region.nombre}"
        addresmodif2 = f"{direccionRepo2.calleNumero} {direccionRepo2.comuna.nombre}\n{direccionRepo2.ciudad}\n{direccionRepo2.region.nombre}"


        
        # Datos de la cabecera
        cabecera = {
            'DocDate': jsonData.get('DocDate'),
            'DocDueDate': jsonData.get('DocDueDate'),
            'TaxDate': jsonData.get('TaxDate'),
            'ContactPersonCode': numerocontactoSAp,
            'Address': addresmodif,
            'Address2': addresmodif2,
            'CardCode': jsonData.get('CardCode'),
            'NumAtCard': jsonData.get('NumAtCard'),
            'Comments': jsonData.get('Comments'),
            'PaymentGroupCode': jsonData.get('PaymentGroupCode'),
            'SalesPersonCode': jsonData.get('SalesPersonCode'),
            'TransportationCode': jsonData.get('TransportationCode'),
            #'U_LED_NROPSH': jsonData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': tipo_venta,
            'U_LED_TIPDOC': jsonData.get('U_LED_TIPDOC'),
            'U_LED_FORENV': jsonData.get('TransportationCode'),
        }

        # Datos de las líneas
        lineas = jsonData.get('DocumentLines', [])
        
        #lineas = self.ajustarShippingMethod(lineas)
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

        return {
            **cabecera,
            'DocumentLines': lineas_json,
        }

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
        
        shipping_methods = set(linea.get('ShippingMethod') for linea in lineas)
        warehouses = set(linea.get('WarehouseCode') for linea in lineas)
        
        if len(shipping_methods) and len(warehouses) == 1:
            return 'TIEN'
        else:
            return 'RESE'
""" 
    @staticmethod
    def ajustarShippingMethod(lineas):

        for linea in lineas:
            shipping_method = linea.get('ShippingMethod')
            warehouse_code = linea.get('WarehouseCode')

            # Regla para ShippingMethod
            if shipping_method == "2":
                if warehouse_code == "LC":
                    linea['ShippingMethod'] = "3"
                elif warehouse_code == "ME":
                    linea['ShippingMethod'] = "2"
                elif warehouse_code == "PH":
                    linea['ShippingMethod'] = "4"

        return lineas """