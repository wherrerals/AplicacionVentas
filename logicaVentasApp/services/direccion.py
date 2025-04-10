import json
from django.http import JsonResponse

from datosLsApp.repositories.direccionrepository import DireccionRepository


class Direccion:

    def __init__(self):
        pass

    def procesarDireccionDesdeAPI(self, data, socio):

        try:
            # Extraer contactos de la respuesta
            direccioness_api = data.get('BPAddresses', [])

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
            direcciones_json = json.dumps(direcciones, ensure_ascii=False)

            # Simular el request con getlist('contactos')
            request_data = {"direcciones": [direcciones_json]}


            from logicaVentasApp.services.socionegocio import SocioNegocio

            # Reutilizar el método original
            return SocioNegocio.procesarDirecciones(request_data, socio)

        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Falta el campo: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error inesperado: {str(e)}'}, status=500)

    def generate_store_address(sucursal):
        direcciones = [
            {
                "Sucursal": "LC",
                "nombreDireccion": "Showroom Las Condes",
                "pais": "Chile",
                "region": "13",
                "comuna": "13114",
                "tipoDireccion": "12",
                "ciudad": "Santiago",
                "direccion": "Las Condes 7363, Las Condes, Santiago, Chile"
            },
            {
                "Sucursal": "PH",
                "nombreDireccion": "Showroom Vitacura",
                "pais": "Chile",
                "region": "13",
                "comuna": "13132",
                "tipoDireccion": "12",
                "ciudad": "Santiago",
                "direccion": "Padre Hurtado Norte 1199, Vitacura, Santiago, Chile"
            },
            {
                "Sucursal": "ME",
                "nombreDireccion": "Showroom Renca",
                "pais": "Chile",
                "region": "13",
                "comuna": "13128",
                "tipoDireccion": "12",
                "ciudad": "Santiago",
                "direccion": "Av. Presidente Frei Montalva 550, Bodega 02, Renca, Santiago, Chile"
            }
        ]
        
        # Diccionario para manejar equivalencias de sucursales
        equivalencias = {
            "LC": "LC",
            "RS": "LC",
            "ME": "ME",
            "PH": "PH"
        }
        
        # Buscar la sucursal con la equivalencia
        sucursal_normalizada = equivalencias.get(sucursal)
        
        # Encontrar y devolver el diccionario de la sucursal
        for direccion in direcciones:
            if direccion["Sucursal"] == sucursal_normalizada:
                return [direccion]
        
        # Si no se encuentra la sucursal, devolver None
        return None
    
    @staticmethod
    def assign_bill_ship_addres(adrres, adrres2):
        
        if adrres == "No hay direcciones disponibles":
            addres_bill = DireccionRepository.obtenerDireccion(adrres)
        else:
            addres_bill = DireccionRepository.obtenerDireccion(adrres2)

        if adrres2 == "No hay direcciones disponibles":
            addres_ship = DireccionRepository.obtenerDireccion(adrres2)
        else:
            addres_ship = DireccionRepository.obtenerDireccion(adrres)
        
        return addres_bill, addres_ship