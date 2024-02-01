import requests
import Response

class SAPServiceLayerView(APIView):
    def get(self, request):
        url = 'https://182.160.29.24:50003/b1s/v1/login'
        headers = {'Content-Type': 'application/json'}
        auth = ("manager", "1245LED98", "TEST_LED_PROD")

        try:
            # Realiza la solicitud GET con la verificación SSL deshabilitada
            response = requests.get(url, headers=headers, auth=auth, verify=False)

            if response.status_code == 200:
                # Puedes personalizar la lógica para manejar los datos según tus necesidades
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(f'Error al obtener datos: {response.status_code}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            return Response(f'Error en la solicitud: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
