from datosLsApp.repositories.productorepository import ProductoRepository
from logicaVentasApp.services.documento import Documento


class SolicitudesDevolucion(Documento):

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
        print(name_mayus)
        name_minus = name.lower() if name else None
        print(name_minus)
        name_title = name.title() if name else None
        print(name_title)

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

        print(f"DATOS: {json_data}")

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

        print(f"RESULTADO: {resultado}")

        return resultado