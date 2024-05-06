from django.shortcuts import render, redirect, HttpResponse # importa el metodo render 
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from gestionPedidos.models import *
from django.views import View
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import JsonResponse
from .api_client import APIClient
from .forms import *
from django.core import serializers
from django.contrib import messages

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

    if User.objects.filter(username=username).exists():
            mensaje3 = "El nombre de usuario ya está en uso"
            return render(request, "micuenta.html", {'email': email, "nombre": nombre, "telefono": telefono, "mensaje_error_username": mensaje3})

    if not mensaje:

        """ n = nombre.split(" ")
        if len(n) == 1:
            firstname = n[0]
            lastname = ''
        else:
            firstname = n[0]
            lastname = n[1] """
        
        if password != rep_password:
            mensaje2 = "Las contraseñas no coinciden"
            return render(request, "micuenta.html", {'email': email, "nombre": nombre, "telefono": telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})

        usuario_login = User.objects.create(username=username, password=make, email=email, first_name= nombre)
        cuenta = Usuario.objects.create(nombre=nombre, email=email, telefono=telefono, usuarios = usuario_login)
        return redirect('/')
        
    elif password != rep_password:
        mensaje2 = "Las contraseñas no coinciden"
        return render(request, "micuenta.html", {'email': email, "nombre": nombre, "telefono": telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})
    
    return render(request,"micuenta.html",{'email': email, "nombre": nombre, "telefono":telefono,"mensaje_error_contrasena": mensaje})

#agregaado vista para modificar los datos
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
            """ n = nombre.split(" ")
            if len(n) == 1:
                user.first_name = n[0]
                user.last_name = ''
            else:
                user.first_name = n[0]
                user.last_name = n[1] """

            if password:
                user.set_password(password)
            
            if password != rep_password:
                mensaje2 = "Las contraseñas no coinciden"
                return render(request, "mis_datos.html", {'email': user.email, "nombre": nombre, "telefono": usuario.telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})
            
            usuario = Usuario.objects.get(usuarios=user)
            usuario.telefono = telefono
            usuario.nombre = nombre
            usuario.save()
            user.save()
            return redirect("/")
        
        else:
            nombre = user.first_name
            if password != rep_password:
                mensaje2 = "Las contraseñas no coinciden"
                return render(request, "mis_datos.html", {'email': user.email, "nombre": nombre, "telefono": usuario.telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})
            
            return render(request, "mis_datos.html", {'email': user.email, "nombre": nombre, "telefono": usuario.telefono, "mensaje_error_contrasena": mensaje})
        
    nombre = user.first_name

    return render(request,"mis_datos.html",{'email': user.email, "nombre": nombre, "telefono":usuario.telefono})

@login_required
def lista_usuarios(request):
    return render(request, "lista_usuarios.html")


@login_required
def creacion_clientes(request):
    return render(request, "cliente.html")

@login_required
def agregar_editar_clientes(request):
    if request.method == "POST":
        
        gruposn = request.POST.get('grupoSN')
        rut = request.POST['rut']
        giro = request.POST['giro']
        telefono = request.POST['telefono']
        email = request.POST['email']
        codigosn = rut[:-2].replace(".","")+'c' #codigoSN rut sin puntos ni digito, concatenada una C
        
        #Aca se asigan isntancias de los modelos con sus llaves foraneas correpsondientes 
        gruposn1 = GrupoSN.objects.get(codigo=gruposn)
        tipocliente = TipoCliente.objects.get(codigo = 'N')
        if gruposn == '100':
            tiposn = TipoSN.objects.get(codigo='C')
        else:
            tiposn = TipoSN.objects.get(codigo='I')
    
        if gruposn == '100':
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            cliente = SocioNegocio.objects.create(codigoSN = codigosn,
                                                nombre=nombre,
                                                apellido =apellido,
                                                rut=rut, 
                                                giro=giro, 
                                                telefono=telefono, 
                                                email=email,
                                                grupoSN = gruposn1,
                                                tipoSN = tiposn,
                                                tipoCliente = tipocliente 
                                                )
            

        elif gruposn == '105':
            razonsocial = request.POST['nombre']
            cliente = SocioNegocio.objects.create(codigoSN = codigosn,
                                                razonSocial = razonsocial,
                                                rut=rut, 
                                                giro=giro, 
                                                telefono=telefono, 
                                                email=email,
                                                grupoSN = gruposn1,
                                                tipoSN = tiposn,
                                                tipoCliente = tipocliente 
                                                )
           
        return redirect("/")

