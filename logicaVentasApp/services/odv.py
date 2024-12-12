import json
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
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
            document_lines.append(document_line)

        # Formar el diccionario final
        resultado = {
            "Cliente": cliente,
            "DocumentLines": document_lines
        }

        return resultado
