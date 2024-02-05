from django.shortcuts import render, redirect, HttpResponse # importa el metodo render 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from gestionPedidos.models import *
from django.http import JsonResponse
from django.views import View
import httpx

@login_required
def home(request):
    if request.user.is_authenticated:
        # Acceder al nombre de usuario
        username = request.user.username
        return render(request, 'home.html', {'username': username})
    else:
        # El usuario no está autenticado, puedes manejarlo de alguna manera
        return render(request, 'home.html')

    #return render(request, "home.html")

@login_required
def salir(request):
    logout(request)
    return redirect('/')

@login_required
def lista_cotizaciones(request):
    return render(request, "lista_cotizaciones.html")

@login_required
def lista_ovs(request):
    return render(request, "lista_ovs.html")

@login_required
def lista_solic_devoluciones(request):
    return render(request, "lista_solic_devoluciones.html")

@login_required
def lista_clientes(request):
    return render(request, "lista_clientes.html")

@login_required
def reporte_stock(request):
    return render(request, "reporte_stock.html")

@login_required
def micuenta(request):

    return render(request, "micuenta.html")

@login_required
def registrarCuenta(request):
    nombre = request.POST['nombre']
    email = request.POST['email']
    username = request.POST['email']
    telefono = request.POST['telefono']
    #showroom = request.POST['showroom']
    #numero_sap = request.POST['num_sap']
    password = request.POST['password']

    cuenta = Usuario.objects.create(nombre=nombre, email=email, telefono=telefono)
    usuario_login = User.objects.create(username=username, password=password)

    return redirect('/')

@login_required
def lista_usuarios(request):
    return render(request, "lista_usuarios.html")


@login_required
def clientes(request):
    return render(request, "cliente.html")

class Funciones(View):
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
    
        return HttpResponse('Todo ok')