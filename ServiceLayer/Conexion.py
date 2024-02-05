import httpx


LocalHost = "1.1"
Puerto = "50003"
Datos =  {"CompanyDB": "TEST_LED_PROD", "UserName": "manager", "Password": "1245LED98"}
#url = f"https://{LocalHost}:{Puerto}/b1s/v1"
url = 'https://httpbin.org'

class funciones:

    def __init__ (self,motor,accion,param,data = None, extra = None, dato_solicitud = None):
        self.motor = motor #determina httpx o request
        self.accion = accion #determina si es GET o POST
        self.param = param #determina si es quotation,etc
        self.data = data #se ingresa si hay un (id).
        self.extra = extra #cancel o close
        self.dato_solicitud = dato_solicitud 
        
    def validacion (self):#proteccion para los datos enviados a eval
        motor_valido = ['httpx','request']
        accion_valida = ['get','post','patch']
        param_valido = ['quotation','Orders','ReturnRequest',None] #Quitar None cuando se trabaje con service layer
        extra_Valido = ['Close','Cancel',None] #tamb quitar
        if self.accion not in accion_valida or self.motor not in motor_valido or self.param not in param_valido or self.extra not in extra_Valido:
            raise ValueError("Parametros ingresados no validos")
    
    def constructor_url(self):
        self.validacion()

        self.dato_solicitud = self.dato_solicitud or {}

        if self.data is None:
            if self.param == None:
                newEndpath = (f"('{url}/')")
                return newEndpath
            else:
                newEndpath = (f"'{url}/{self.param}', json={self.dato_solicitud}")
                return newEndpath
        else:
            if self.extra is None:
                newEndpath = (f"{self.motor}.{self.accion}('{url}/{self.param}({self.data})', json={self.dato_solicitud})")
                return newEndpath
            else:
                newEndpath = (f"{self.motor}.{self.accion}('{url}/{self.param}({self.data})/{self.extra}')")
                return newEndpath
            

sol = {'key1': 'value1', 'key2': 'value2'}
data = {
    "CardCode": "c001",
    "DocumentLines": [
        {
            "ItemCode": "i001",
            "Quantity": "100",
            "TaxCode": "T1",
            "UnitPrice": "30"
        }
    ]
}
mensaje = {
    "Comments": "new comments - modified by Service Layer"
}




c1 = funciones('httpx','get','quotation')
c2= funciones('httpx','get','quotation',123)
c3= funciones('httpx','post','quotation',175,None,data)
c4 = funciones('httpx','patch','quotation',123,None,mensaje)
c5  = funciones('httpx','post','quotation',123,'Close',mensaje)
c6  = funciones('httpx','post','quotation',123,'Cancel')


resultado = c1.constructor_url()
print(f'\nGET QUOTATIONS \n {resultado}\n')
resultado = c2.constructor_url()
print(f'GET QUOTATIONS(ID) \n {resultado}\n')
resultado = c3.constructor_url()
print(f'POSt quotations \n {resultado}\n')
resultado = c4.constructor_url()
print(f'patch quotations (id) \n {resultado}\n')
resultado = c5.constructor_url()
print(f'post quotatiions(id)/close \n {resultado}\n')
resultado = c6.constructor_url()
print(f'poset quotations(id)/cancel \n {resultado}\n')


