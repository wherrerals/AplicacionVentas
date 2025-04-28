from logicaVentasApp.services.typeofsale import TypeOfSale


class SalesConsultationSerializer:

    @staticmethod
    def serializer_sales(data):

        #mnajear si la lista es vacia

        if not data or 'value' not in data or not data['value']:
            return {}

        data_sales = data['value'][0]
        
        main_key = next(iter(data_sales))
        document_data = data_sales[main_key]
        sales_person_code = document_data.get("SalesPersonCode") 

        return {
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
            "VatSum": document_data.get("VatSum"),
            "DocTotal": document_data.get("DocTotal"),
            "SalesEmployeeName": sales_person_code
        }
    