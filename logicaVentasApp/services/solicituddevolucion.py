from venv import logger
from adapters.sl_client import APIClient
from datosLsApp.models.documentodb import DocumentoDB
from datosLsApp.models.lineadb import LineaDB
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.documentorepository import DocumentoRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from datosLsApp.serializer.documentSerializer import SerializerDocument
from datosLsApp.serializer.returnRequestSerializer import RertunrRequestSerializer
from logicaVentasApp.services.documento import Documento


class SolicitudesDevolucion(Documento):

    def __init__(self, request=None):

        super().__init__(request)
        self.client = APIClient()
        self.cliente = None
        self.items = []

    def get_endpoint(self):

        return 'ReturnRequest'

    def construirSolicitudesDevolucion(data):
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

        if data.get('carData'):
            car_data = data.get('carData')
            car_data = car_data.replace("C", "").replace('c', '').strip()
            
            if car_data.isdigit(): 
                filters['contains(ReturnRequest/CardCode,'] = f"'{car_data}')"
            else:
                filters['(contains(ReturnRequest/CardName,'] = f"'{name_mayus}') or contains(ReturnRequest/CardName, '{name_minus}') or contains(ReturnRequest/CardName, '{name_title}'))"

        if data.get('salesEmployeeName'):
            value = data.get('salesEmployeeName')
            
            if str(value).isdigit():
                filters['contains(SalesPersons/SalesEmployeeCode,'] = f"{value})" 
            else:
                filters['contains(SalesPersons/SalesEmployeeName,'] = f"'{value}')"
        
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

        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters
    

    def formatearDatos(self, json_data):

        client_info = json_data["Client"]["value"][0]
        quotations = client_info.get("ReturnRequest", {})
        salesperson = client_info.get("SalesPersons", {})
        contact_employee = client_info.get("BusinessPartners/ContactEmployees", {})

        cliente = {
            "ReturnRequest": {
                "DocEntry": quotations.get("DocEntry"),
                "DocNum": quotations.get("DocNum"),
                "U_VK_Folio": quotations.get("U_VK_Folio"),
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
                "U_LED_TIPDEV": quotations.get("U_LED_TIPDEV"),
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

        resultado = {
            "Cliente": cliente,
            "DocumentLines": document_lines
        }
        
        return resultado

    def actualizarDocumento(self, docnum, docentry, data):
        docentry = docentry

        try:
            docentry = int(docentry)
            jsonData = RertunrRequestSerializer.document_serializer2(data)
            json_lineas_ok = self.elimnar_lineas_no_check(jsonData)

            response = self.client.actualizarDevolucionesSL(docentry, json_lineas_ok)

            if 'success' in response:
                return {
                    'success': True,
                    'title': 'Solicitud de Devolución Actualizada en SAP',
                    'message': f'Solicitud Devolución Actualizada exitosamente. N°: {docnum}',
                    'docNum': docnum,
                    'docEntry': docentry
                }
        
        except Exception as e:
            logger.error(f"Error al actualizar la cotización: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def validar_check(data):
        errores = []
        for item in data.get('DocumentLines', []):
            #validar que almenos una de las lineas tenga marcado el EstadoCheck
            if item.get('EstadoCheck'):
                errores.append("Debe marcar al menos un producto para la devolucion.")
        return ' '.join(errores)


    def elimnar_lineas_no_check(self, data):

        lineas_filtradas = [
            linea for linea in data.get('DocumentLines', [])
            if linea.get('EstadoCheck') != 0
        ]

        data['DocumentLines'] = lineas_filtradas

        return data

    def crearDocumento(self, data):

        try:
            errores = self.validarDatosCotizacion(data)
            if errores:
                return {'error': errores}

            jsonData = RertunrRequestSerializer.document_serializer2(data)
            json_lineas_ok = self.elimnar_lineas_no_check(jsonData)
            response = self.client.crearCotizacionSL(self.get_endpoint(), json_lineas_ok)
            
            if isinstance(response, dict):
                if 'DocEntry' in response:
                    doc_num = response.get('DocNum')
                    doc_entry = response.get('DocEntry')
                    salesPersonCode = response.get('SalesPersonCode')
                    name_vendedor = VendedorRepository.obtenerNombreVendedor(salesPersonCode)

                    return {
                        'success': True,
                        'title': 'Solicitud de Devolución creada',
                        'message': f'Solicitud de Devolución creada exitosamente. N°: {doc_num}',
                        'docNum': doc_num,
                        'docEntry': doc_entry,
                        'salesPersonCode': salesPersonCode,
                        'salesPersonName': name_vendedor
                    }
                
                elif 'error' in response:
                    error_message = response.get('error', 'Error desconocido')
                    return {'error': f"Error: {error_message}"}
                else:
                    return {'error': 'Respuesta inesperada de la API.'}
            
            else:
                return {'error': 'La respuesta de la API no es válida.'}
        
        except Exception as e:
            logger.error(f"{str(e)}")
            return {'error': str(e)}

    def validarDatosCotizacion(self, data):

        errores = []

        if not data.get('CardCode'):
            errores.append("No se a ingresado cliente para la Cotizacion.")

        if not data.get('DocumentLines'):
            errores.append("La cotización debe tener al menos una línea de documento.")

        for item in data.get('DocumentLines', []):
            cantidad = item.get('Quantity', 0)
            if cantidad <= 0:
                errores.append(f"La cantidad del artículo {item.get('ItemCode')} debe ser mayor a cero.")

        return ' '.join(errores)

    @staticmethod
    def tipoVentaTipoVendedor(codigo_vendedor):

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

        warehouses = set(linea.get('WarehouseCode') for linea in lineas)
        return 'TIEN' if len(warehouses) == 1 else 'RESE'

    @staticmethod
    def validar_lineas_documento(data):
        """
        data = {
            "docEntry_relacionado": int,
            "DocumentLines": [
                {
                    "producto_id": int,
                    "numLinea": int,
                    "cantidad": int,
                    "EstadoCheck": int,
                    ...
                },
                ...
            ]
        }
        """

        print("Validando líneas del documento...")

        errores = []

        doc_entry_relacionado = data.get('RefDocEntr')
        if not doc_entry_relacionado:
            errores.append("No se proporcionó docEntry_relacionado.")
            return {"errores": errores}

        try:
            documento = DocumentoDB.objects.filter(docEntry_relacionado=doc_entry_relacionado).first()
        except DocumentoDB.DoesNotExist:
            errores.append(f"No existe un documento relacionado con docEntry {doc_entry_relacionado}.")
            return {"errores": errores}

        lineas_doc = LineaDB.objects.filter(documento=documento)

        # Validar cada línea enviada vs base
        lineas_enviadas = data.get('DocumentLines', [])

        # Validar que todas las líneas estén marcadas como check y cantidades coherentes
        for linea in lineas_enviadas:
            if linea.get('EstadoCheck') != 1:
                errores.append(f"La línea {linea.get('LineNum')} no está marcada como seleccionada.")

            cantidad_enviada = linea.get('Quantity', 0)

            try:
                linea_db = lineas_doc.get(producto=linea.get('ItemCode'))
                if cantidad_enviada > linea_db.cantidad:
                    errores.append(
                        f"Cantidad enviada ({cantidad_enviada}) es mayor que la cantidad original "
                        f"({linea_db.cantidad_solicitada}) para la ItemCode {linea.get('ItemCode')}"
                    )
            except LineaDB.DoesNotExist:
                errores.append(f"La línea {linea.get('ItemCode')} no existe en el documento.")

        # Validar si las líneas son exactamente iguales (producto, numLinea, cantidad)
        # Genera set DB: solo las líneas con estado_devolucion == 1
        lineas_db_set = set(
            (
                l.producto.codigo,
                str(l.numLineaBase),
                l.cantidad,
                )
            for l in lineas_doc
        )

        # Genera set Enviado: solo líneas con EstadoCheck == 1
        lineas_enviadas_set = set(
            (
                l.get('ItemCode'),
                str(l.get('LineNum')),
                l.get('Quantity'),
            )
            for l in lineas_enviadas if l.get('EstadoCheck') == 1
        )

        print(f"Líneas DB filtradas: {lineas_db_set}")
        print(f"Líneas Enviadas filtradas: {lineas_enviadas_set}")

        # Validación final: solo OK si todo coincide y todos cumplen condición de ambos en 1
        if lineas_enviadas_set == lineas_db_set:
            return {
                "resultado": True,
                "DoctotalBase": documento.DoctotalBase
            }
        else:
            print("Errores de validación:", errores)
            return None

