import requests
import json
from django.conf import settings
import logging

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
            self.__autehnticated = True
            return print('Autenticado con exito')
    
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
        order_by = f"DocNum desc"
        filter_condition = f"{endpoint}/SalesPersonCode eq SalesPersons/SalesEmployeeCode"

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        headers = {
            "Prefer": f"odata.maxpagesize={top}"
        }

        query_url = f"$crossjoin({crossjoin})?$expand={expand}&$orderby={order_by}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        print(url)
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
        filter_condition = f"{endpoint}/SalesPersonCode eq SalesPersons/SalesEmployeeCode"

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        headers = {
            "Prefer": f"odata.maxpagesize={top}"
        }

        query_url = f"$crossjoin({crossjoin})?$expand={expand}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

        response = self.session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        print(url)
        return response.json()

    
    
    def obtenerCotizacionesDE(self, endpoint, docEntry, top=20, skip=0):
        
        self.__login()

        crossjoin = f"({endpoint},Quotations/DocumentLines,Items/ItemWarehouseInfoCollection)"

        expand_fields = (f"{endpoint}/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)")
        
        filter_condition = f"{endpoint}/DocEntry eq {docEntry} and {endpoint}/DocumentLines/DocEntry eq {endpoint}/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq {endpoint}/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq Quotations/DocumentLines/WarehouseCode"

        # Construir la URL con el endpoint y la consulta
        queryUrl = (
            f"$crossjoin{crossjoin}?$expand={expand_fields}&$filter={filter_condition}"
            f"&$top={top}&$skip={skip}"
        )
        url = f"{self.base_url}{queryUrl}"
        print (url)
        try:
            response = self.session.get(url, headers={"Prefer": f"odata.maxpagesize={top}"}, verify=False)
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
        print(url)
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

        # Imprimir el JSON y los headers para ver qué se está enviando
            print(f"URL: {url}")
            print(f"Data being sent: {json.dumps(data, indent=4)}")

            response = self.session.post(url, json=data, headers=headers, verify=False)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud a la API: {e}")
            raise
    
    def actualizarEstadoDocumentoSL(self, endpoint, docNum, estado):
        """
        permite cambiar el estado de un documento en la base de datos de SAP

        Parámetros:
            endpoint : str, opcional
                El endpoint donde se creara la cotizacion (por defecto es '').
            docNum : int, opcional
                El numero de documento a cambiar de estado.
            estado : str, opcional
                El estado al que se cambiara el documento.
        """

        print(f"Endpoint: {endpoint}")
        print(f"DocNum: {docNum}")
        print(f"Estado: {estado}")
        self.__login()

        url = f"{self.base_url}{endpoint}({docNum})/{estado}"
        response = self.session.post(url, verify=False)
        response.raise_for_status()

        print(response)
        print(url)
        if response.status_code == 204:
            return {'message': 'Estado actualizado correctamente'}
        
    
    def verificarCliente(self, endpoint, cardCode):
        """
        Verifica si un cliente existe en la base de datos de SAP

        Parámetros:
            endpoint : str, opcional
                El endpoint donde se creara la cotizacion (por defecto es '').
            cardCode : str, opcional
                El codigo de cliente a verificar.
        """
        print("Probando la conexión con la API...")

        self.__login()
        select = "CardCode"
        url = f"{self.base_url}{endpoint}('{cardCode}')?$select={select}"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
        print(url)
        print(response)

        return response.json()

    def crearCliente(self, data):
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
        print("Probando la conexión con la API...")
        print(f"CardCode: {cardCode}")
        print("*" * 50)
        details = f"BusinessPartners('{cardCode}')?$select=CardCode,CardName,CardType,Phone1,EmailAddress,Notes,GroupCode,FederalTaxID,BPAddresses,ContactEmployees"
        url = f"{self.base_url}{details}"
        response = self.session.get(url, verify=False) # Se realiza la solicitud GET
        response.raise_for_status() # Esto generará una excepción para cualquier código de estado HTTP 4xx/5xx
        
        print(url)
        return response.json()
    
    def detalleCotizacionCliente(self, docEntry):
        """
        permite obtener el detalle de una cotizacion de un cliente en la base de datos de SAP

        Parámetros:
            docEntry : int, opcional
                El numero de documento de la cotizacion.
        """

        crossjoin = "Quotations,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Quotations/DocEntry eq {docEntry} and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"    
        url = f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"

        print(url)

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    

    def detalleCotizacionLineas(self, docEntry):
        """
        Permite obtener el detalle de las lineas de una cotizacion en la base de datos de SAP

        Parámetros:
            docEntry : int, opcional
                El numero de documento de la cotizacion.

        """

        crossJoin = "Quotations,Quotations/DocumentLines,Items/ItemWarehouseInfoCollection"
        expand = "Quotations/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"
        filter = f"Quotations/DocEntry eq {docEntry} and Quotations/DocumentLines/DocEntry eq Quotations/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq Quotations/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq Quotations/DocumentLines/WarehouseCode"

        url = f"{self.base_url}$crossjoin({crossJoin})?$expand={expand}&$filter={filter}"

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    