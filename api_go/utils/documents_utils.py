from datetime import datetime
from infrastructure.models.usuariodb import UsuarioDB


class CotizacionPayloadBuilder:

    @staticmethod
    def build(data: dict) -> dict:
        doc_date = datetime.now().strftime("%Y-%m-%d")

        sales_person_code = data.get("SalesPersonCode")

        warehouse_code = CotizacionPayloadBuilder._get_warehouse(sales_person_code)

        return {
            "DocDate": doc_date,
            "DocDueDate": doc_date,
            "TaxDate": doc_date,

            "NumAtCard": data.get("NumAtCard", ""),
            "Comments": data.get("Comments", ""),
            "CardCode": data["CardCode"],

            "PaymentGroupCode": data.get("PaymentGroupCode", -1),
            "SalesPersonCode": sales_person_code,
            "TransportationCode": data.get("TransportationCode", "1"),

            "U_LED_TIPDOC": data.get("U_LED_TIPDOC", "BOLE"),
            "U_LED_FORENV": data.get("U_LED_FORENV", 1),

            "DocumentLines": CotizacionPayloadBuilder._build_lines(
                data.get("DocumentLines", []),
                doc_date,
                warehouse_code
            ),
            "Cupon_code": data.get("Cupon_code", "")
        }

    @staticmethod
    def _build_lines(lines, doc_date, warehouse_code):
        result = []

        for line in lines:
            result.append({
                "ItemCode": line["ItemCode"],
                "Quantity": line["Quantity"],
                "ShipDate": doc_date,
                "FreeText": line.get("FreeText", ""),
                "WarehouseCode": warehouse_code,
                "ShippingMethod": line.get("ShippingMethod", "1"),
                "COGSCostingCode": warehouse_code,
                "CostingCode2": "AV",
                "COGSCostingCode2": "AV",
            })

        return result

    @staticmethod
    def _get_warehouse(sales_person_code):
        if not sales_person_code:
            return None

        usuario = (
            UsuarioDB.objects
            .select_related("sucursal", "vendedor")
            .filter(vendedor__codigo=sales_person_code)
            .first()
        )

        if not usuario or not usuario.sucursal:
            return None

        return usuario.sucursal.codigo  # ← esto es lo que necesitas