from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
from django.http import JsonResponse
from datosLsApp.sl_client import APIClient
import json

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class Documento(View):
    
    def __init__(self, docEntry=None, docNum=None, folio=None, fechaDocumento=None, numEntrega=None, fechaEntrega=None, 
                 referencia=None, comentario=None, totalAntesDelDescuento=None, totalDocumento=None, codigoVenta=None, client=None):
        
        self.docEntry = docEntry
        self.docNum = docNum
        self.folio = folio
        self.fechaDocumento = fechaDocumento
        self.numEntrega = numEntrega
        self.fechaEntrega = fechaEntrega
        self.referencia = referencia
        self.comentario = comentario
        self.totalAntesDelDescuento = totalAntesDelDescuento
        self.descuento = 0
        self.totalDocumento = totalDocumento
        self.codigoVenta = codigoVenta
        self.client = client or APIClient()

    def get(self, request):
        top = request.GET.get('top', 20)
        skip = request.GET.get('skip', 0)

        try:
            top = int(top)
            skip = int(skip)
        except ValueError:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        data = self.client.getData(endpoint='Quotations', top=top, skip=skip)
        return JsonResponse(data, safe=False)
    
    def post(self, request):
        if request.path == '/listado_Cotizaciones_filtrado/':
            return self.filter(request)
        else:
            return JsonResponse({'error': 'Invalid URL'}, status=404)
    
    def filter(self, request):
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
            docTotal = int(data.get('docTotal'))
            filters['contains(Quotations/DocTotal,'] = f"{docTotal})"
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
            data = self.client.getData(endpoint='Quotations', top=top, skip=skip, filters=filters)
            return JsonResponse({'data': data}, safe=False)
        except Exception as e:
            print("Error:", e)  # Verifica el error específico que está ocurriendo
            return JsonResponse({'error': str(e)}, status=500)
