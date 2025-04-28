from logicaVentasApp.services.typeofsale import TypeOfSale
import re

class SalesConsultationSerializer:

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
            "FederalTaxID": invoice_data.get("FederalTaxID"),
            "CardCode": invoice_data.get("CardCode"),
            "CardName": invoice_data.get("CardName"),
            "TransportationCode": invoice_data.get("TransportationCode"),
            "Address": invoice_data.get("Address"),
            "Address2": invoice_data.get("Address2"),
            "DocDate": invoice_data.get("DocDate"),
            "Comments": invoice_data.get("Comments"),
            "DocumentStatus": invoice_data.get("DocumentStatus"),
        }

        invoice_lines = []
        for data in data_lines.get('value', []):
            doc_line = data.get('Invoices/DocumentLines', {})
            if doc_line:
                data_lines = {
                    "ItemCode": doc_line.get("ItemCode"),
                    "Quantity": doc_line.get("Quantity"),
                    "UnitPrice": doc_line.get("UnitPrice"),
                    "ShipDate": doc_line.get("ShipDate"),
                    "FreeText": doc_line.get("FreeText"),
                    "DiscountPercent": doc_line.get("DiscountPercent"),
                    "WarehouseCode": doc_line.get("WarehouseCode"),
                    "CostingCode": doc_line.get("CostingCode"),
                    "ShippingMethod": doc_line.get("ShippingMethod"),
                    "COGSCostingCode": doc_line.get("COGSCostingCode"),
                    "CostingCode2": doc_line.get("CostingCode2")
                }
                invoice_lines.append(data_lines)
        
        sales_data = data_bp.get('SalesPersons', {})
        if sales_data:
            invoice_bp["SalesEmployeeCode"] = sales_data.get("SalesEmployeeCode")
            invoice_bp["SalesEmployeeName"] = re.sub(r'.*-\s*','',sales_data.get("SalesEmployeeName"))
            invoice_bp["U_LED_SUCURS"] = sales_data.get("U_LED_SUCURS")
        
        return {
            "Invoices": invoice_bp,
            "DocumentLines": invoice_lines
        }
        