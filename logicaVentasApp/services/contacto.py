import json
from django.http import JsonResponse
from logicaVentasApp.services.socionegocio import SocioNegocio


class Contacto:

    def __init__(self):
        pass

    def procesarContactosDesdeAPI(self, data, socio):
        print("Procesando contactos desde API...")
        print(f"Datos recibidos: {data}")

        try:
            # Extraer contactos de la respuesta
            contactos_api = data.get('ContactEmployees', [])
            print(f"Contactos extraídos de la API: {contactos_api}")

            if not contactos_api:
                return JsonResponse({'success': False, 'message': 'No se encontraron contactos en la respuesta de la API.'}, status=400)

            # Transformar los datos al formato esperado por el método original
            contactos = [
                {
                    "nombre": contacto.get('FirstName', '').strip(),
                    "apellido": contacto.get('LastName', '').strip(),
                    "telefono": contacto.get('Phone1', '').strip(),
                    "celular": contacto.get('MobilePhone', '').strip(),
                    "email": contacto.get('E_Mail', '').strip(),
                    "contacto_id": contacto.get('InternalCode')
                }
                for contacto in contactos_api
            ]

            print(f"Contactos transformados: {contactos}")
            # Convertir al formato JSON string que espera el método original
            contactos_json = json.dumps(contactos)

            print(f"Contactos JSON: {contactos_json}")
            # Simular el request con getlist('contactos')
            request_data = {"contactos": [contactos_json]}

            # Reutilizar el método original
            return SocioNegocio.procesarContactos(request_data, socio)

        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Falta el campo: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error inesperado: {str(e)}'}, status=500)
