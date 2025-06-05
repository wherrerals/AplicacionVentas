from venv import logger
from adapters.sl_client import APIClient
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.documentorepository import DocumentoRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from logicaVentasApp.services.documento import Documento


class SolicitudesDevolucion(Documento):

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
        return 'ReturnRequest'

    def construirSolicitudesDevolucion(data):
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
            filters['ReturnRequest/DocDate ge'] = str(f"'{data.get('fecha_doc')}'")
            filters['ReturnRequest/DocDate le'] = str(f"'{data.get('fecha_doc')}'")
        if data.get('fecha_inicio'):
            filters['ReturnRequest/DocDate ge'] = str(f"'{data.get('fecha_inicio')}'")
        if data.get('fecha_fin'):
            filters['ReturnRequest/DocDate le'] = str(f"'{data.get('fecha_fin')}'")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(ReturnRequest/DocNum,'] = f"{docum})"

        # Modificación para el filtro de CardName con múltiples opciones de formato
        # Mantener la lógica original para carData
        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(ReturnRequest/CardCode,'] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['(contains(ReturnRequest/CardName,'] = f"'{name_mayus}') or contains(ReturnRequest/CardName, '{name_minus}') or contains(ReturnRequest/CardName, '{name_title}'))"

        if data.get('salesEmployeeName'):
            numecode = int(data.get('salesEmployeeName'))
            filters['contains(SalesPersons/SalesEmployeeCode,'] = f"{numecode})" 
        
        if data.get('DocumentStatus'):
            document_status = data.get('DocumentStatus')

            if document_status == 'O':
                filters['ReturnRequest/DocumentStatus eq'] = "'O'"
            elif document_status == 'C':
                filters['ReturnRequest/DocumentStatus eq'] = "'C'"
                filters['ReturnRequest/Cancelled eq'] = "'N'"
                
            else:
                filters['ReturnRequest/Cancelled eq'] = "'Y'"

        if data.get('docTotal'):
            docTotal = float(data.get('docTotal'))
            filters['ReturnRequest/DocTotal eq'] = f"{docTotal}"

        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters
    
    def detallesOrdenVentaLineas(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(ReturnRequest,ReturnRequest/DocumentLines,Items/ItemWarehouseInfoCollection)?$expand=ReturnRequest/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)
        &$filter=ReturnRequest/DocEntry eq 201882 and ReturnRequest/DocumentLines/DocEntry eq ReturnRequest/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq ReturnRequest/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq ReturnRequest/DocumentLines/WarehouseCode
        """

        crossJoin = (
            "ReturnRequest,ReturnRequest/DocumentLines,Items/ItemWarehouseInfoCollection"
            )
        
        expand = "ReturnRequest/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"
        filter = f"ReturnRequest/DocEntry eq {docEntry} and ReturnRequest/DocumentLines/DocEntry eq ReturnRequest/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq ReturnRequest/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq ReturnRequest/DocumentLines/WarehouseCode"

        base_url = self.base_url # Asegura que no haya doble "/"
        url = f"{base_url}/$crossjoin({crossJoin})?$expand={expand}&$filter={filter}"

        all_data = []  # Lista para almacenar todos los valores

        while url:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            # Agregar los resultados actuales a la lista acumulada
            all_data.extend(data.get("value", []))

            # Obtener el próximo enlace si existe
            next_link = data.get("odata.nextLink")
            url = f"{base_url}/{next_link}" if next_link else None  # Agregar base_url si es necesario

        return {"value": all_data}
    
    def formatearDatos(self, json_data):
        # Extraer y limpiar la información del cliente

        client_info = json_data["Client"]["value"][0]
        quotations = client_info.get("ReturnRequest", {})
        salesperson = client_info.get("SalesPersons", {})
        contact_employee = client_info.get("BusinessPartners/ContactEmployees", {})

        # Formatear los datos de cliente
        cliente = {
            "ReturnRequest": {
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
            line = line_info.get("ReturnRequest/DocumentLines", {})
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

    def prepararJsonDevoluciones(self, jsonData):
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
            tipo_venta = self.Sale_type_line_type(lineas)
        
        transportationCode = jsonData.get('TransportationCode')

        if tipo_venta == 'NA' and transportationCode != '1':
            tipo_venta = 'RESE'
        elif tipo_venta == 'PROY':
            tipo_venta = 'PROY'
        elif tipo_venta == 'ECCO':
            tipo_venta = 'ECCO'
                    
        adrres = jsonData.get('Address')
        adrres2 = jsonData.get('Address2')
        
        idContacto = jsonData.get('ContactPersonCode')
        
        if idContacto == "No hay contactos disponibles":
            numerocontactoSAp = "null"
        else:
            contacto = ContactoRepository.obtenerContacto(idContacto)
            numerocontactoSAp = contacto.codigoInternoSap        #consultar en base de datos con el id capturado
        

        
        if adrres == "No hay direcciones disponibles":
            addresmodif = "null"
        else:
            direccion1 = DireccionRepository.obtenerDireccion(adrres)
            addresmodif = f"{direccion1.calleNumero}, {direccion1.comuna.nombre}\n{direccion1.ciudad}\n{direccion1.region.nombre}"

        if adrres2 == "No hay direcciones disponibles":
            addresmodif2 = "null"
        else:
            direccionRepo2 = DireccionRepository.obtenerDireccion(adrres2)
            addresmodif2 = f"{direccionRepo2.calleNumero}, {direccionRepo2.comuna.nombre}\n{direccionRepo2.ciudad}\n{direccionRepo2.region.nombre}"
        
        # Datos de la cabecera
        cabecera = {
            'DocDate': jsonData.get('DocDate'),
            #'DocDueDate': jsonData.get('DocDueDate'),
            'TaxDate': jsonData.get('TaxDate'),
            'DocTotal': jsonData.get('DocTotal'),
            #'ContactPersonCode': numerocontactoSAp,
            #'Address': addresmodif,
            #'Address2': addresmodif2,
            'CardCode': jsonData.get('CardCode'),
            'NumAtCard': jsonData.get('NumAtCard'),
            'Comments': jsonData.get('Comments'),
            'PaymentGroupCode': jsonData.get('PaymentGroupCode'),
            'SalesPersonCode': jsonData.get('SalesPersonCode'),
            'TransportationCode': jsonData.get('TransportationCode'),
            #'U_LED_NROPSH': jsonData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': tipo_venta,  # Tipo de venta calculado
            'U_LED_TIPDOC': jsonData.get('U_LED_TIPDOC'),
            'U_LED_FORENV': jsonData.get('TransportationCode'),
        }

        # Datos de las líneas
        lineas = jsonData.get('DocumentLines', [])

        repo_producto = ProductoRepository()
        
        #maper item code


        lineas_json = [
            
            {
                'lineNum': linea.get('LineNum'),
                'ItemCode': linea.get('ItemCode'),
                'Quantity': linea.get('Quantity'),
                #'PriceAfVAT': repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')),
                #'GrossPrice': repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')),
                'UnitPrice': repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')),
                #'NetTaxAmount': repo_producto.obtener_precio_unitario_bruto(linea.get('ItemCode')) * linea.get('Quantity') - repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')) * linea.get('Quantity'),
                #'TaxTotal': repo_producto.obtener_precio_unitario_bruto(linea.get('ItemCode')) * linea.get('Quantity') - repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')) * linea.get('Quantity'),
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

        taxExtension = {
            "StreetS": direccion1.calleNumero,
            "CityS": direccion1.ciudad,
            "CountyS": f"{direccion1.comuna.codigo} - {direccion1.comuna.nombre}",
            "StateS": direccion1.region.numero,
            "CountryS": "CL",
            "StreetB": direccionRepo2.calleNumero,
            "CityB": direccionRepo2.ciudad,
            "CountyB": f"{direccionRepo2.comuna.codigo} - {direccionRepo2.comuna.nombre}",
            "StateB": direccionRepo2.region.numero,
            "CountryB": "CL",
        } 

        return {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }

    def actualizarDocumento(self,docnum, docentry, data):
        docentry = docentry

        try:
            docentry = int(docentry)
            jsonData = self.prepararJsonDevoluciones(data)
            response = self.client.actualizarDevolucionesSL(docentry, jsonData)

            if 'success' in response:
                return {
                    'success': 'Devolución creada exitosamente',
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
            print(f"Datos de la cotización: {data}")  # Para depuración

            # Verificar los datos antes de preparar el JSON
            errores = self.validarDatosCotizacion(data)
            if errores:
                return {'error': errores}

            # Preparar el JSON para la cotización
            jsonData = self.prepararJsonDevoluciones(data)

            DocumentoRepository.create_document_db(jsonData)  # Guardar en la base de datos

            print(f"JSON Data: {jsonData}")  # Para depuración

            return True
            
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
                    return {
                        'success': 'Devolución creada exitosamente',
                        'docNum': doc_num,
                        'docEntry': doc_entry,
                        'salesPersonCode': salesPersonCode,
                        'salesPersonName': name_vendedor
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

        # Si hay errores, retornarlos como una cadena
        return ' '.join(errores)

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
    def Sale_type_line_type(lineas):
        """
        Asigna el tipo de venta a las líneas de la cotización.

        - Si todas las lineas son del mismo warehouse, se asigna el tipo de venta: TIEN.
        - Si las lineas son de diferentes warehouses, se asigna el tipo de venta: RESE.

        Args:
            lineas (list): Líneas de la cotización.
        """

        warehouses = set(linea.get('WarehouseCode') for linea in lineas)
        return 'TIEN' if len(warehouses) == 1 else 'RESE'