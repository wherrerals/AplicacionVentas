#Hacer las pruebas en el modulo de vista tienen que enlazar la url 

""" def pruebas(request):
    try:
        # Crear una instancia del cliente de la API
        client = APIClient()

        # Realizar una solicitud de prueba a la API
        full_data = client.get_data('Items')

        # Extraer solo los campos necesarios
        processed_data = []
        for item in full_data['value']:
            processed_item = {
                'value': item['ItemCode'],
                'ItemName': item['ItemName'],
                'precio': item.get('ItemPrices', [{}])[0].get('Price', None),  # Precio del primer elemento en ItemPrices
                'precioAnterior': item.get('ItemPrices', [{}])[0].get('BasePriceList', None)  # Precio anterior del primer elemento en ItemPrices
            }
            processed_data.append(processed_item)

        # Devolver los datos procesados como una respuesta JSON
        return JsonResponse({'resultados': processed_data})
    except Exception as e:
        # Manejar cualquier error que ocurra durante la solicitud
        return JsonResponse({'error': str(e)}) """

#prueba para URLS 

""" def pruebas(request):
    # Crear una instancia del cliente de la API
    client = APIClient()
    SKU = "C10100519"

    # Realizar solicitudes a la API
    data = client.get_data2('Items', SKU)

    # Devolver los datos como una respuesta JSON
    return JsonResponse(data) """