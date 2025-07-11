import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

# Importing modules
from adapters.sl_client import APIClient
from datosLsApp.models.documentodb import DocumentoDB
from datosLsApp.models.usuariodb import UsuarioDB
from datosLsApp.serializer.invoiceSerializer import InvoiceSerializer
from logicaVentasApp.context.user_context import UserContext
from logicaVentasApp.services.documento import Documento
from logicaVentasApp.services.invoice import Invoice
from logicaVentasApp.services.socionegocio import SocioNegocio
from logicaVentasApp.services.usuario import User
from logicaVentasApp.services.valitadionApp import ValitadionApp

logger = logging.getLogger(__name__)


class InvoiceView(View):

    # this method dispatches the request to the appropriate handler based on the HTTP method
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    @method_decorator(require_http_methods(["GET", "POST"]))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            route_handler = self.get_route_map().get(request.path.rstrip('/'), None)
        
            if route_handler is None:
                return JsonResponse({'error': 'Ruta no válida'}, status=404)
            
            return route_handler(request, *args, **kwargs)
        
        except Exception as e:
            logger.error(f"Error in GET method: {str(e)}")
            return JsonResponse({'error': 'Ocurrió un error en el servidor'}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            path = request.path
            route_handler = self.post_route_map().get(path) or self.post_route_map().get(path.rstrip('/'))
            if route_handler is None:
                return JsonResponse({'error': 'Ruta no válida'}, status=404)
            return route_handler(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in POST method: {str(e)}")
            return JsonResponse({'error': 'Ocurrió un error en el servidor'}, status=500)


    def post_route_map(self):
        return {
            '/ventas/obtener-ventas': self.get_sales_view,
            '/ventas/duplicar-documento': self.duplicate_in_document,
        }


    def get_route_map(self):

        return {
            '/ventas/consulta-ventas': self.sales_consultation,
            '/ventas/lista-ventas': self.sales_list_view,
            '/ventas/detalles-ventas': self.sales_details_view,

        }
    
    def sales_consultation(self, request):

        authenticated_user = ValitadionApp.user_autentication(request)
        context = UserContext.user_context(authenticated_user, request)

        return render(request, 'salesConsultation.html', context)
    
    def sales_list_view(self, request):

        authenticated_user = ValitadionApp.user_autentication(request)
        context = UserContext.user_context(authenticated_user, request)

        return render(request, 'list_sales_global.html', context)

    def get_sales_view(self, request):

        api_service_layer = APIClient()
        type_sales = "Invoices"

        build_filters = Invoice.build_query_filters(json.loads(request.body), type_sales)
        get_data_sales = api_service_layer.get_sales_sl(build_filters, type_sales)
        data_sales_serializer = InvoiceSerializer.serializer_sales(get_data_sales)

        return JsonResponse({"data": data_sales_serializer}, safe=False)

    def sales_details_view(self, request):
        
        docEntry = request.GET.get('docentry')
        api_service_layer = APIClient()

        sales_data_bp = api_service_layer.sales_details_sl_bp(type_document='Invoices', docEntry=docEntry)
        sales_data_lines = api_service_layer.sales_details_sl_lines(type_document='Invoices', docEntry=docEntry)
        data_sales_serializer = InvoiceSerializer.serializer_sales_details(sales_data_bp, sales_data_lines)

        print("Datos de ventas serializados:", data_sales_serializer)

        socio_negocio_data = data_sales_serializer.get('Invoices')
        if socio_negocio_data:
            card_code = socio_negocio_data.get('CardCode')
            tax_id = socio_negocio_data.get('FederalTaxID')

            if card_code and tax_id:
                sn = SocioNegocio(request)
                if not sn.verificarSocioDB(card_code):
                    sn.crearYresponderCliente(card_code, tax_id)

        return JsonResponse(data_sales_serializer, safe=False)

    

    def duplicate_in_document(self, request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)

                print("Datos recibidos para duplicar documento:", data)

                tipo_documento = data.get('tipo', 'NA')

                sales_person_code = User.user_data(request)['vendedor']
                lineas_procesadas = InvoiceSerializer.serialize_invoice_lines(data, sales_person_code, tipo_documento)
                # Procesar duplicación u otras tareas

                print("Líneas procesadas Duplicar Documento:", lineas_procesadas)
                
                return JsonResponse({"status": "ok", "lineas": lineas_procesadas})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)
        return JsonResponse({"error": "Método no permitido"}, status=405)



    def duplicate_in_document(self, request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                print("Datos recibidos para duplicar documento:", data)

                tipo_documento = data.get('tipo', 'NA')
                sales_person_code = User.user_data(request)['vendedor']
                lineas_procesadas = InvoiceSerializer.serialize_invoice_lines(data, sales_person_code, tipo_documento)

                folio = data.get('folio')
                dict_entry = data.get('docEntry')

                existe_folio = DocumentoDB.objects.filter(folio=folio).exists()

                if existe_folio:
                    for linea in lineas_procesadas:
                        producto_codigo = linea.get('ItemCode')
                        num_linea = int(linea.get('LineNum'))

                        try:
                            saldo = Documento.saldo_disponible_linea(
                                docentry_ref=dict_entry,
                                producto_codigo=producto_codigo,
                                numLinea=num_linea
                            )

                            linea['Quantity'] = saldo

                        except Exception as e:
                            print(f"No se pudo calcular saldo para {producto_codigo} Linea {num_linea}: {str(e)}")
                else:
                    print(f"No existe folio base {folio}. Se usan cantidades originales.")

                print("Líneas procesadas Duplicar Documento:", lineas_procesadas)

                return JsonResponse({
                    "status": "ok",
                    "message": "Documento duplicado correctamente",
                    "lineas": lineas_procesadas
                })

            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        return JsonResponse({"error": "Método no permitido"}, status=405)