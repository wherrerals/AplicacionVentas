from shlex import quote
import requests
import json
from django.conf import settings
import logging
import re

from adapters.batch.batch_product import BatchProduct

logger = logging.getLogger(__name__)


class APIClient:
    """
    Una clase que representa el cliente de API para la capa de servicio.

    Atributos:
        base_url (str): La URL base para la API de la capa de servicio.
        session (requests.Session): Una sesión persistente para realizar solicitudes HTTP.
        autehnticated (bool): Estado de autenticación.

    Métodos:
        login(): Autentica la sesión con la API usando las credenciales proporcionadas.
        logout(): Cirra la sesión con la API
    """

    def __init__(self):
        """
        Inicializa una nueva instancia de APIClient.

        Configura la url base
        Crea una nueva sesión persistente.
        El estado de autenticación se establece en falso.
        Llama el metodo login para autenticar la sesión con la API.
        """

        self.base_url = settings.API_BASE_URL
        self.session = requests.Session()
        self.__autehnticated = False
        self.__login()

    def __login(self):
        """
        Construye la URL de inicio de sesión.

        Si la autenticacion es falsa, Autentica la sesión con la API usando las credenciales proporcionadas.
        Establece el estado de autenticación en True si la autenticación es exitosa.

        Raises:
            HTTPError: Si la respuesta HTTP contiene un error de estado.
        """
        login_url = f"{self.base_url}Login"

        if not self.__autehnticated:
            auth_data = {
                "CompanyDB": settings.COMPANY_DB,
                "UserName": settings.API_USERNAME,
                "Password": settings.API_PASSWORD,
            }
            response = self.session.post(login_url, json=auth_data, verify=False)
            response.raise_for_status()

            self.session_id = self.session.cookies.get("B1SESSION")

            self.__autehnticated = True

    def logout(self):
        """
        Construye la URL de fin de sesión.

        Si la autentincación es verdadera, finaliza la conexion de la API
        Establece el estado de autenticación en False si el cierre de sesión es exitoso.

        Raises:
            HTTPError: Si la respuesta HTTP contiene un error de estado.
        """
        if self.__autehnticated:
            logout_url = f"{self.base_url}Logout"
            response = self.session.post(logout_url, verify=False)
            response.raise_for_status()
            self.__autehnticated = False

    def getData(self, endpoint="", top=20, skip=0, filters=None):

        self.__login()
        crossjoin = f"{endpoint},SalesPersons"
        expand = f"{endpoint}($select=U_LED_TIPDEV,DocEntry,DocNum,CardCode,CardName,SalesPersonCode,DocDate,DocumentStatus,Cancelled,VatSum,DocTotal,DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeName)"
        order_by = f"DocNum desc"
        filter_condition = (
            f"{endpoint}/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        )

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        headers = {"Prefer": f"odata.maxpagesize={top}"}

        query_url = f"$crossjoin({crossjoin})?$expand={expand}&$orderby={order_by}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        print(f"URL Obtener Lista de {endpoint}: {url}")

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def obtenerProductos(self, endpoint="", top=20, skip=0, filters=None):
        """
        Recupera una lista de datos desde un endpoint específico con filtros opcionales, paginación y expansión.

        Parámetros:
            endpoint : str, opcional
                El endpoint desde donde recuperar los datos (por defecto es '').
            top : int, opcional
                El número máximo de registros a recuperar (por defecto es 0, lo que recupera todos los registros).
            skip : int, opcional
                El número de registros a omitir desde el inicio del conjunto de resultados (por defecto es 0).
            filters : dict, opcional
                Un diccionario de pares clave-valor para filtrar los resultados según condiciones específicas.

        Returns:

            dict
                Un diccionario con la respuesta de la API en formato JSON.
        """

        self.__login()
        crossjoin = f"{endpoint},SalesPersons"
        expand = f"{endpoint}($select=DocEntry,DocNum,CardCode,CardName,SalesPersonCode,DocDate,DocumentStatus,Cancelled,VatSum,DocTotal,DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeName)"
        filter_condition = (
            f"{endpoint}/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        )

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        headers = {"Prefer": f"odata.maxpagesize={top}"}

        query_url = f"$crossjoin({crossjoin})?$expand={expand}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def obtenerCotizacionesDE(self, endpoint, docEntry, top=20, skip=0):

        self.__login()

        crossjoin = (
            f"({endpoint},Quotations/DocumentLines,Items/ItemWarehouseInfoCollection)"
        )

        expand_fields = f"{endpoint}/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"

        filter_condition = f"{endpoint}/DocEntry eq {docEntry} and {endpoint}/DocumentLines/DocEntry eq {endpoint}/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq {endpoint}/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq Quotations/DocumentLines/WarehouseCode"

        # Construir la URL con el endpoint y la consulta
        queryUrl = (
            f"$crossjoin{crossjoin}?$expand={expand_fields}&$filter={filter_condition}"
            f"&$top={top}&$skip={skip}"
        )
        url = f"{self.base_url}{queryUrl}"
        try:
            response = self.session.get(
                url, headers={"Prefer": f"odata.maxpagesize={top}"}, verify=False
            )
            response.raise_for_status()  # Esto generará una excepción para cualquier código de estado HTTP 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud a la API: {e}")
            raise

    def get_orders(self, order_number):
        select = "DocEntry,DocNum,FolioNumber,U_ReportPdf,DocObjectCode,DocumentSubType"
        url = f"{self.base_url}Invoices?$select={select}&$filter=U_LED_NROPSH eq '{order_number}'"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def crearCotizacionSL(self, endpoint, data=None, headers=None):
        """
        permite la creacion de cotizaciones en la base de datos de SAP

        Parámetros:
            endpoint : str, opcional
                El endpoint donde se creara la cotizacion (por defecto es '').
            data : dict, opcional
                Un diccionario de pares clave-valor para crear la cotizacion.
            headers : dict, opcional
                Un diccionario de pares clave-valor para los encabezados de la solicitud.
        RETURNS:
            si la creacion de la cotizacion es exitosa retorna un diccionario con la respuesta de la API en formato JSON.
            si la creacion de la cotizacion no es exitosa retorna un diccionario con un mensaje de error.
            si la conexion con la API falla retorna un diccionario con un mensaje de error.
            si el tiempo de espera de la API se agota retorna un diccionario con un mensaje de error.
            si la respuesta de la API contiene un error de estado retorna un diccionario con un mensaje de error.
            si se produce un error al analizar JSON retorna un diccionario con un mensaje de error.
        """
        self.__login()
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, headers=headers, verify=False)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            try:
                error_message = response.json().get("error", "Error desconocido")
                return {"error": f"{error_message['message']['value']}"}
            except ValueError:  # Si la respuesta no es JSON
                error_message = response.text or "Error desconocido"
                error_value = error_message.get("message").get("value", "Error desconocido")  
            return {"error": f"{error_value}"}

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud a la API: {e}")
            raise

    def crearODV(self, data=None, headers=None):
        """
        permite la creacion de cotizaciones en la base de datos de SAP

        Parámetros:
            endpoint : str, opcional
                El endpoint donde se creara la cotizacion (por defecto es '').
            data : dict, opcional
                Un diccionario de pares clave-valor para crear la cotizacion.
            headers : dict, opcional
                Un diccionario de pares clave-valor para los encabezados de la solicitud.
        RETURNS:
            si la creacion de la cotizacion es exitosa retorna un diccionario con la respuesta de la API en formato JSON.
            si la creacion de la cotizacion no es exitosa retorna un diccionario con un mensaje de error.
            si la conexion con la API falla retorna un diccionario con un mensaje de error.
            si el tiempo de espera de la API se agota retorna un diccionario con un mensaje de error.
            si la respuesta de la API contiene un error de estado retorna un diccionario con un mensaje de error.
            si se produce un error al analizar JSON retorna un diccionario con un mensaje de error.
        """
        self.__login()
        url = f"{self.base_url}Orders"
        try:

            response = self.session.post(url, json=data, headers=headers, verify=False)
            response.raise_for_status()
            
            return response.json()

        except requests.exceptions.RequestException as e:
            raise

    def actualizarEstadoDocumentoSL(self, endpoint, docNum, estado):
        """
        Permite cambiar el estado de un documento en la base de datos de SAP.

        Parámetros:
            endpoint : str
                El endpoint donde se creará la cotización.
            docNum : int
                El número de documento a cambiar de estado.
            estado : str
                El estado al que se cambiará el documento.
        """
        self.__login()

        url = f"{self.base_url}{endpoint}({docNum})/{estado}"
        response = self.session.post(url, verify=False)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Intentar capturar el mensaje de error de la respuesta
            try:
                error_message = response.json().get("error", "Error desconocido")
            except ValueError:  # Si la respuesta no es JSON
                error_message = response.text or "Error desconocido"

            return {
                "error": f"Error al actualizar el estado del documento: {error_message}"
            }

        if response.status_code == 204:
            return {"message": "Estado actualizado correctamente"}
        elif response.status_code == 400:
            try:
                error_message = response.json().get(
                    "error", "Detalles no proporcionados"
                )
            except ValueError:
                error_message = response.text or "Detalles no proporcionados"

            return {"error": f"Error al actualizar el estado: {error_message}"}

    def verificarCliente(self, endpoint, cardCode):
        self.__login()

        select = "CardCode"
        url = f"{self.base_url}{endpoint}('{cardCode}')?$select={select}"
        response = self.session.get(url, verify=False)
        
        # Si la respuesta no fue exitosa, imprime los detalles del error
        if response.status_code != 200:
            print(f"Error HTTP: {response.status_code}")
            error_json = response.json()
            print(f"Mensaje de error: {error_json['error']['message']['value']}")
            return False

        return True
    
    def create_bp_sl(self, data):
        """
        permite la creacion de clientes en la base de datos de SAP

        Parámetros:
            data : dict, opcional
                Un diccionario de pares clave-valor para crear el cliente.
        returns:
            si la creacion del cliente es exitosa retorna un diccionario con la respuesta de la API en formato JSON.
            si la creacion del cliente no es exitosa retorna un diccionario con un mensaje de error.
            si la conexion con la API falla retorna un diccionario con un mensaje de error.
            si el tiempo de espera de la API se agota retorna un diccionario con un mensaje de error.
            si la respuesta de la API contiene un error de estado retorna un diccionario con un mensaje de error.
            si se produce un error al analizar JSON retorna un diccionario con un mensaje de error.
        """

        self.__login()
        url = f"{self.base_url}BusinessPartners"
        try:
            response = self.session.post(url, json=data, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud a la API: {e}")
            raise

    def getInfoSN(self, cardCode):
        #eliminar c, C, - y . del cardCode
        cardCode = cardCode.replace("C", "").replace("c", "").replace("-", "").replace(".", "").replace(" ", "").strip()
        card_code  = f"{cardCode}C"
        card_code_min = card_code.lower()

        details = f"BusinessPartners?$select=CardCode,CardName,CardType,Phone1,EmailAddress,Notes,GroupCode,FederalTaxID,BPAddresses,ContactEmployees&$filter=CardCode eq '{card_code}' or CardCode eq '{card_code_min}'"
        url = f"{self.base_url}{details}"
        
        try:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            # Normalizar respuesta si viene en formato "value"
            if "value" in data:
                if len(data["value"]) > 0:
                    return data["value"][0]
                else:
                    return {"error": True, "message": "No se encontró ningún BusinessPartner con ese código."}
            else:
                return data

        except requests.exceptions.HTTPError as http_err:
            return {"error": True, "message": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as req_err:
            return {"error": True, "message": f"Request error occurred: {req_err}"}
        except Exception as e:
            return {"error": True, "message": f"An unexpected error occurred: {e}"}



    def detalleCotizacionCliente(self, docEntry):
        """
        permite obtener el detalle de una cotizacion de un cliente en la base de datos de SAP

        Parámetros:
            docEntry : int, opcional
                El numero de documento de la cotizacion.
        """

        crossjoin = "Quotations,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Quotations($select=U_LED_COD_CUPON,DocEntry,DocNum, FederalTaxID, CardCode,CardName,TransportationCode,Address,Address2,DocDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Quotations/DocEntry eq {docEntry} and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def detalleCotizacionCliente2(self, docEntry):
        """
        permite obtener el detalle de una cotizacion de un cliente en la base de datos de SAP

        Parámetros:
            docEntry : int, opcional
                El numero de documento de la cotizacion.
        """

        crossjoin = "Quotations,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Quotations($select=U_LED_COD_CUPON,DocEntry,DocNum, FederalTaxID, CardCode,CardName,TransportationCode,Address,Address2,DocDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Quotations/DocEntry eq {docEntry} and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def detalleCotizacionLineas(self, docEntry: int) -> dict:
        crossJoin = (
            "Quotations,Quotations/DocumentLines,Items/ItemWarehouseInfoCollection"
        )

        expand = (
            "Quotations/DocumentLines("
            "$select=ItemCode,U_LED_DCTO_CUPON,TreeType,DocEntry,LineNum,"
            "ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,"
            "DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,"
            "ShipDate,Address,ShippingMethod,FreeText,BaseType,"
            "GrossBuyPrice,BaseEntry,BaseLine,LineStatus"
            "),"
            "Items/ItemWarehouseInfoCollection("
            "$select=WarehouseCode,InStock,Committed,"
            "InStock sub Committed as SalesStock"
            ")"
        )

        filter_ = (
            f"Quotations/DocEntry eq {docEntry} and "
            "Quotations/DocumentLines/DocEntry eq Quotations/DocEntry and "
            "Items/ItemWarehouseInfoCollection/ItemCode eq Quotations/DocumentLines/ItemCode and "
            "Items/ItemWarehouseInfoCollection/WarehouseCode eq Quotations/DocumentLines/WarehouseCode"
        )

        orderby = "Quotations/DocumentLines/LineNum"

        url = (
            f"{self.base_url}/$crossjoin({crossJoin})"
            f"?$expand={expand}&$filter={filter_}&$orderby={orderby}"
        )

        all_data = []
        seen = set()

        while url:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            for row in data.get("value", []):
                dl = row.get("Quotations/DocumentLines", {})
                key = (
                    dl.get("DocEntry"),
                    dl.get("LineNum"),
                    dl.get("ItemCode"),
                    dl.get("WarehouseCode"),
                )
                if key not in seen:
                    seen.add(key)
                    all_data.append(row)

            next_link = data.get("odata.nextLink")
            url = f"{self.base_url}/{next_link.lstrip('/')}" if next_link else None

        return {"value": all_data}




    def detallesOrdenVentaCliente(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "Orders,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Orders($select=U_LED_COD_CUPON,DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Orders/DocEntry eq {docEntry} and Orders/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Orders/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    
    # solucion temporal 
    def detallesOrdenVentaCliente2(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "Orders,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Orders($select=U_LED_COD_CUPON,DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Orders/DocEntry eq {docEntry} and Orders/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    

    def detallesOrdenVentaCliente(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "Orders,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Orders($select=U_LED_COD_CUPON,DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Orders/DocEntry eq {docEntry} and Orders/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Orders/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    

    def detallesOrdenVentaLineas(self, docEntry: int) -> dict:
        crossJoin = (
            "Orders,Orders/DocumentLines,Items/ItemWarehouseInfoCollection"
        )

        expand = (
            "Orders/DocumentLines("
            "$select=ItemCode,U_LED_DCTO_CUPON,TreeType,DocEntry,LineNum,"
            "ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,"
            "DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,"
            "ShipDate,Address,ShippingMethod,FreeText,BaseType,"
            "GrossBuyPrice,BaseEntry,BaseLine,LineStatus"
            "),"
            "Items/ItemWarehouseInfoCollection("
            "$select=WarehouseCode,InStock,Committed,"
            "InStock sub Committed as SalesStock"
            ")"
        )

        filter_ = (
            f"Orders/DocEntry eq {docEntry} and "
            "Orders/DocumentLines/DocEntry eq Orders/DocEntry and "
            "Items/ItemWarehouseInfoCollection/ItemCode eq Orders/DocumentLines/ItemCode and "
            "Items/ItemWarehouseInfoCollection/WarehouseCode eq Orders/DocumentLines/WarehouseCode"
        )

        orderby = "Orders/DocumentLines/LineNum"

        url = (
            f"{self.base_url}/$crossjoin({crossJoin})"
            f"?$expand={expand}&$filter={filter_}&$orderby={orderby}"
        )

        all_data = []
        seen = set()

        while url:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            for row in data.get("value", []):
                dl = row.get("Orders/DocumentLines", {})
                key = (
                    dl.get("DocEntry"),
                    dl.get("LineNum"),
                    dl.get("ItemCode"),
                    dl.get("WarehouseCode"),
                )
                if key not in seen:
                    seen.add(key)
                    all_data.append(row)

            next_link = data.get("odata.nextLink")
            url = f"{self.base_url}/{next_link.lstrip('/')}" if next_link else None

        return {"value": all_data}
    
    # solucion temporal 
    def detallesRR(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "ReturnRequest,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "ReturnRequest($select=DocEntry,DocNum,U_VK_Folio,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_TIPDEV,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"ReturnRequest/DocEntry eq {docEntry} and ReturnRequest/SalesPersonCode eq SalesPersons/SalesEmployeeCode and ReturnRequest/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        print(url)

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    
    def detallesRR2(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDEV,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "ReturnRequest,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "ReturnRequest($select=DocEntry,DocNum,U_VK_Folio,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"ReturnRequest/DocEntry eq {docEntry} and ReturnRequest/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        print(url)

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def detallesRRlineas(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(ReturnRequest,ReturnRequest/DocumentLines,Items/ItemWarehouseInfoCollection)?$expand=ReturnRequest/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)
        &$filter=ReturnRequest/DocEntry eq 201882 and ReturnRequest/DocumentLines/DocEntry eq ReturnRequest/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq ReturnRequest/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq ReturnRequest/DocumentLines/WarehouseCode
        """

        crossJoin = (
            "ReturnRequest,ReturnRequest/DocumentLines,Items/ItemWarehouseInfoCollection"
            )
        
        expand = "ReturnRequest/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"
        filter = f"ReturnRequest/DocEntry eq {docEntry} and ReturnRequest/DocumentLines/DocEntry eq ReturnRequest/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq ReturnRequest/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq ReturnRequest/DocumentLines/WarehouseCode"

        base_url = self.base_url # Asegura que no haya doble "/"
        url = f"{base_url}/$crossjoin({crossJoin})?$expand={expand}&$filter={filter}"

        all_data = []  # Lista para almacenar todos los valores

        while url:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            # Agregar los resultados actuales a la lista acumulada
            all_data.extend(data.get("value", []))

            # Obtener el próximo enlace si existe
            next_link = data.get("odata.nextLink")
            url = f"{base_url}/{next_link}" if next_link else None  # Agregar base_url si es necesario

        return {"value": all_data}

    def getDataSN(self, top=20, skip=0, filters=None):
        """
        Recupera datos de socios de negocio desde la API con filtros opcionales.
        """
        self.__login()
        select = f"CardCode,CardName,CardType,Phone1,EmailAddress,GroupCode"
        order_by = f"CardName desc"
        filter_condition = f"CardType eq 'cCustomer'"

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key}, {value}"

        headers = {"Prefer": f"odata.maxpagesize={top}"}

        query_url = f"BusinessPartners?$select={select}&$orderby={order_by}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def actualizarSocioNegocioSL(self, cardCode, data):
        """
        Actualiza un socio de negocio en SAP Business One.
        """
        self.__login()

        url = f"{self.base_url}BusinessPartners('{cardCode}')"
        response = self.session.patch(url, data, verify=False)

        # Manejar la respuesta según el código de estado
        if response.status_code == 204:
            return {
                "success": True,
                "message": "Socio de negocio actualizado correctamente.",
            }
        
        else:
           error_data = response.json()
           error_message = error_data.get('error', {}).get('message', {}).get('value', 'Error desconocido')

           return {
                "error": True,
                "message": f"Respuesta error SAP: {error_message}",
            }
    
    
    def obtenerProductosSL(self, skip=0, tipo="nacional"):

        self.__login()
        select = "ItemCode,ItemName,TreeType,SalesItem,InventoryItem,AvgStdPrice,U_LED_MARCA,U_LED_ARTDESC,Frozen,UpdateDate,UpdateTime,ItemPrices,ItemWarehouseInfoCollection"
        if tipo == "nacional":
            filter = "SalesItem eq 'tYES' and U_Origin eq 'N' and TreeType eq 'iNotATree' and U_LED_SYNC eq 1"
        elif tipo == "importado":
            filter = "SalesItem eq 'tYES' and U_Origin ne 'N' and TreeType eq 'iNotATree' and U_LED_SYNC eq 1"
        else:
            filter = "SalesItem eq 'tYES' and TreeType ne 'iNotATree' and U_LED_SYNC eq 1"        
        
        order_by = "ItemCode asc"

        url = f"{self.base_url}Items?$select={select}&$filter={filter}&$orderby={order_by}&$skip={skip}"
        
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def elementosReceta(self, itemCode):

        self.__login()
        select = "ItemCode,ItemName,TreeType,SalesItem,InventoryItem,AvgStdPrice,U_LED_MARCA,UpdateDate,UpdateTime,ItemPrices,ItemWarehouseInfoCollection"
        filter = f"ItemCode eq '{itemCode}' and SalesItem eq 'tYES'"
        order_by = "ItemCode asc"

        url = f"{self.base_url}Items?$select={select}&$filter={filter}&$orderby={order_by}"

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def productTree(self, itemCode):

        url = f"{self.base_url}ProductTrees('{itemCode}')"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def getODV(self, top=20, skip=0, filters=None):

        self.__login()
        crossjoin = f"Orders,SalesPersons"
        expand = f"Orders($select=DocEntry,DocNum,CardCode,CardName,SalesPersonCode,DocDate,DocumentStatus,Cancelled,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeName)"
        order_by = f"DocNum desc"
        filter_condition = f"Orders/SalesPersonCode eq SalesPersons/SalesEmployeeCode"

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        headers = {"Prefer": f"odata.maxpagesize={top}"}

        query_url = f"$crossjoin({crossjoin})?$expand={expand}&$orderby={order_by}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    # usando patch actualizar las cotizaciones
    def actualizarCotizacionesSL(self, docEntry, data):
        self.__login()
        url = f"{self.base_url}Quotations({docEntry})"

        # Definir los encabezados, incluyendo el encabezado B1S-ReplaceCollectionsOnPatch
        headers = {
            "B1S-ReplaceCollectionsOnPatch": "true",  # Encabezado adicional
            "Content-Type": "application/json",  # Asegúrate de incluir este encabezado si es necesario
            "Cookie": f"B1SESSION={self.session_id}",  # <- Aquí agregas la cookie
        }

        try:

            response = self.session.patch(url, json=data, headers=headers, verify=False)
            if response.status_code == 204:
                return {
                    "success": True,
                    "message": "Cotización actualizada correctamente.",
                }
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la solicitud a la API: {e}")
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")
            raise

    # usando patch actualizar las cotizaciones
    def actualizarDevolucionesSL(self, docEntry, data):
        self.__login()
        url = f"{self.base_url}ReturnRequest({docEntry})"

        # Definir los encabezados, incluyendo el encabezado B1S-ReplaceCollectionsOnPatch
        headers = {
            "B1S-ReplaceCollectionsOnPatch": "true",  # Encabezado adicional
            "Content-Type": "application/json",  # Asegúrate de incluir este encabezado si es necesario
            "Cookie": f"B1SESSION={self.session_id}",  # <- Aquí agregas la cookie
        }

        try:

            response = self.session.patch(url, json=data, headers=headers, verify=False)
            if response.status_code == 204:
                return {
                    "success": True,
                    "message": "Cotización actualizada correctamente.",
                }
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la solicitud a la API: {e}")
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")
            raise

    def actualizarODVSL(self, docEntry, data):
        self.__login()
        url = f"{self.base_url}Orders({docEntry})"

        # Definir los encabezados, incluyendo el encabezado B1S-ReplaceCollectionsOnPatch
        headers = {
            "B1S-ReplaceCollectionsOnPatch": "true",  # Encabezado adicional
            "Content-Type": "application/json",  # Asegúrate de incluir este encabezado si es necesario
            "Cookie": f"B1SESSION={self.session_id}",  # <- Aquí agregas la cookie

        }

        try:
            # Hacer la solicitud PATCH incluyendo los encabezados
            response = self.session.patch(url, json=data, headers=headers, verify=False)

            if response.status_code == 204:
                return {
                    "success": True,
                    "message": "Cotización actualizada correctamente.",
                }
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la solicitud a la API: {e}")
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")
            raise

    def actualizarDevolucionesSL(self, docEntry, data):
        self.__login()
        url = f"{self.base_url}ReturnRequest({docEntry})"

        # Definir los encabezados, incluyendo el encabezado B1S-ReplaceCollectionsOnPatch
        headers = {
            "B1S-ReplaceCollectionsOnPatch": "true",  # Encabezado adicional
            "Content-Type": "application/json",  # Asegúrate de incluir este encabezado si es necesario
            "Cookie": f"B1SESSION={self.session_id}",  # <- Aquí agregas la cookie
        }

        try:
            # Hacer la solicitud PATCH incluyendo los encabezados
            response = self.session.patch(url, json=data, headers=headers, verify=False)

            if response.status_code == 204:
                return {
                    "success": True,
                    "message": "Cotización actualizada correctamente.",
                }
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la solicitud a la API: {e}")
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")
            raise

    def actualizarDireccionSL(self, cardCode, data):
        self.__login()
        url = f"{self.base_url}BusinessPartners('{cardCode}')"

        headers = {
            "B1S-ReplaceCollectionsOnPatch": "true",  # Encabezado adicional
            "Content-Type": "application/json",  # Asegúrate de incluir este encabezado si es necesario
            "Cookie": f"B1SESSION={self.session_id}",  # <- Aquí agregas la cookie
        }

        try:

            response = self.session.patch(url, json=data, headers=headers, verify=False)

            if response.status_code == 204:
                return {
                    "success": True,
                    "message": "Dirección actualizada correctamente.",
                }
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la solicitud a la API: {e}")
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")
            raise

    def actualizarContactosSL(self, cardCode, data):
        self.__login()
        url = f"{self.base_url}BusinessPartners('{cardCode}')"

        headers = {
            #"B1S-ReplaceCollectionsOnPatch": "true",  # Encabezado adicional
            "Content-Type": "application/json",  # Asegúrate de incluir este encabezado si es necesario
            "Cookie": f"B1SESSION={self.session_id}",  # <- Aquí agregas la cookie
        }
        try:
            response = self.session.patch(url, json=data, headers=headers, verify=False)

            if response.status_code == 204:
                return {
                    "success": True,
                    "message": "Contacto actualizado correctamente.",
                }
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error en la solicitud a la API: {e}")
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")
            raise

    def obtenerDataSn(self, cardCode, tipo):

        details = f"BusinessPartners('{cardCode}')/{tipo}"
        url = f"{self.base_url}{details}"

        response = self.session.get(url, verify=False)  # Se realiza la solicitud GET
        response.raise_for_status()  # Esto generará una excepción para cualquier código de estado HTTP 4xx/5xx
        return response.json()

    def contarProductos(self, tipo=""):
        self.__login()
        
        if tipo == "nacional":
            filter = "SalesItem eq 'tYES' and U_Origin eq 'N' and TreeType eq 'iNotATree' and U_LED_SYNC eq 1"
        elif tipo == "importado":
            filter = "SalesItem eq 'tYES' and U_Origin ne 'N' and TreeType eq 'iNotATree' and U_LED_SYNC eq 1"
        else:
            filter = "SalesItem eq 'tYES' and TreeType ne 'iNotATree' and U_LED_SYNC eq 1"        
        
        url = f"{self.base_url}Items?$apply=aggregate($count as ItemsCount)&$filter={filter}"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def getQuantityBusinessPartners(self):
        self.__login()
        url = f"{self.base_url}BusinessPartners?$apply=aggregate($count as BusinessPartners)&$filter=CardType eq 'cCustomer'"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def getBusinessPartners(self, skip=0):
        self.__login()
        url = f"{self.base_url}BusinessPartners?$select=CardCode,CardName,CardType,Phone1,EmailAddress,Notes,GroupCode,FederalTaxID,BPAddresses,ContactEmployees&$filter=CardType eq 'cCustomer'&$skip={skip}"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def productTreesComponents(self, itemCode):
        url = f"{self.base_url}ProductTrees('{itemCode}')"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def urlPrueba(self, codigo, skip=0):

        self.__login()
        adicionales = f"Items('{codigo}')?$select=ItemCode,ItemName,TreeType,SalesItem,InventoryItem,AvgStdPrice,U_LED_MARCA,UpdateDate,UpdateTime,ItemPrices,ItemWarehouseInfoCollection&$filter=SalesItem eq 'tYES'&$orderby=ItemCode asc"

        url = f"{self.base_url}{adicionales}"

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def prueba(self, skip=0):

        self.__login()
        select = "ItemCode,ItemName,TreeType,SalesItem,InventoryItem,AvgStdPrice,U_LED_MARCA,UpdateDate,UpdateTime,ItemPrices,ItemWarehouseInfoCollection"
        filter = "SalesItem eq 'tYES' and TreeType eq 'iSalesTree'"
        order_by = "ItemCode asc"

        url = f"{self.base_url}Items?$select={select}&$filter={filter}&$orderby={order_by}&$skip={skip}"

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    
    def get_sales_sl(self, filter=None, type_document=None):

        self.__login()
        cross_join = f"{type_document},SalesPersons"
        expand = f"{type_document}($select=DocEntry,DocNum,DocObjectCode,DocumentSubType,ReserveInvoice,FolioNumber,CardCode,CardName,SalesPersonCode,DocDate,DocumentStatus,Cancelled,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeName)&$orderby=DocNum desc"

        url = f"{self.base_url}$crossjoin({cross_join})?$expand={expand}&$filter=Invoices/SalesPersonCode eq SalesPersons/SalesEmployeeCode and {filter}"

        response = self.session.get(url, verify=False)

        response.raise_for_status()
        return response.json()
    
    


    def bacth_processes_products(self, listItems):
        body, boundary, changeset_boundary = BatchProduct.generate_batch(listItems)
        headers = {"Content-Type": f"multipart/mixed;boundary={boundary}"}

        batch_response = self.session.post(
            f"{self.base_url}/$batch",
            data=body,
            headers=headers,
            verify=False
        )

        print(f"Batch response status: {batch_response.status_code}")

        if batch_response.status_code != 202:
            print("❌ El batch request falló antes de procesarse.")
            print(batch_response.text)
            return False

        # --- Extrae las respuestas individuales ---
        responses = self._parse_batch_response(batch_response.text)

        print("\n📦 Resultados individuales:")
        for i, resp in enumerate(responses, start=1):
            print(f"\n➡️  Respuesta #{i}")
            print(f"Status: {resp['status']}")
            print(f"Body: {resp['body']}\n")

        return True


    def _parse_batch_response(self, raw_response: str):
        """
        Analiza el multipart/mixed devuelto por un batch OData.
        Retorna una lista de dicts con 'status' y 'body'.
        """
        # Detecta los boundaries del changeset
        boundaries = re.findall(r'--changeset_[^\n\r]+', raw_response)
        if not boundaries:
            # fallback si no hay changeset
            boundaries = re.findall(r'--batch_[^\n\r]+', raw_response)

        parts = re.split(r'--changeset_[^\n\r]+', raw_response)
        results = []

        for part in parts:
            # Busca el status line
            match_status = re.search(r'HTTP/1\.1\s+(\d+)\s+([^\n\r]+)', part)
            if match_status:
                status_code = int(match_status.group(1))
                status_text = match_status.group(2).strip()

                # Extrae cuerpo JSON o texto
                match_body = re.search(r'\{[\s\S]+\}', part)
                body = match_body.group(0).strip() if match_body else "(sin cuerpo)"

                results.append({
                    "status": f"{status_code} {status_text}",
                    "body": body
                })

        return results

    
    
    def get_docEntry_sl(self, type_document, doc_num):

        order_by = f"DocDate desc"
        select = f"$select=DocEntry&$orderby={order_by}&$filter=DocNum eq {doc_num}"
        url = f"{self.base_url}{type_document}?{select}"

        response = self.session.get(url, verify=False)

        if response.status_code == 200:
            data = response.json()
            if 'value' in data and len(data['value']) > 0:
                doc_entry = data['value'][0].get('DocEntry')
                return doc_entry
        
        # Si algo falló o no se encontró el documento
        return None

    def sales_details_sl_bp(self, type_document, docEntry):

        crossjoin = f"{type_document},SalesPersons,BusinessPartners/ContactEmployees"
        expand = f"{type_document}($select=DocumentSubType,ReserveInvoice,FolioNumber,DocEntry,DocNum, FederalTaxID, CardCode,CardName,TransportationCode,Address,Address2,DocDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"{type_document}/DocEntry eq {docEntry} and {type_document}/SalesPersonCode eq SalesPersons/SalesEmployeeCode and {type_document}/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"
        
        url = (f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}")

        response = self.session.get(url, verify=False)
        response.raise_for_status()

        data_sales = response.json()

        if 'value' in data_sales and len(data_sales['value']) > 0:
            return data_sales['value'][0]
        else:
            filter = f"{type_document}/DocEntry eq {docEntry} and {type_document}/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
            url = (f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}")
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data_sales = response.json()
            return data_sales['value'][0]

    def sales_details_sl_lines(self, type_document, docEntry):
        crossJoin = (f"{type_document},{type_document}/DocumentLines,Items/ItemWarehouseInfoCollection")
        expand = f"{type_document}/DocumentLines($select=TreeType,DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"
        filter = f"{type_document}/DocEntry eq {docEntry} and {type_document}/DocumentLines/DocEntry eq {type_document}/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq {type_document}/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq {type_document}/DocumentLines/WarehouseCode"

        base_url = self.base_url
        url = f"{base_url}/$crossjoin({crossJoin})?$expand={expand}&$filter={filter}"

        all_data = []

        while url:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            all_data.extend(data.get("value", []))

            next_link = data.get("odata.nextLink")
            url = f"{base_url}/{next_link}" if next_link else None  
        return {"value": all_data}


    def lines_details(self, docEntry, type_document):
        crossJoin = (
            f"{type_document},{type_document}/DocumentLines,Items/ItemWarehouseInfoCollection"
        )
        
        expand = f"{type_document}/DocumentLines($select=DocEntry,LineNum,ItemCode,TreeType,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"
        filter = f"{type_document}/DocEntry eq {docEntry} and {type_document}/DocumentLines/DocEntry eq {type_document}/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq {type_document}/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq {type_document}/DocumentLines/WarehouseCode"

        base_url = self.base_url # Asegura que no haya doble "/"
        url = f"{base_url}/$crossjoin({crossJoin})?$expand={expand}&$filter={filter}"

        all_data = []  # Lista para almacenar todos los valores

        while url:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()

            # Agregar los resultados actuales a la lista acumulada
            all_data.extend(data.get("value", []))

            # Obtener el próximo enlace si existe
            next_link = data.get("odata.nextLink")
            url = f"{base_url}/{next_link}" if next_link else None  # Agregar base_url si es necesario

        return {"value": all_data}


    # usando patch actualizar las cotizaciones
    def update_recipe_ingredients_sl(self, docEntry, data, type_document):
        self.__login()
        url = f"{self.base_url}{type_document}({docEntry})"

        headers = {
            "Content-Type": "application/json",  # Asegúrate de incluir este encabezado si es necesario
            "Cookie": f"B1SESSION={self.session_id}",  # <- Aquí agregas la cookie
        }

        try:
            response = self.session.patch(url, json=data, headers=headers, verify=False)
            
            if response.status_code == 204:
            
                return {
                    "success": True,
                    "message": "Cotización actualizada correctamente.",
                }
            
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")


    def get_sales_or_orders(self, card_code):
        self.__login()
        #quitar C o c a el cardcode
        card_code = card_code.replace("C", "").replace("c", "")
        crossjoin = "(Invoices,SalesPersons)"
        expand = "Invoices($select=DocEntry)&$filter=Invoices/SalesPersonCode eq SalesPersons/SalesEmployeeCode "
        query = f"and (Invoices/CardCode eq '{card_code}C' or Invoices/CardCode eq '{card_code}c' or contains(Invoices/CardCode, '{card_code}'))&$top=1"
        url = f"{self.base_url}$crossjoin{crossjoin}?$expand={expand}{query}"

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        
        # Retorna el conteo de resultados
        return len(data.get("value", []))