@login_required
#desde ambos botones se puede llamar y usar el tipo para ver donde se muestra en "barras (ayax)"
def agregar_direccion(request):
    if request.method == "POST":
        #numrow se define solo cmo 0
        nombredireccion = request.POST['id']
        ciudad = request.POST['cuidad']
        callenumero = request.POST['direccion']
        #codio impuesto esta defecto iva
        tipo = request.POST['tipodespacho'] #Ver si cada boton puede implicar una u otra cosa (o ambas)
        pais = request.POST['pais'] #igual por defecto esta chile
        region = request.POST['region']
        comuna = request.POST['comuna']
    
        #Inicialiando las intancias correspondientes de las llaves foraneas
        socio = SocioNegocio.objects.get(codigoSN = '1c') #Hay que crear un socio que su rut sea 1xx
        fcomuna = Comuna.objects.get(nombre = comuna)
        fregion = Region.objects.get(nombre = region)

        dir = Direccion.objects.create(nombreDireccion=nombredireccion,
                                       ciudad = ciudad,
                                       calleNumero = callenumero,
                                       comuna = fcomuna,
                                       region = fregion,
                                       tipoDireccion = tipo,
                                       SocioNegocio = socio,
                                       pais = pais) #Se crea, el resto se pasan por defecto
    return redirect("/")

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

@login_required
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

""" @login_required
def busquedaProductos(request):
    if request.method == 'GET' and 'numero' in request.GET:
        numero = request.GET.get('numero')
        # Realiza la consulta a la base de datos para obtener los resultados
        resultados = Producto.objects.filter(codigo__icontains=numero)
        # Convierte los resultados en una lista de diccionarios
        resultados_formateados = [{'codigo': producto.codigo, 'nombre': producto.nombre} for producto in resultados]
        return JsonResponse({'resultados': resultados_formateados})
    else:
        return JsonResponse({'error': 'No se proporcionó un número válido'}) """

@login_required
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
                                   'precioAnterior': producto.precioLista,
                                   'maxDescuento': producto.dsctoMaxTienda} for producto in resultados]
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

""" 
@login_required
def busquedaClientes(request):
    if request.method == 'GET' and 'numero' in request.GET:
        numero = request.GET.get('numero')
        resultadosClientes = SocioNegocio.objects.filter(rut__icontains=numero)
        resultadosClientes_formateados = [{'nombre': socionegocio.nombre,
                                   'apellido': socionegocio.apellido,
                                   'razonSocial': socionegocio.razonSocial,
                                   'rut': socionegocio.rut,
                                   'email': socionegocio.email,
                                   'telefono': socionegocio.telefono,
                                   'giro': socionegocio.giro,
                                   'condicionPago': socionegocio.condicionPago,
                                   'plazoReclamaciones': socionegocio.plazoReclamaciones,
                                   'clienteExportacion': socionegocio.clienteExportacion,
                                   'vendedor': socionegocio.vendedor,} for socionegocio in resultadosClientes]
        return JsonResponse({'resultadosClientes': resultadosClientes_formateados})
    else:
        return JsonResponse({'error': 'No se proporcionó un número válido'}) 
"""

class BusquedaClientes(LoginRequiredMixin, APIView):
    def get(self, request):
        if 'numero' in request.GET:
            numero = request.GET.get('numero')
            resultados_clientes = SocioNegocio.objects.filter(rut__icontains=numero)
            resultados_formateados = [{'nombre': socio.nombre,
                                       'apellido': socio.apellido,
                                       'razonSocial': socio.razonSocial,
                                       'rut': socio.rut,
                                       'email': socio.email,
                                       'telefono': socio.telefono,
                                       'giro': socio.giro,
                                       'condicionPago': socio.condicionPago,
                                       'plazoReclamaciones': socio.plazoReclamaciones,
                                       'clienteExportacion': socio.clienteExportacion,
                                       'vendedor': socio.vendedor} for socio in resultados_clientes]
            return Response({'resultadosClientes': resultados_formateados})
        else:
            return Response({'error': 'No se proporcionó un número válido'})

# views.py


def my_view(request):
    # Crear una instancia del cliente de la API
    client = APIClient()

    # Realizar solicitudes a la API
    data = client.get_data('endpoint_deseado')

    # Devolver los datos como una respuesta JSON
    return JsonResponse(data)

def test_connection(request):
    # Crear una instancia del cliente de la API
    client = APIClient()

    try:
        # Realizar una solicitud de prueba a la API
        test_data = client.get_data('Quotations')

        # Devolver los datos obtenidos como respuesta JSON
        return JsonResponse({'success': True, 'message': 'Conexión exitosa', 'data': test_data})
    except Exception as e:
        # Manejar cualquier error que ocurra durante la solicitud
        return JsonResponse({'success': False, 'message': 'Error al conectar con la API', 'error': str(e)})