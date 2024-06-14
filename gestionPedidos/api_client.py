import requests
from django.conf import settings
from django.http import JsonResponse

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
    
    def get_data_rules2(self, endpoint):
        select = "DocEntry,DocNum,CardName,DocDate,SalesPersonCode,Cancelled,DocTotal,DocumentLines"
        top= 80
        skip=1
        queryUrl = f"?$select={select}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{endpoint}{queryUrl}"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

#docTotal total bruto:
#total neto = vatsum - docTotal
#DocumentLines agregar a la URL
