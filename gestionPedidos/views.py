#Django modulos
from django.shortcuts import render, redirect, HttpResponse # importa el metodo render 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.http import JsonResponse
from django.core import serializers
#Django Rest F modulos
from rest_framework.views import APIView
from rest_framework.response import Response
#Modulos Diseñados
from gestionPedidos.models import *
from .forms import * #prueba
from .api_client import APIClient
#librerias Python usadas
import requests

#Inicio vistas Renderizadoras
@login_required
def home(request):
    if request.user.is_authenticated:
        username = request.user.username 
        return render(request, 'home.html', {'username': username}) # Accede al nombre de usuario y permite su uso en el template
    else:
        return render(request, 'home.html')

@login_required
def salir(request):
    logout(request)
    return redirect('/')

@login_required
def list_quotations(request):
    
    return render(request, "lista_cotizaciones.html")
 
@login_required
def quotations(request):
    if request.user.is_authenticated:
        username = request.user.username
    
        doc_num = request.GET.get('docNum', None)

        context = {
            'docnum': doc_num,
            'username': username
        }

        return render(request, 'cotizacion.html', context)
    else:
        return render(request, "cotizacion.html")
    
@login_required
def quotations_view(request):
    if request.user.is_authenticated:
        username = request.user.username 

    doc_num = request.GET.get('docNum', None)
    
    context = {
        'docnum': doc_num,
        'username': username
    }
    return render(request, 'cotizacion.html', context)

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
    

class BusquedaProductosView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        numero = request.GET.get('numero')
        if numero:
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


class BusquedaClientes(LoginRequiredMixin, APIView):
    def get(self, request):
        if 'numero' in request.GET:
            numero = request.GET.get('numero')
            resultados_clientes = SocioNegocio.objects.filter(rut__icontains=numero)
            resultados_formateados = []

            for socio in resultados_clientes:
                direcciones = Direccion.objects.filter(SocioNegocio=socio)
                direcciones_formateadas = [{
                    'rowNum': direccion.rowNum,
                    'nombreDireccion': direccion.nombreDireccion,
                    'ciudad': direccion.ciudad,
                    'calleNumero': direccion.calleNumero,
                    'codigoImpuesto': direccion.codigoImpuesto,
                    'tipoDireccion': direccion.tipoDireccion,
                    'pais': direccion.pais,
                    'comuna': direccion.comuna.nombre,  # Asumiendo que Comuna tiene un campo nombre
                    'region': direccion.region.nombre  # Asumiendo que Region tiene un campo nombre
                } for direccion in direcciones]

                resultados_formateados.append({
                    'nombre': socio.nombre,
                    'apellido': socio.apellido,
                    'razonSocial': socio.razonSocial,
                    'rut': socio.rut,
                    'email': socio.email,
                    'telefono': socio.telefono,
                    'giro': socio.giro,
                    'condicionPago': socio.condicionPago,
                    'plazoReclamaciones': socio.plazoReclamaciones,
                    'clienteExportacion': socio.clienteExportacion,
                    'vendedor': socio.vendedor,
                    'direcciones': direcciones_formateadas
                })
            
            return Response({'resultadosClientes': resultados_formateados})
        else:
            return Response({'error': 'No se proporcionó un número válido'})
        

def quotate_items(request, docNum):
    client = APIClient()  

    try:
        data = client.get_quotations_items('Quotations')  # Ajusta según el método de cliente API

        # Verificar si hay datos y procesarlos
        if 'value' in data:
            quotations = data['value']
            found_quotation = None

            # Buscar la cotización con el DocNum especificado
            for quotation in quotations:
                if quotation.get('DocNum') == int(docNum):  # Convertir docNum a entero si es necesario
                    found_quotation = quotation
                    break

            if found_quotation:
                # Obtener las líneas de documentos (DocumentLines)
                document_lines = found_quotation.get('DocumentLines', [])

                # Preparar los datos para enviar como respuesta JSON
                lines_data = []
                for line in document_lines:
                    line_data = {
                        'LineNum': line.get('LineNum'),
                        'ItemCode': line.get('ItemCode'),
                        'ItemDescription': line.get('ItemDescription'),
                        'ItemCode': line.get('ItemCode'),
                        'ItemCode': line.get('ItemCode'),
                        'ItemCode': line.get('ItemCode'),
                        'ItemDescription': line.get('ItemDescription'),
                        'Quantity': line.get('Quantity'),
                        'Price': line.get('Price'),
                    }
                    lines_data.append(line_data)

                # Retornar respuesta JSON con las líneas de documentos encontradas
                return JsonResponse({'DocumentLines': lines_data}, status=200)
            else:
                return JsonResponse({'error': 'No se encontró la cotización con el DocNum especificado'}, status=404)

        else:
            return JsonResponse({'error': 'No se encontraron datos de cotizaciones'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


@require_http_methods(["GET"])
def list_quotations_2(request):
    client = APIClient()

    # Obtener los valores de 'top' y 'skip' de los parámetros de la solicitud GET
    top = request.GET.get('top', 20)  # valor predeterminado de 100
    skip = request.GET.get('skip', 0)  # valor predeterminado de 0

    # Convertir a entero ya que los parámetros de solicitud son cadenas por defecto
    try:
        top = int(top)
        skip = int(skip)
    except ValueError:
        # Manejar el caso en que la conversión a entero falle
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    data = client.get_quotations(top=top, skip=skip)
    return JsonResponse(data, safe=False)


def post_quotations1(request):
    client = APIClient()
    endpoint = "Quotations"
    data = client.post_data(endpoint)
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_POST
def post_quotations(request):
    try:
        # Datos de prueba
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

        client = APIClient()
        endpoint = "Quotations"
        response_data = client.post_data(endpoint, data=data)

        # Verificar si response_data es None
        if response_data is None:
            return JsonResponse({'error': 'No response data received'}, status=500)
        
        # Verificar si hay un error en response_data
        if isinstance(response_data, dict) and 'error' in response_data:
            return JsonResponse(response_data, status=500)
        
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        print("An error occurred:", e)
        return JsonResponse({'error': str(e)}, status=500)