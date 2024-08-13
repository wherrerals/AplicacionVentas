from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from datosLsApp.sl_client import APIClient


@method_decorator(require_http_methods(["GET"]), name="dispatch")
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