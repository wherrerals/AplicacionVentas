import math
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from logicaVentasApp.services.trasportation import Trasnportation
from logicaVentasApp.services.typeofsale import TypeOfSale
import re

class InvoiceSerializer:

    @staticmethod
    def serializer_sales(data):
        if not data or 'value' not in data or not data['value']:
            return {}
        
        serialized_data = []

        for data_sales in data['value']:
            main_key = next(iter(data_sales))
            document_data = data_sales[main_key]
            sales_person = data_sales.get('SalesPersons', {})

            serialized_data.append({
                "DocEntry": document_data.get("DocEntry"),
                "DocNum": document_data.get("DocNum"),
                "DocObjectCode": document_data.get("DocObjectCode"),
                "documenttype": TypeOfSale.get_type_of_sale(document_data.get("DocumentSubType"), document_data.get("ReserveInvoice")),
                "FolioNumber": document_data.get("FolioNumber"),
                "CardCode": document_data.get("CardCode"),
                "CardName": document_data.get("CardName"),
                "SalesPersonCode": document_data.get("SalesPersonCode"),
                "DocDate": document_data.get("DocDate"),
                "DocumentStatus": document_data.get("DocumentStatus"),
                "Cancelled": document_data.get("Cancelled"),
                "NetTotal": document_data.get("DocTotal") - document_data.get("VatSum"),
                "DocTotal": document_data.get("DocTotal"),
                "SalesEmployeeName": re.sub(r'.*-\s*','',sales_person.get("SalesEmployeeName")),
            })

        return serialized_data
    
    def serializer_sales_details(data_bp, data_lines):

        if not data_bp or not data_lines:
            return {}
        
        invoice_data = data_bp.get('Invoices', {})
        
        invoice_bp = {
            "documenttype": TypeOfSale.get_type_of_sale(invoice_data.get("DocumentSubType"), invoice_data.get("ReserveInvoice")),
            "FolioNumber": invoice_data.get("FolioNumber"),
            "DocEntry": invoice_data.get("DocEntry"),
            "DocNum": invoice_data.get("DocNum"),
            "FederalTaxID": invoice_data.get("FederalTaxID"),
            "CardCode": invoice_data.get("CardCode"),
            "CardName": invoice_data.get("CardName"),
            "Address": invoice_data.get("Address").split("\r")[0],
            "Address2": invoice_data.get("Address2").split("\r")[0],
            "DocDate": invoice_data.get("DocDate"),
            "Comments": invoice_data.get("Comments"),
            "DocumentStatus": invoice_data.get("DocumentStatus"),
            "Cancelled": invoice_data.get("Cancelled"),
            "TransportationCode": Trasnportation.get_transportation_code(invoice_data.get("TransportationCode")),
            "DocTotalNeto": invoice_data.get("DocTotalNeto"),
            "VatSum": invoice_data.get("VatSum"),
            "DocTotal": invoice_data.get("DocTotal"),
        }

        invoice_lines = []
        for data in data_lines.get('value', []):
            doc_line = data.get('Invoices/DocumentLines', {})
            if doc_line:
                data_lines = {
                    "DocEntry": doc_line.get("DocEntry"),
                    "LineNum": doc_line.get("LineNum"),
                    "ItemCode": doc_line.get("ItemCode"),
                    "ItemDescription": doc_line.get("ItemDescription"),
                    "imagen":  ProductoRepository.obtenerImagenProducto(doc_line.get("ItemCode")),
                    "Quantity": doc_line.get("Quantity"),
                    "GrossPrice": doc_line.get("GrossPrice"),
                    "FreeText": doc_line.get("FreeText"),
                    "DiscountPercent": doc_line.get("DiscountPercent"),
                    "WarehouseCode": doc_line.get("WarehouseCode"),
                    "CostingCode": doc_line.get("CostingCode"),
                    "DiscountPercent": doc_line.get("DiscountPercent"),
                    "WarehouseCode": doc_line.get("WarehouseCode"),
                    "GrossPrice": doc_line.get("GrossPrice"),
                    "GrossTotal": doc_line.get("GrossTotal"),

                }
                tipo = doc_line.get("TreeType")
                
                if tipo != "I":
                    invoice_lines.append(data_lines)
        
        sales_data = data_bp.get('SalesPersons', {})
        sales_data_contact = data_bp.get('BusinessPartners/ContactEmployees', {})

        if sales_data_contact:
            invoice_bp["InternalCode"] = sales_data_contact.get("InternalCode")
            name = sales_data_contact.get("FirstName")
            if name != None:
                invoice_bp["FirstName"] = re.sub(r'.*-\s*','',sales_data_contact.get("FirstName"))
            else:
                invoice_bp["FirstName"] = invoice_data.get("CardName")

        if sales_data:
            invoice_bp["SalesEmployeeCode"] = sales_data.get("SalesEmployeeCode")
            invoice_bp["SalesEmployeeName"] = re.sub(r'.*-\s*','',sales_data.get("SalesEmployeeName"))
            invoice_bp["U_LED_SUCURS"] = sales_data.get("U_LED_SUCURS")
        
        

        return {
            "Invoices": invoice_bp,
            "DocumentLines": invoice_lines
        }

    @staticmethod
    def serialize_invoice_lines(json_data, salesperson):
        document_lines = []
        vendedor_repo = VendedorRepository()
        tipo_vendedor = vendedor_repo.obtenerTipoVendedor(salesperson)

        for line_info in json_data["DocumentLine"]["value"]:
            line = line_info  # <-- Ya está todo en line_info

            sku = line.get("ItemCode")

            imagen = ProductoRepository.obtenerImagenProducto(sku)
            marca = ProductoRepository.obtenerMarcaProducto(sku)
            descuentoMax = ProductoRepository.descuentoMax(sku)
            priceList = ProductoRepository.obtenerPrecioLista(sku)
            precioVenta = ProductoRepository.obtenerPrecioVenta(sku)

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

            warehouse_info = {
                "WarehouseCode": line.get("WarehouseCode"),
            }

            document_line = {
                "ItemCode": line.get("ItemCode"),  #enviado
                "ItemDescription": line.get("ItemDescription"), 
                "Quantity": line.get("Quantity"),
                "LineNum": line.get("LineNum"),  #enviado     
                "DocEntry": line.get("DocEntry_line"), #enviado
                "ShipDate": line.get("ShipDate"),
                "FreeText": line.get("FreeText"),
                "DiscountPercent": line.get("DiscountPercent"),
                "WarehouseInfo": warehouse_info,
                "WarehouseCode": line.get("WarehouseCode"),
                "ShippingMethod": line.get("ShippingMethod"),
                "imagen": imagen,
                "marca": marca,
                "descuentoMax": descuentoMax,
                "PriceList": priceList,
                "Price": precioVenta,
            }

            if document_line.get("Quantity", 1) > 0:
                document_lines.append(document_line)

        return document_lines
