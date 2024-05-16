import aiohttp
import asyncio
import requests
from django.conf import settings
from django.http import JsonResponse


class AsyncAPIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.session = aiohttp.ClientSession()

    async def login(self):
        login_url = f"{self.base_url}Login"
        auth_data = {
            "CompanyDB": settings.COMPANY_DB,
            "UserName": settings.API_USERNAME,
            "Password": settings.API_PASSWORD
        }
        async with self.session.post(login_url, json=auth_data, verify_ssl=False) as response:
            response.raise_for_status()

    async def get_data(self, endpoint):
        await self.login()  # Asegurarse de que la autenticación se haya completado antes de realizar la solicitud
        url = f"{self.base_url}{endpoint}"
        async with self.session.get(url, verify_ssl=False) as response:
            response.raise_for_status()
            return await response.json()

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
    
    def get_data2(self, endpoint, id_item):
        url = f"{self.base_url}{endpoint}('{id_item}')"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    
