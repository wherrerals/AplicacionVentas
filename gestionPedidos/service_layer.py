import httpx

class Funciones:
    LocalHost = "1.1"
    Puerto = "50003"
    Datos = {"CompanyDB": "TEST_LED_PROD", "UserName": "manager", "Password": "1245LED98"}
    #url = f"https://{LocalHost}:{Puerto}/b1s/v1"
    url = 'https://httpbin.org'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.motor = None  # determina httpx o request
        self.accion = None  # determina si es GET o POST
        self.param = None  # determina si es quotation, etc
        self.data = None  # se ingresa si hay un (id).
        self.extra = None  # cancel o close
        self.dato_solicitud = None

    def validacion(self):  # protección para los datos enviados a evaluar
        motor_valido = ['httpx', 'request']
        accion_valida = ['get', 'post', 'patch']
        param_valido = ['quotation', 'Orders', 'ReturnRequest', None]  # Quitar None cuando se trabaje con service layer
        extra_valido = ['Close', 'Cancel', None]  # también quitar
        if self.accion not in accion_valida or self.motor not in motor_valido or self.param not in param_valido or self.extra not in extra_valido:
            raise ValueError("Parámetros ingresados no válidos")

    def constructor_url(self):
        self.validacion()

        self.dato_solicitud = self.dato_solicitud or {}

        if self.data is None:
            if self.param is None:
                new_endpath = f"{self.url}/"
            else:
                new_endpath = f"{self.url}/{self.param}"
        else:
            if self.extra is None:
                new_endpath = f"{self.url}/{self.param}({self.data})"
            else:
                new_endpath = f"{self.url}/{self.param}({self.data})/{self.extra}"

        return new_endpath
    
    def get(self, request, motor, accion, param):
        self.motor = motor
        self.accion = accion
        self.param = param

        resultado = self.constructor_url()
    
        #return HttpResponse('Todo ok')
    
class SAPService:

    def __init__(self,CompanyDB,UserName,Password): #se inizialisa una unica instnacia de cliente
        self.username = UserName
        self.password = Password
        self.CompanyDB = CompanyDB
        self.client = httpx.Client()
        
    def __del__(self): # se llama destructor cuando se queire cerrar la conexion
        self.client.close()

    def _get_auth(self): #Se utiliza para cada peticion, agrega seguridad
        return(self.CompanyDB,self.username, self.password)

    #En el siguiente metodo esta todo el manejo de execepciones y el manejo de los datos
    def _solicitud(self,motor,accion,param,data = None, extra = None, dato_solicitud = None,**kwargs):
        headers = {'CompanyDB': self.CompanyDB}
        c1 = Funciones(motor, accion, param, data, extra, dato_solicitud = None)
        try:
            url = c1.constructor_url()
            response = self.client.request(accion,url,auth=self._get_auth, json=dato_solicitud,headers=headers,**kwargs)
            response.raise_for_status()

        except httpx.TimeoutException as exc: #cuando el tiempo de espera excede un limite
            print(f'Finalizo el tiempo de espera {exc}')

        except httpx.HTTPStatusError as exc: #cualquier codigo de retorno 4xx y 5xx
            print(f"Se produjo un error HTTP: {exc}")
            print(f"Código de estado HTTP: {exc.response.status_code}")
            print(f"Mensaje de error: {exc.response.text}")

        except httpx.NetworkError as exc: #error de conexion a internet
            print(f"Error de red: {exc}")
            print(f"Revise su conexion a internet.")

        except Exception as exc:
            print(f"Error desconocido: {exc}")



    def solicitud(self, motor, accion, param, data=None, extra=None, dato_solicitud=None, **kwargs):
        return self._solicitud(motor, accion, param, data=data, extra=extra, dato_solicitud=dato_solicitud, **kwargs)