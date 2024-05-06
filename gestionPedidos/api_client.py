# api_client.py
import requests
from django.conf import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.session = requests.Session()
        self.login()

    def login(self):
        login_url = f"{self.base_url}Login"
        auth_data = {
            "CompanyDB": settings.COMPANY_DB,
            "UserName": settings.API_USERNAME,
            "Password": settings.API_PASSWORD
        }
        response = self.session.post(login_url, json=auth_data, verify=False)
        response.raise_for_status()

    def get_data(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
