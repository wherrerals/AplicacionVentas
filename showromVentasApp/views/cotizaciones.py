from django.http import JsonResponse
from showromVentasApp.views.documento import Documento
from adapters.sl_client import APIClient
import json
import logging

logger = logging.getLogger(__name__)

class Cotizaciones(Documento):
    
    def get_route_map(self):
        return {
            '/listado_Cotizaciones_filtrado/': self.filter_quotations,
            '/crear_cotizacion/': self.crear,
            '/obtener_detalles_cotizacion/': self.obtenerDetallesCotizacion,
        }

    def get_required_fields(self):
        return ['CardCode', 'DocumentLines']

    def prepare_json_data(self, data):
        return {
            "DocDate": data.get('DocDate'),
            "DocDueDate": data.get('DocDueDate'),
            "TaxDate": data.get('TaxDate'),
            "CardCode": data.get('CardCode'),
            "PaymentGroupCode": data.get('PaymentGroupCode'),
            "SalesPersonCode": data.get('SalesPersonCode'),
            "TransportationCode": data.get('TransportationCode'),
            "U_LED_NROPSH": data.get('U_LED_NROPSH'),
            "U_LED_TIPVTA": data.get('U_LED_TIPVTA'),
            "U_LED_TIPDOC": data.get('U_LED_TIPDOC'),
            "U_LED_FORENV": data.get('U_LED_FORENV'),
            "DocumentLines": data.get('DocumentLines')
        }

    def get_endpoint(self):
        return 'Quotations'

    def get(self, request, *args, **kwargs):
        docEntry = kwargs.get('DocEntry')
        if docEntry:
            return self.quotate_items(request, docEntry)
        else:
            return self.listarCotizaciones(request)

    def listarCotizaciones(self, request):
        try:
            client = APIClient()
            top = int(request.GET.get('top', 20))
            skip = int(request.GET.get('skip', 0))
            data = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip)
            return JsonResponse(data, safe=False)
        except ValueError:
            return self.handle_error(ValueError("Parámetros inválidos"))
        except Exception as e:
            return self.handle_error(e)

    def filter_quotations(self, request):
        try:
            data = json.loads(request.body)
            client = APIClient()
            filters = self.prepare_filters(data)
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
            result = client.getData(endpoint=self.get_endpoint(), top=top, skip=skip, filters=filters)
            return JsonResponse({'data': result}, safe=False)
        except json.JSONDecodeError:
            return self.handle_error(json.JSONDecodeError("JSON inválido", request.body, 0))
        except Exception as e:
            return self.handle_error(e)

    def prepare_filters(self, data):
        filters = {}
        filter_mappings = {
            'fecha_inicio': ('Quotations/DocDate ge', str),
            'fecha_fin': ('Quotations/DocDate le', str),
            'docNum': ('contains(Quotations/DocNum,', int),
            'carCode': ('contains(Quotations/CardCode,', str),
            'cardNAme': ('contains(Quotations/CardName,', str),
            'salesEmployeeName': ('contains(SalesPersons/SalesEmployeeName,', str),
            'DocumentStatus': ('Quotations/DocumentStatus eq', str),
            'docTotal': ('contains(Quotations/DocTotal,', int),
            'cancelled': ('Quotations/Cancelled eq', str),
        }

        for key, (filter_key, value_type) in filter_mappings.items():
            if data.get(key):
                value = value_type(data.get(key))
                filters[filter_key] = f"'{value}'" if isinstance(value, str) else f"{value})"

        return {k: v for k, v in filters.items() if v and v != "''"}

    def obtenerDetallesCotizacion(self, request, docEntry):
        try:
            client = APIClient()
            doc_num_int = int(docEntry)
            all_quotations = self.get_all_quotations(client, docEntry)
            found_quotation = next((q for q in all_quotations if q.get('docEntry') == doc_num_int), None)

            if not found_quotation:
                raise ValueError('No se encontró la cotización con el DocNum especificado')

            document_lines = found_quotation.get('DocumentLines', [])
            lines_data = self.prepare_lines_data(document_lines)
            return JsonResponse({'DocumentLines': lines_data}, status=200)
        except Exception as e:
            return self.handle_error(e)

    def get_all_quotations(self, client, docEntry):
        all_quotations = []
        page = 1
        while True:
            data = client.get_quotations_items('Quotations', docEntry, top=20, skip=(page - 1) * 20)
            if 'value' not in data or not data['value']:
                break
            all_quotations.extend(data['value'])
            if 'odata.nextLink' not in data:
                break
            page += 1
        return all_quotations

    def prepare_lines_data(self, document_lines):
        return [
            {
                'LineNum': line.get('LineNum'),
                'ItemCode': line.get('ItemCode'),
                'ItemDescription': line.get('ItemDescription'),
                'Quantity': line.get('Quantity'),
                'Price': line.get('Price'),
            }
            for line in document_lines
        ]

    def quotate_items(self, request, docNum):
        try:
            client = APIClient()
            data = client.get_quotations_items('Quotations')
            if 'value' not in data:
                raise ValueError('No se encontraron datos de cotizaciones')

            quotations = data['value']
            found_quotation = next((q for q in quotations if q.get('DocNum') == int(docNum)), None)

            if not found_quotation:
                raise ValueError('No se encontró la cotización con el DocNum especificado')

            document_lines = found_quotation.get('DocumentLines', [])
            lines_data = self.prepare_lines_data(document_lines)
            return JsonResponse({'DocumentLines': lines_data}, status=200)
        except Exception as e:
            return self.handle_error(e)