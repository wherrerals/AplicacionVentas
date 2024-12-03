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

    def serializeProducts(self, data):

        
        return [
            {
                "sku": item["SKU"],
                "name": item["Name"],
                "description": item["Description"],
                "price": item.get("Price"), 
            }
            for item in data
        ]

    def serializeStock(self, data):


        return [
            {
                "sku": item["SKU"],
                "warehouse": item["Warehouse"],
                "stock": item["Stock"],
            }
            for item in data
        ]