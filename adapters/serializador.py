import json

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
            'Notes': "Persona",
            'FederalTaxID': datos['rutSN'],
            'Cellular': datos['telefonoSN'],
            'EmailAddress': datos['emailSN'],
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
    




