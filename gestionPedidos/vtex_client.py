# vtex_client.py
import requests
from django.conf import settings

class VTEXClient:
    def __init__(self):
        self.base_url = settings.VTEX_BASE_URL
        self.headers = {
            'Accept': "application/json",
            'Content-Type': "application/json",
            'X-VTEX-API-AppKey': settings.VTEX_APP_KEY,
            'X-VTEX-API-AppToken': settings.VTEX_APP_TOKEN
        }

    def get_order_details(self, order_number):
        url = f"{self.base_url}oms/pvt/orders/{order_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
