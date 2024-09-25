import requests
import json
from django.http import JsonResponse
from adapter.vtex_client import VTEXClient
from adapter.sl_client import APIClient

def cambio_ordenes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_number = data.get('orderNumber')

            # Consulta a la API de Service Layer
            client = APIClient()
            service_layer_data = client.get_orders(order_number)
            
            if 'value' in service_layer_data and len(service_layer_data['value']) > 0:
                first_item = service_layer_data['value'][0]  # Tomamos el primer elemento de 'value'
                folio_number = first_item.get('FolioNumber')
                u_report_pdf = first_item.get('U_ReportPdf')

                print(f'FolioNumber: {folio_number}')
                print(f'U_ReportPdf: {u_report_pdf}')
            else:
                return JsonResponse({'message': 'No se encontraron datos en Service Layer para el número de orden especificado'}, status=404)
            
            # Consulta a la API de VTEX
            vtex_client = VTEXClient()
            vtex_data = vtex_client.get_order_details(order_number)

            value = vtex_data.get('value')
            creation_date = vtex_data.get('creationDate')

            print(f'value: {value}')
            print(f'creationDate: {creation_date}')

            # Construir el JSON y enviarlo a otra URL de VTEX
            payload = {
                "type":'Output', #string
                "issuanceDate": creation_date, #string
                # Agregar otros campos del payload según sea necesario
                "invoiceNumber": folio_number, #string
                "invoiceValue": value, #string revisar que el campo en el excel sea si o si tipo numero, luego de agg los dos 00 adicionales
                "invoiceKey": '', #string 
                "invoiceUrl": u_report_pdf, #string 
                "courier": '', #string 
                "trackingNumber": '', #string 
                "trackingUrl": '', #string 
                "dispatchedDate": '', #string 
            }

            vtex_post_url = f'https://ledstudiocl.myvtex.com/api/oms/pvt/orders/{order_number}/invoice'
            vtex_post_response = requests.post(vtex_post_url, json=payload, headers=vtex_client.headers)
            vtex_post_response.raise_for_status()

            return JsonResponse({'message': 'Proceso completado exitosamente', 'data': vtex_post_response.json()})
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Error al decodificar JSON en la solicitud'}, status=400)
        
        except requests.RequestException as e:
            return JsonResponse({'message': 'Error al hacer la solicitud a VTEX', 'error': str(e)}, status=500)
        
        except Exception as e:
            return JsonResponse({'message': 'Error al procesar la solicitud', 'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)