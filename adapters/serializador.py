import json

from datosLsApp.repositories.comunarepository import ComunaRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.regionrepository import RegionRepository
from datosLsApp.repositories.socionegociorepository import SocioNegocioRepository

class Serializador:
    def __init__(self, formato):
        self.formato = formato

    def serializar(self, datos, cardCode):
        """
        Serializa los datos al formato especificado, incluyendo el cardCode.
        """
        if self.formato == 'json':
            return self.serializarAJson(datos, cardCode)
        elif self.formato == 'xml':
            return self.serializarAXml(datos)
        else:
            raise ValueError('Formato no soportado')

    def serializarAJson(self, datos, cardCode):
        # Transforma los datos del QueryDict al formato esperado por la API
        datos_transformados = self.mapearDatosApi(datos, cardCode)
        return json.dumps(datos_transformados)

    def serializarAXml(self, datos):
        return 'No implementado'

    def mapearDatosApi(self, datos, cardCode):
        """
        Mapea los datos recibidos al formato esperado por la API externa.
        """

        # Extraer datos y formatear campos necesarios
        nombre_completo = f"{datos['nombreSN']} {datos['apellidoSN']}"

        return {
            'CardCode': cardCode,
            'CardName': nombre_completo,
            'Notes': datos['giroSN'],
            'FederalTaxID': datos['rutSN'],
            'Phone2': datos['telefonoSN'],
            "Phone1": datos['telefonoSN'],
            "Cellular": datos['telefonoSN'],
            'GroupCode': datos['tipoSN'],
            'EmailAddress': datos['emailSN'],
        }
    
    def mapearDirecciones(self, datos, cardCode, rut):
        dirRepo = DireccionRepository()

        print("DATOS CREACION DE DIRECCIONES:", datos)

        if not isinstance(datos, list):
            raise ValueError("Se esperaba una lista de direcciones en 'datos'.")

        tipo_direcciones = list({direccion.get('tipoDireccion') for direccion in datos if 'tipoDireccion' in direccion})

        tipo_direcciones_complementarios = ["13" if t == "12" else "12" for t in tipo_direcciones]
        print("TIPOS DE DIRECCIONES COMPLEMENTARIOS:", tipo_direcciones_complementarios)

        datos2 = dirRepo.obtenerDireccionPorSocioYTipo(cardCode, tipo_direcciones_complementarios)
        print("DATOS DESDE LA BASE DE DATOS:", datos2)

        direcciones_mapeadas = []

        for direccion in datos:
            tipo_direccion = direccion.get('tipoDireccion')
            if not tipo_direccion:
                continue

            id_comuna = direccion.get('comuna')
            comunas = ComunaRepository().obtenerComunaPorId(id_comuna)
            
            print("COMUNA:", comunas)

            direcciones_mapeadas.append({
                'RowNum': direccion.get('rowNum', ''),
                'AddressName': direccion.get('nombreDireccion'),
                'Street': direccion.get('direccion'),
                'City': direccion.get('ciudad'),
                'County': f"{comunas.codigo} - {comunas.nombre}",
                'Country': 'CL',
                'State': int(direccion.get('region')),
                'FederalTaxID': cardCode,
                'TaxCode': 'IVA',
                'AddressType': "bo_ShipTo" if tipo_direccion == "12" else "bo_BillTo"
            })

            tipo_complementario = "13" if tipo_direccion == "12" else "12"
            complementarias = [d for d in datos2 if str(d['tipoDireccion']) == tipo_complementario]

            for complementaria in complementarias:
                if not any(d['RowNum'] == complementaria.get('rowNum', '') for d in direcciones_mapeadas):
                    
                    id_comuna = complementaria.get('comuna')        
                    # Buscar la comuna por id 
                    comunas = ComunaRepository().obtenerComunaPorId(id_comuna)
                    
                    print("COMUNA XX1:", comunas)

                    
                    direcciones_mapeadas.append({
                        'RowNum': complementaria.get('rowNum', ''),
                        'AddressName': complementaria.get('nombreDireccion'),
                        'Street': complementaria.get('direccion'),
                        'City': complementaria.get('ciudad'),
                        'County': f"{comunas.codigo} - {comunas.nombre}",
                        'Country': "CL",
                        'State': complementaria.get('region'),
                        'FederalTaxID': cardCode,
                        'TaxCode': 'IVA',
                        'AddressType': "bo_BillTo" if tipo_complementario == "13" else "bo_ShipTo"
                    })

        for direccion_db in datos2:
            # Si la dirección no está en la lista de direcciones mapeadas, agregarla
            if not any(d['RowNum'] == direccion_db.get('rowNum', '') for d in direcciones_mapeadas):
                
                id_comuna = direccion.get('comuna')        
                # Buscar la comuna por id 
                comunas = ComunaRepository().obtenerComunaPorId(id_comuna)
                
                print("COMUNA XX2:", comunas)
                
                direcciones_mapeadas.append({
                    'RowNum': direccion_db.get('rowNum', ''),
                    'AddressName': direccion_db.get('nombreDireccion'),
                    'Street': direccion_db.get('direccion'),
                    'City': direccion_db.get('ciudad'),
                    'County': f"{comunas.codigo} - {comunas.nombre}",
                    'Country': "CL",
                    'State': direccion_db.get('region'),
                    'FederalTaxID': cardCode,
                    'TaxCode': 'IVA',
                    'AddressType': "bo_BillTo" if direccion_db['tipoDireccion'] == "13" else "bo_ShipTo"
                })

        return {
            'BPAddresses': direcciones_mapeadas
        }



    
    def mapearContactos(self, datos, cardCode):

        
        # Construir la lista de empleados de contacto
        contactos_mapeados = []
        for contacto in datos:
            contactos_mapeados.append({
                'InternalCode': contacto.get('codigoInternoSap'),
                'Name': f"{contacto.get('nombre')} {contacto.get('apellido')}",
                'Phone1': contacto.get('telefono'),
                'MobilePhone': contacto.get('celular'),
                'E_Mail': contacto.get('email'),
                'CardCode': cardCode,
                'FirstName': contacto.get('nombre'),
                'LastName': contacto.get('apellido'),
            })

        print("Contactos mapeados: ", contactos_mapeados)
        
        return {
            'ContactEmployees': contactos_mapeados
        }


    def formatearDatos(self, json_data):
        # Lista para almacenar todos los productos procesados
        productos = []

        # Recorrer todos los productos en "value"
        for product_data in json_data.get("value", []):
            # Verificar si 'ItemName' es nulo, si es así, omitir el producto
            if not product_data.get("ItemName"):
                continue

            # Formatear información de un producto
            producto = {
                "Producto": {
                    "nombre": product_data.get("ItemName"),
                    "codigo": product_data.get("ItemCode"),
                    "marca": product_data.get("U_LED_MARCA"),
                    "costo": product_data.get("AvgStdPrice"),
                    "TreeType": product_data.get("TreeType"),
                }
            }

            # Inicializar precios para PriceList 1 y 2
            price_1 = None
            price_2 = None

            # Filtrar y formatear la información de precios (PriceList = 1 o 2)
            item_prices = []
            for item_price in product_data.get("ItemPrices", []):
                price_list = item_price.get("PriceList")
                price = item_price.get("Price")
                if price_list == 2:
                    price_1 = price
                elif price_list == 3:
                    price_2 = price

                if price_list in [2, 3]:  # Filtrar por PriceList
                    item_prices.append({
                        "priceList": price_list,
                        "precio": price,
                        "moneda": item_price.get("Currency"),
                    })

            # Establecer valores para los precios según la lógica
            if price_1 is None and price_2 is not None:
                price_1 = price_2
            elif price_2 is None and price_1 is not None:
                price_2 = price_1
            elif price_1 is None and price_2 is None:
                price_1 = price_2 = 0

            # Actualizar precios en la lista
            for item_price in item_prices:
                if item_price["priceList"] == 2:
                    item_price["precio"] = price_1
                elif item_price["priceList"] == 3:
                    item_price["precio"] = price_2

            # Filtrar y formatear la información de bodegas (WarehouseCode = "PH", "LC", "ME")
            bodegas = []
            for warehouse_info in product_data.get("ItemWarehouseInfoCollection", []):
                warehouse_code = warehouse_info.get("WarehouseCode")
                if warehouse_code in ["PH", "LC", "ME"]:  # Filtrar por WarehouseCode
                    bodegas.append({
                        "nombre": warehouse_code,
                        "stock_disponible": warehouse_info.get("InStock"),
                        "stock_comprometido": warehouse_info.get("Committed"),
                    })

            # Agregar el producto procesado a la lista
            productos.append({
                "Producto": producto,
                "Precios": item_prices,
                "Bodegas": bodegas,
            })

        return productos
    
    def formatearDatosReceta(self, json_data):
        # Lista para almacenar todos los productos procesados
        productos = []

        # Recorrer todos los productos en "value"
        for product_data in json_data.get("value", []):
            # Verificar si 'ItemName' es nulo, si es así, omitir el producto
            if not product_data.get("ItemName"):
                continue

            # Formatear información de un producto
            producto = {
                "Producto": {
                    "nombre": product_data.get("ItemName"),
                    "codigo": product_data.get("ItemCode"),
                    "imagen": "imagen.jpg",  # Este dato debería ser dinámico si existe en el JSON
                }
            }

            # Filtrar y formatear la información de precios (PriceList = 1 o 2)
            item_prices = []
            for item_price in product_data.get("ItemPrices", []):
                price_list = item_price.get("PriceList")
                if price_list in [1, 2]:  # Filtrar por PriceList
                    item_prices.append({
                        "priceList": price_list,
                        "precio": item_price.get("Price"),
                        "moneda": item_price.get("Currency"),
                    })

            # Filtrar y formatear la información de bodegas (WarehouseCode = "PH", "LC", "ME")
            bodegas = []
            for warehouse_info in product_data.get("ItemWarehouseInfoCollection", []):
                warehouse_code = warehouse_info.get("WarehouseCode")
                if warehouse_code in ["PH", "LC", "ME", "TR_LC", "TR_ME", "TR_PH"]:  # Filtrar por WarehouseCode
                    bodegas.append({
                        "nombre": warehouse_code,
                        "stock_disponible": warehouse_info.get("InStock"),
                        "stock_comprometido": warehouse_info.get("Committed"),
                    })

            # Agregar el producto procesado a la lista
            productos.append({
                "Producto": producto,
                "Precios": item_prices,
                "Bodegas": bodegas,
            })

        return productos
    


    def serializarSN(data):

        print(data)
        # Decodifica el JSON de entrada
        client_data = json.loads(data)
        
        # Serializa los datos principales del cliente
        serialized_data = {
            "CardCode": client_data.get("rutSN", "").replace("-", ""),
            "CardName": f"{client_data.get('nombreSN', '')} {client_data.get('apellidoSN', '')}".strip(),
            "CardType": "C",
            "GroupCode": client_data.get("tipoSN", ""),
            "Phone1": client_data.get("telefonoSN", ""),
            "Phone2": client_data.get("telefonoSN", ""),
            "Notes": client_data.get("giroSN", ""),
            "PayTermsGrpCode": -1,
            "FederalTaxID": client_data.get("rutSN", "").split("-")[0],
            "SalesPersonCode": -1,
            "Cellular": client_data.get("telefonoSN", ""),
            "EmailAddress": client_data.get("emailSN", ""),
            "CardForeignName": f"{client_data.get('nombreSN', '')} {client_data.get('apellidoSN', '')}".strip(),
            "ShipToDefault": "DESPACHO",
            "BilltoDefault": "FACTURACION",
            "DunningTerm": "ESTANDAR",
            "CompanyPrivate": "cPrivate",
            "AliasName": client_data.get("nombreSN", ""),
            "U_Tipo": "N",
            "U_FE_Export": "N",
            "BPAddresses": [],
            "ContactEmployees": []
        }
        
        # Serializa las direcciones
        for address in client_data.get("direcciones", []):
            serialized_address = {
                "AddressName": address.get("nombreDireccion", ""),
                "Street": address.get("direccion", ""),
                "City": address.get("ciudad", ""),
                "County": address.get("tipoDireccion", ""),
                "Country": address.get("pais", "")[:2].upper(),  # Abreviación del país (e.g., Chile -> CL)
                "State": address.get("region", ""),
                "FederalTaxID": client_data.get("rutSN", "").split("-")[0],
                "TaxCode": "IVA",
                "AddressType": "bo_ShipTo"
            }
            serialized_data["BPAddresses"].append(serialized_address)
        
        # Serializa los contactos
        for contact in client_data.get("contactos", []):
            serialized_contact = {
                "Name": f"{contact.get('nombreContacto', '')} {contact.get('apellidoContacto', '')}".strip(),
                "Phone1": contact.get("telefonoContacto", ""),
                "MobilePhone": contact.get("telefonoContacto", ""),
                "E_Mail": contact.get("emailContacto", ""),
                "FirstName": contact.get("nombreContacto", ""),
                "LastName": contact.get("apellidoContacto", "")
            }
            serialized_data["ContactEmployees"].append(serialized_contact)
        
        return serialized_data
        




