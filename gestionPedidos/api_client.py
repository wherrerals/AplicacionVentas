import requests
from django.conf import settings
from django.http import JsonResponse
from urllib.parse import quote


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
            "Password": settings.API_PASSWORD,
        }
        response = self.session.post(login_url, json=auth_data, verify=False)
        response.raise_for_status()

    def get_quotations(self, top=0, skip=0, filters=None):
        crossjoin = "Quotations,SalesPersons"
        expand = "Quotations($select=DocEntry,DocNum,CardCode,CardName,SalesPersonCode,DocDate,DocumentStatus,Cancelled,VatSum,DocTotal,DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeName)"
        filter_condition = "Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode"

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        headers = {
            "Prefer": f"odata.maxpagesize={top}"
        }

        query_url = f"/$crossjoin({crossjoin})?$expand={expand}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        print(url)
        return response.json()
    
    def get_quotations2(self, top=20, skip=0, filters=None):
        crossjoin = "Quotations,SalesPersons"
        expand = "Quotations($select=DocEntry,DocNum,CardCode,CardName,SalesPersonCode,DocDate,DocumentStatus,Cancelled,VatSum,DocTotal,DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeName)"
        filter_condition = "Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode"

        if filters:
            filter_condition += " and " + " and ".join([f"{k} {v}" for k, v in filters.items()])

        headers = {
            "Prefer": f"odata.maxpagesize={top}"
        }

        query_url = f"/$crossjoin({crossjoin})?$expand={expand}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        print(url)
        return response.json()

    
    def get_quotations_items(self, endpoint, top=20):
        
        select = "DocEntry,DocNum,CardName,DocDate,SalesPersonCode,Cancelled,DocTotal,VatSum,DocumentLines"
        skip=0

        headers = {
            "Prefer": f"odata.maxpagesize={top}"
        }

        queryUrl = f"?$select={select}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{endpoint}{queryUrl}"

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def post_data2(self, endpoint, data=None, headers=None):
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, headers=headers, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")

    def post_data(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, headers=headers, verify=True)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            error_msg = f"HTTP error occurred: {http_err}"
            print(error_msg)
            return {'error': error_msg}
        except requests.exceptions.ConnectionError as conn_err:
            error_msg = f"Connection error occurred: {conn_err}"
            print(error_msg)
            return {'error': error_msg}
        except requests.exceptions.Timeout as timeout_err:
            error_msg = f"Timeout error occurred: {timeout_err}"
            print(error_msg)
            return {'error': error_msg}
        except requests.exceptions.RequestException as req_err:
            error_msg = f"An error occurred: {req_err}"
            print(error_msg)
            return {'error': error_msg}
        except ValueError as json_err:
            error_msg = f"Error parsing JSON: {json_err}"
            print(error_msg)
            return {'error': error_msg}

    def get_orders(self, order_number):
        select = "DocEntry,DocNum,FolioNumber,U_ReportPdf,DocObjectCode,DocumentSubType"
        url = f"{self.base_url}Invoices?$select={select}&$filter=U_LED_NROPSH eq '{order_number}'"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        print(url)
        return response.json()