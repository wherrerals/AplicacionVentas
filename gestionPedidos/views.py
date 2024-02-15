from django.shortcuts import render, redirect, HttpResponse # importa el metodo render 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from gestionPedidos.models import *
from django.views import View
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.core import serializers


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
def cotizacion(request):
    if request.user.is_authenticated:
        # Acceder al nombre de usuario
        username = request.user.username
        return render(request, 'cotizacion.html', {'username': username})
    else:
        return render(request, "cotizacion.html")
    
@login_required #Implementada para menus de opciones con regiones
def regiones(request):
    regiones = Region.objects.all()
    return render(request, 'cotizacion.html', {'regiones': regiones})


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

@transaction.atomic
@login_required
def registrarCuenta(request):
    nombre = request.POST['nombre']
    email = request.POST['email']
    username = request.POST['email']
    telefono = request.POST['telefono'] 
    rep_password = request.POST.get('rep_password')
    #showroom = request.POST['showroom']
    #numero_sap = request.POST['num_sap']
    password = request.POST['password']
    make = make_password(password)
    mensaje = validar_contrasena(password)

    if not mensaje:
        n = nombre.split(" ")
        if len(n) == 1:
            firstname = n[0]
            lastname = ''
        else:
            firstname = n[0]
            lastname = n[1]
        
        if password != rep_password:
            mensaje2 = "Las contraseñas no coinciden"
            return render(request, "micuenta.html", {'email': email, "nombre": nombre, "telefono": telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})

        usuario_login = User.objects.create(username=username, password=make, email=email, first_name= firstname,last_name = lastname)
        cuenta = Usuario.objects.create(nombre=nombre, email=email, telefono=telefono, usuarios = usuario_login)
        return redirect('/')
        
    elif password != rep_password:
        mensaje2 = "Las contraseñas no coinciden"
        return render(request, "micuenta.html", {'email': email, "nombre": nombre, "telefono": telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})
    
    return render(request,"micuenta.html",{'email': email, "nombre": nombre, "telefono":telefono,"mensaje_error_contrasena": mensaje})
    

#agregaado vista para modificar los datos
@login_required
def mis_datos(request):

    usuario = Usuario.objects.get(usuarios=request.user)
    user = request.user

    if request.method == "POST":
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        password = request.POST.get('password', '')
        rep_password = request.POST.get('rep_password')
        mensaje = validar_contrasena(password)

        if not mensaje:
            n = nombre.split(" ")
            if len(n) == 1:
                user.first_name = n[0]
                user.last_name = ''
            else:
                user.first_name = n[0]
                user.last_name = n[1]

            if password:
                user.set_password(password)
            
            if password != rep_password:
                mensaje2 = "Las contraseñas no coinciden"
                return render(request, "mis_datos.html", {'email': user.email, "nombre": nombre_completo, "telefono": usuario.telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})
            
            usuario = Usuario.objects.get(usuarios=user)
            usuario.telefono = telefono
            usuario.nombre = nombre
            usuario.save()
            user.save()
            return redirect("/")
        
        else:
            nombre = user.first_name
            apellido = user.last_name
            nombre_completo = f'{nombre} {apellido}'
            if password != rep_password:
                mensaje2 = "Las contraseñas no coinciden"
                return render(request, "mis_datos.html", {'email': user.email, "nombre": nombre_completo, "telefono": usuario.telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})
            
            return render(request, "mis_datos.html", {'email': user.email, "nombre": nombre_completo, "telefono": usuario.telefono, "mensaje_error_contrasena": mensaje})
        
    nombre = user.first_name
    apellido = user.last_name
    nombre_completo = f'{nombre} {apellido}'
    return render(request,"mis_datos.html",{'email': user.email, "nombre": nombre_completo, "telefono":usuario.telefono})


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

def obtenerDatosProducto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    data = {
        'productoCodigo': producto.codigo,
        'stock': producto.stock,
        'precioActual': str(producto.precio_actual),
        'precioAnterior': str(producto.precio_anterior),
        'maxDescuento': producto.max_descuento,       
    }

    return JsonResponse(data)


"""def busquedaProductos(request):
    if request.method == 'GET' and 'numero' in request.GET:
        numero = request.GET.get('numero')
        # Realiza la consulta a la base de datos para obtener los resultados
        resultados = Producto.objects.filter(codigo__icontains=numero)
        # Convierte los resultados en una lista de diccionarios
        resultados_formateados = [{'codigo': producto.codigo, 'nombre': producto.nombre} for producto in resultados]
        return JsonResponse({'resultados': resultados_formateados})
    else:
        return JsonResponse({'error': 'No se proporcionó un número válido'})"""

def busquedaProductos(request):
    if request.method == 'GET' and 'numero' in request.GET:
        numero = request.GET.get('numero')
        # Realiza la consulta a la base de datos para obtener los resultados
        resultados = Producto.objects.filter(codigo__icontains=numero)
        # Convierte los resultados en una lista de diccionarios
        resultados_formateados = [{'codigo': producto.codigo,
                                   'nombre': producto.nombre,
                                   'imagen': producto.imagen,
                                   'precio': producto.precioVenta,
                                   'stockTotal': producto.stockTotal,
                                   'precioActual': producto.precioVenta,
                                   'precioAnterior': producto.precioLista,
                                   'maxDescuento': producto.dsctoMaxTienda} for producto in resultados]
        return JsonResponse({'resultados': resultados_formateados})
    else:
        return JsonResponse({'error': 'No se proporcionó un número válido'})

def busquedaClientes(request):
    if request.method == 'GET' and 'numero' in request.GET:
        numero = request.GET.get('numero')
        # Realiza la consulta a la base de datos para obtener los resultados
        resultados = SocioNegocio.objects.filter(rut__icontains=numero)
        # Convierte los resultados en una lista de diccionarios
        resultados_formateados = [{'nombre': producto.codigo, 'nombre': producto.nombre} for producto in resultados]
        return JsonResponse({'resultados': resultados_formateados})
    else:
        return JsonResponse({'error': 'No se proporcionó un número válido'})

def validar_contrasena(password):
    mensajes = []

    if not any(caracter in password for caracter in "!@#$%^&*_+:;<>?/~"):
        mensajes.append("Su contraseña debe incluir al menos un símbolo [!@#$%^&*_+:;<>?/~].")

    if not any(caracter.isupper() for caracter in password):
        mensajes.append("Su contraseña debe incluir al menos una mayúscula.")

    if not any(caracter.isdigit() for caracter in password):
        mensajes.append("Su contraseña debe incluir al menos un número.")

    if len(password) < 8:
        mensajes.append("Su contraseña debe tener al menos 8 caracteres.")

    return mensajes 