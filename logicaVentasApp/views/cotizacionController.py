from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datosLsApp.sl_client import APIClient
import json

@method_decorator(csrf_exempt, name='dispatch')
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

        data = client.get_quotations(top=top, skip=skip)
        return JsonResponse(data, safe=False)
    
    def post(self, request):
        # Implementación del método POST para filtrado de cotizaciones
        if request.path == '/listado_Cotizaciones_filtrado/':
            return self.filter_quotations(request)
        else:
            # Manejar el caso cuando la ruta no es correcta
            return JsonResponse({'error': 'Invalid URL'}, status=404)
    
    def filter_quotations(self, request):
        print("Request body:", request.body)  # Verifica el cuerpo de la solicitud JSON recibida
        
        client = APIClient()

        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Verifica los datos JSON recibidos
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        filters = {}

        # Agregar filtros solo si se proporcionan datos válidos
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
            filters['contains(Quotations/DocTotal,'] = data.get('docTotal')
        if data.get('cancelled'):
            filters['Quotations/Cancelled eq'] = f"'{data.get('cancelled')}'"

        # Limpiar los filtros vacíos o con valores inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        try:
            top = int(data.get('top', 20))
            skip = int(data.get('skip', 0))
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        print("Applying filters:", filters)# Verifica los filtros aplicados
        print("-" * 10)  
        print(filters)
        

        try:
            data = client.get_quotations(top=top, skip=skip, filters=filters)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            print("Error:", e)  # Verifica el error específico que está ocurriendo
            return JsonResponse({'error': str(e)}, status=500)
