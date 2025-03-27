from shlex import quote
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
        filter_condition = (
            f"{endpoint}/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        )

        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        headers = {"Prefer": f"odata.maxpagesize={top}"}

        query_url = f"$crossjoin({crossjoin})?$expand={expand}&$orderby={order_by}&$filter={filter_condition}&$top={top}&$skip={skip}"
        url = f"{self.base_url}{query_url}"

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
        """
        Verifica si un cliente existe en la base de datos de SAP

        Parámetros:
            endpoint : str, opcional
                El endpoint donde se creara la cotizacion (por defecto es '').
            cardCode : str, opcional
                El codigo de cliente a verificar.
        """
        self.__login()
        select = "CardCode"
        url = f"{self.base_url}{endpoint}('{cardCode}')?$select={select}"
        response = self.session.get(url, verify=False)
        response.raise_for_status()
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
        details = f"BusinessPartners('{cardCode}')?$select=CardCode,CardName,CardType,Phone1,EmailAddress,Notes,GroupCode,FederalTaxID,BPAddresses,ContactEmployees"
        url = f"{self.base_url}{details}"
        
        try:

            response = self.session.get(url, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Captura errores HTTP (como 404, 500, etc.)
            error_message = f"HTTP error occurred: {http_err}"
            return {"error": True, "message": error_message, "status_code": response.status_code}
        except requests.exceptions.RequestException as req_err:
            # Captura otros errores relacionados con la solicitud (como problemas de conexión)
            error_message = f"Request error occurred: {req_err}"
            return {"error": True, "message": error_message}
        except Exception as e:
            # Captura cualquier otra excepción inesperada
            error_message = f"An unexpected error occurred: {e}"
            return {"error": True, "message": error_message}


    def detalleCotizacionCliente(self, docEntry):
        """
        permite obtener el detalle de una cotizacion de un cliente en la base de datos de SAP

        Parámetros:
            docEntry : int, opcional
                El numero de documento de la cotizacion.
        """

        crossjoin = "Quotations,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Quotations($select=DocEntry,DocNum, FederalTaxID, CardCode,CardName,TransportationCode,Address,Address2,DocDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
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
        expand = "Quotations($select=DocEntry,DocNum, FederalTaxID, CardCode,CardName,TransportationCode,Address,Address2,DocDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Quotations/DocEntry eq {docEntry} and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()

    def detalleCotizacionLineas(self, docEntry):
        """
        Obtiene el detalle de las líneas de una cotización en SAP,
        iterando sobre los resultados paginados hasta obtener todos los registros.

        Parámetros:
            docEntry : int
                Número de documento de la cotización.

        Retorna:
            dict: Respuesta consolidada con todas las líneas de la cotización.
        """
        crossJoin = (
            "Quotations,Quotations/DocumentLines,Items/ItemWarehouseInfoCollection"
        )
        
        expand = "Quotations/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"
        filter = f"Quotations/DocEntry eq {docEntry} and Quotations/DocumentLines/DocEntry eq Quotations/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq Quotations/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq Quotations/DocumentLines/WarehouseCode"

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



    def detallesOrdenVentaCliente(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "Orders,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "Orders($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
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
        expand = "Orders($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
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
        expand = "Orders($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"Orders/DocEntry eq {docEntry} and Orders/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Orders/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    
    def detallesOrdenVentaLineas(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Orders,Orders/DocumentLines,Items/ItemWarehouseInfoCollection)?$expand=Orders/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)
        &$filter=Orders/DocEntry eq 201882 and Orders/DocumentLines/DocEntry eq Orders/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq Orders/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq Orders/DocumentLines/WarehouseCode
        """

        crossJoin = (
            "Orders,Orders/DocumentLines,Items/ItemWarehouseInfoCollection"
            )
        
        expand = "Orders/DocumentLines($select=DocEntry,LineNum,ItemCode,ItemDescription,WarehouseCode,Quantity,UnitPrice,GrossPrice,DiscountPercent,Price,PriceAfterVAT,LineTotal,GrossTotal,ShipDate,Address,ShippingMethod,FreeText,BaseType,GrossBuyPrice,BaseEntry,BaseLine,LineStatus),Items/ItemWarehouseInfoCollection($select=WarehouseCode,InStock,Committed,InStock sub Committed as SalesStock)"
        filter = f"Orders/DocEntry eq {docEntry} and Orders/DocumentLines/DocEntry eq Orders/DocEntry and Items/ItemWarehouseInfoCollection/ItemCode eq Orders/DocumentLines/ItemCode and Items/ItemWarehouseInfoCollection/WarehouseCode eq Orders/DocumentLines/WarehouseCode"

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
    
    # solucion temporal 
    def detallesRR(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "ReturnRequest,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "ReturnRequest($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"ReturnRequest/DocEntry eq {docEntry} and ReturnRequest/SalesPersonCode eq SalesPersons/SalesEmployeeCode and ReturnRequest/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

        response = self.session.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    
    def detallesRR2(self, docEntry):
        """
        https://182.160.29.24:50003/b1s/v1/$crossjoin(Quotations,SalesPersons,BusinessPartners/ContactEmployees)?$expand=Quotations($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address, Address2,DocDate,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal, DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)
        &$filter=Quotations/DocEntry eq 165332 and Quotations/SalesPersonCode eq SalesPersons/SalesEmployeeCode and Quotations/ContactPersonCode eq BusinessPartners/ContactEmployees/InternalCode
        """
        crossjoin = "ReturnRequest,SalesPersons,BusinessPartners/ContactEmployees"
        expand = "ReturnRequest($select=DocEntry,DocNum,CardCode,CardName,TransportationCode,Address,Address2,DocDate,DocDueDate,Comments,DocumentStatus,Cancelled,U_LED_TIPVTA,U_LED_TIPDOC,U_LED_NROPSH,NumAtCard,VatSum,DocTotal,  DocTotal sub VatSum as DocTotalNeto),SalesPersons($select=SalesEmployeeCode,SalesEmployeeName,U_LED_SUCURS),BusinessPartners/ContactEmployees($select=InternalCode,FirstName)"
        filter = f"ReturnRequest/DocEntry eq {docEntry} and ReturnRequest/SalesPersonCode eq SalesPersons/SalesEmployeeCode"
        url = (
            f"{self.base_url}$crossjoin({crossjoin})?$expand={expand}&$filter={filter}"
        )

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

        try:
            # Enviar la solicitud PATCH a la API
            response = self.session.patch(url, data, verify=False)

            # Manejar la respuesta según el código de estado
            if response.status_code == 204:
                # Si la respuesta es 204, no hay contenido en la respuesta, pero la operación fue exitosa

                return {
                    "success": True,
                    "message": "Socio de negocio actualizado correctamente.",
                }
            else:
                # Si la respuesta tiene contenido (por ejemplo, 200 OK o 201 Created), procesar la respuesta
                response.raise_for_status()  # Lanzar un error si la respuesta no es exitosa
                return response.json()

        except requests.exceptions.HTTPError as e:
            # Si ocurre un error en la solicitud, imprimir y lanzar la excepción
            if "response" in locals() and response is not None:
                print(f"Cuerpo de la respuesta del servidor: {response.text}")
            raise
        except Exception as e:
            # Capturar otros posibles errores y registrarlos
            print(f"Error inesperado: {e}")
            raise

    def obtenerProductosSL(self, skip=0, tipo=""):

        self.__login()
        select = "ItemCode,ItemName,TreeType,SalesItem,InventoryItem,AvgStdPrice,U_LED_MARCA,UpdateDate,UpdateTime,ItemPrices,ItemWarehouseInfoCollection"
        if tipo == "nacional":
            filter = "SalesItem eq 'tYES' and U_Origin eq 'N' and TreeType eq 'tNo'"
        elif tipo == "importado":
            filter = "SalesItem eq 'tYES' and U_Origin nq 'N' and TreeType eq 'tNo'"
        else:
            filter = "SalesItem eq 'tYES' and TreeType nq 'tNo'"
        
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
            filter = "SalesItem eq 'tYES' and U_Origin eq 'N' and TreeType eq 'tNo'"
        elif tipo == "importado":
            filter = "SalesItem eq 'tYES' and U_Origin nq 'N' and TreeType eq 'tNo'"
        else:
            filter = "SalesItem eq 'tYES' and TreeType nq 'tNo'"        
        
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
