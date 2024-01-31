import requests

def obtener_datos_sap(Quotations):
    url = f'https://182.160.29.24:50003/b1s/v1/Quotations'
    # Configura los encabezados y autenticación según sea necesario
    headers = {'Content-Type': 'application/json'}
    auth = ('manager', '1245LED98')
    
    try:
        # Realiza la solicitud GET
        response = requests.get(url, headers=headers, auth=auth)

        # Verifica si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Devuelve los datos en formato JSON
            return response.json()
        else:
            # Manejo de errores para códigos diferentes de 200
            print(f'Error al obtener datos: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        # Manejo de errores para excepciones durante la solicitud
        print(f'Error en la solicitud: {e}')
        return None
    

# Llamada a la función con un endpoint específico
datos_sap = obtener_datos_sap('Quotations')
