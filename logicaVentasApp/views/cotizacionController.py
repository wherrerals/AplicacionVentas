from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datosLsApp.sl_client import APIClient
import re
import json

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name="dispatch")
class CotizacionesController(View):
    
    def get(self, request):
        client = APIClient()

        top = request.GET.get('top', 20)
        skip = request.GET.get('skip', 0)

        try:
            top = int(top)
            skip = int(skip)
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        data = client.getData(endpoint='Quotations', top=top, skip=skip)
        return JsonResponse(data, safe=False)

    def post(self, request):

        route_map = {
            '/listado_Cotizaciones_filtrado/': self.filter_quotations,
            '/crear_cotizacion/': self.crearCotizacion,
        }

        handler = route_map.get(request.path)

        if not handler:

            dynamic_routes = [
                (r'^/actualizar_cotizacion/\d+/$', self.actualizarCotizacion),
            ]

            for pattern, view_method in dynamic_routes:
                if re.match(pattern, request.path):

                    doc_num = re.findall(r'\d+', request.path)[0]
                    return view_method(request, doc_num)

            return JsonResponse({'error': 'Invalid URL'}, status=404)

        return handler(request)
    

    def crearCotizacion(self, request):
        client = APIClient()
        try:

            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        required_fields = ['CardCode', 'DocumentLines']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        

        json_data = {
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


        endpoint = 'Quotations'
        headers = {"Content-Type": "application/json"}


        result = client.post_data(endpoint, data=json_data, headers=headers)


        return JsonResponse(result, safe=False)


    def filter_quotations(self, request):
        print("Request body:", request.body)
        
        client = APIClient()

        try:
            data = json.loads(request.body)
            print("Received data:", data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        filters = {}


        if data.get('fecha_inicio'):
            filters['Quotations/DocDate ge'] = f"'{data.get('fecha_inicio')}'"
        if data.get('fecha_fin'):
            filters['Quotations/DocDate le'] = f"'{data.get('fecha_fin')}'"
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Quotations/DocNum,'] = f"{docum})"
        if data.get('carCode'):
            filters['contains(Quotations/CardCode,'] = f"'{data.get('carCode')}'"
        if data.get('cardNAme'):
            filters['contains(Quotations/CardName,'] = f"'{data.get('cardNAme')}')"
        if data.get('salesEmployeeName'):
            filters['contains(SalesPersons/SalesEmployeeName,'] = f"'{data.get('salesEmployeeName')}'"
        if data.get('DocumentStatus'):
            filters['Quotations/DocumentStatus eq'] = f"'{data.get('DocumentStatus')}'"
        if data.get('docTotal'):
            docTotal = int(data.get('docTotal'))
            filters['contains(Quotations/DocTotal,'] = f"{docTotal})"
        if data.get('cancelled'):
            filters['Quotations/Cancelled eq'] = f"'{data.get('cancelled')}'"


        filters = {k: v for k, v in filters.items() if v and v != "''"}

        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        print("Applying filters:", filters)
        print("-" * 10)  
        print(filters)
        

        try:
            data = client.getData(endpoint='Quotations', top=top, skip=skip, filters=filters)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            print("Error:", e) 
            return JsonResponse({'error': str(e)}, status=500)

    def actualizarCotizacion(self, request,  docNum):
        client = APIClient()  

        try:
            data = client.get_quotations_items('Quotations')


            if 'value' in data:
                quotations = data['value']
                found_quotation = None

                for quotation in quotations:
                    if quotation.get('DocNum') == int(docNum):
                        found_quotation = quotation
                        break

                if found_quotation:

                    document_lines = found_quotation.get('DocumentLines', [])


                    lines_data = []
                    for line in document_lines:
                        line_data = {
                            'LineNum': line.get('LineNum'),
                            'ItemCode': line.get('ItemCode'),
                            'ItemDescription': line.get('ItemDescription'),
                            'ItemCode': line.get('ItemCode'),
                            'ItemDescription': line.get('ItemDescription'),
                            'Quantity': line.get('Quantity'),
                            'Price': line.get('Price'),
                        }
                        lines_data.append(line_data)


                    return JsonResponse({'DocumentLines': lines_data}, status=200)
                else:
                    return JsonResponse({'error': 'No se encontró la cotización con el DocNum especificado'}, status=404)

            else:
                return JsonResponse({'error': 'No se encontraron datos de cotizaciones'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    """     
    def post(self, request):
        # Implementación del método POST para filtrado de cotizaciones
        if request.path == '/listado_Cotizaciones_filtrado/':
            return self.filter_quotations(request)
        else:
            # Manejar el caso cuando la ruta no es correcta
            return JsonResponse({'error': 'Invalid URL'}, status=404)
    
    def post(self, request):
        # Implementación del método POST para crear productos
        if request.path == '/crear_cotizacion/':
            return self.crearCotizacion(request)
        else:
            # Manejar el caso cuando la ruta no es correcta
            return JsonResponse({'error': 'Invalid URL'}, status=404) 
    """
    