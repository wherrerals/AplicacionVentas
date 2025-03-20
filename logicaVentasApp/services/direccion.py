import json
from django.http import JsonResponse


class Direccion:

    def __init__(self):
        pass

    def procesarDireccionDesdeAPI(self, data, socio):
        print("PASO 5")
        print(f"Datos recibidos: {data}")

        try:
            # Extraer contactos de la respuesta
            direccioness_api = data.get('BPAddresses', [])
            print(f"Contactos extraídos de la API: {direccioness_api}")

            if not direccioness_api:
                return JsonResponse({'success': False, 'message': 'No se encontraron contactos en la respuesta de la API.'}, status=400)

            # Transformar los datos al formato esperado por el método original
            direcciones = [
                {
                    "tipoDireccion": direccion.get('AddressType', ''),
                    "nombreDireccion": direccion.get('AddressName', ''),
                    "ciudad": direccion.get('City', ''),
                    "pais": direccion.get('Country', ''),
                    "region": direccion.get('State', ''),
                    "comuna": direccion.get('County'),
                    "direccion": direccion.get('Street'),
                    "row_id": direccion.get('RowNum')
                }
                for direccion in direccioness_api
            ]

            # Convertir al formato JSON string que espera el método original
            direcciones_json = json.dumps(direcciones)

            # Simular el request con getlist('contactos')
            request_data = {"direcciones": [direcciones_json]}

            print("Requestadata",request_data)

            from logicaVentasApp.services.socionegocio import SocioNegocio

            # Reutilizar el método original
            return SocioNegocio.procesarDirecciones(request_data, socio)

        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Falta el campo: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error inesperado: {str(e)}'}, status=500)

    @staticmethod
    def generarDireccionTiendas():
        direcciones = [
                {
                "nombreDireccion": "Direccion General",
                "pais": 'Chile',
                "region": '13',
                "comuna": '13101',
                "tipoDireccion": '12',
                "ciudad": 'Santiago',
                "direccion": 'Av. Las Condes 7363, Las Condes, Santiago, Chile',
                }
        ]
        return direcciones