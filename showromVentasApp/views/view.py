from io import BytesIO
from turtle import width
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, TA_CENTER

from django.shortcuts import get_object_or_404, render, redirect  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.http import JsonResponse, HttpResponse
#Modulos Diseñados
from datosLsApp.models.usuariodb import User 
from datosLsApp.models import (ProductoDB, SocioNegocioDB, UsuarioDB, RegionDB, GrupoSNDB, TipoSNDB, TipoClienteDB, DireccionDB, ComunaDB, ContactoDB)
from adapters.sl_client import APIClient
from datosLsApp.repositories.comunarepository import ComunaRepository
from datosLsApp.repositories.regionrepository import RegionRepository
from datosLsApp.repositories.stockbodegasrepository import StockBodegasRepository
from logicaVentasApp.services.contacto import Contacto
from logicaVentasApp.services.cotizacion import Cotizacion
from logicaVentasApp.services.direccion import Direccion
from logicaVentasApp.services.producto import Producto
from logicaVentasApp.services.socionegocio import SocioNegocio
#librerias Python usadas
import requests
import json

from logicaVentasApp.services.comuna import Comuna
from datosLsApp.models.stockbodegasdb import StockBodegasDB
from taskApp.tasks import sync_products
from celery.exceptions import TimeoutError

#Inicio vistas Renderizadoras

"""
Decoradores usados: 
    @login_required: Decorador que indica que solo se ejecuta el template si el usurio esta logeado
    @transaction.atomic: Decorador usado para vistas que realizan  un conjunto de operaciones sobre la db, permitiendo que todas se ejecuten con exito o ninguna se aplique si ocurre un error. 
"""

@login_required
def home(request):
    """
    Rendereriza la pagina principal y muestra el nombre del usuario y sus grupos que ha iniciado sesión

    Args: 
        request (HttpRequest): La petición HTTP recibida.

    Returns:
        HttpResponse: Si el usuario está autenticado, renderiza el template 'home.html' con el nombre de usuario y los grupos.
        HttpResponse: Si el usuario no está autenticado, redirige al template del login.
    """
    if request.user.is_authenticated:
        username = request.user.username

        try:
            usuario = UsuarioDB.objects.get(usuarios=request.user)
            nombreUser = usuario.nombre


        except UsuarioDB.DoesNotExist:
            return JsonResponse({'error': 'No se encontró el usuario relacionado con el usuario autenticado'}, status=404)
        

        
        context = {
            'username': username,
            'nombreuser': nombreUser,
        }

        return render(request, 'home.html', context)

@login_required  
def odv(request):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtiene el nombre de usuario del modelo User de Django
        username = request.user.username

        # Intenta obtener el objeto UsuarioDB relacionado con el usuario autenticado
        try:
            usuario = UsuarioDB.objects.get(usuarios=request.user)
            sucurs = usuario.sucursal  # Accede a la sucursal a través del modelo UsuarioDB
            nombreUser = usuario.nombre  # Accede al nombre del usuario a través del modelo UsuarioDB
            codVen = usuario.vendedor.codigo  # Accede al código del vendedor a través del modelo UsuarioDB

        except UsuarioDB.DoesNotExist:
            # Maneja el caso en que no se encuentre el usuario relacionado
            JsonResponse({'error': 'No se encontró el usuario relacionado con el usuario autenticado'}, status=404)

        # Obtiene el parámetro DocNum de la URL, o None si no está presente
        doc_num = request.GET.get('docNum', None)

        # Obtiene todas las regiones de la base de datos
        regiones = RegionDB.objects.all()

        # Contexto para renderizar el template
        context = {
            'docnum': doc_num,
            'username': username,
            'regiones': regiones,
            'sucursal': sucurs,
            'nombreuser': nombreUser,
            'codigoVendedor': codVen
        }
    
    return render(request, "ordenventa.html", context)


@login_required
def userLogout(request):
    """
    Finaliza la sesion del usuario.

    Args: 
        request (HttpsRequest): La peticion HTTP recibida

    Returns: 
        HttpResponse: redirige a la pagina de inicio despues de cerrar la sesion del usuario.
    """

    logout(request)
    return redirect('/')

@login_required
def list_quotations(request):
    """
    Renderiza la pagina de lista de cotizaciones 
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'lista_cotizaciones.html' 
    """
    
    return render(request, "lista_cotizaciones.html")

def enlazarComunas(request):
    """
    Obtiene las comunas de una región y las devuelve en formato JSON.

    Args:
        request (HttpRequest): La petición HTTP recibida.

    Returns:
        JsonResponse: Si no se proporciona un ID de región, devuelve un error 400.
        JsonResponse: Las comunas de la región solicitada en formato JSON.
    """

    print("Enlazando comunas")
    if request.method == 'GET':
        id_Region = request.GET.get('idRegion')
        
        if not id_Region:
            return JsonResponse({'error': 'No se proporcionó un ID de región'}, status=400)
        
        comuna_service = Comuna()

    return comuna_service.obtenerComunas(id_Region)

@login_required
def quotations(request):
    """
    Renderiza la pagina de cotizaciones y muestra el nombre de usuario.

    Captura de la url el parametro DocNum y, si este no esta presente, lo establece en null.
    También obtiene todas las instancias del modelo 'Region' para ser utilizadas en el template.

    Args:
        request (HttpRequest): La petición HTTP recibida.
    
    Returns:
        HttpResponse: Renderiza el template 'cotizacion.html' con el nombre de usuario y el DocNum.
        HttpResponse: Si el usuario no está autenticado, redirige al template del inicio.
    """

    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Obtiene el nombre de usuario del modelo User de Django
        username = request.user.username

        # Intenta obtener el objeto UsuarioDB relacionado con el usuario autenticado
        try:
            usuario = UsuarioDB.objects.get(usuarios=request.user)
            sucurs = usuario.sucursal  # Accede a la sucursal a través del modelo UsuarioDB
            nombreUser = usuario.nombre  # Accede al nombre del usuario a través del modelo UsuarioDB
            codVen = usuario.vendedor.codigo  # Accede al código del vendedor a través del modelo UsuarioDB

        except UsuarioDB.DoesNotExist:
            # Maneja el caso en que no se encuentre el usuario relacionado
            JsonResponse({'error': 'No se encontró el usuario relacionado con el usuario autenticado'}, status=404)

        # Obtiene el parámetro DocNum de la URL, o None si no está presente
        doc_num = request.GET.get('docNum', None)

        # Obtiene todas las regiones de la base de datos
        regiones = RegionDB.objects.all()

        # Contexto para renderizar el template
        context = {
            'docnum': doc_num,
            'username': username,
            'regiones': regiones,
            'sucursal': sucurs,
            'nombreuser': nombreUser,
            'codigoVendedor': codVen
        }

        # Renderiza el template con el contexto
        return render(request, 'cotizacion.html', context)

@login_required
def lista_ovs(request):
    """
    Renderiza la página de ordenes de venta
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'lista_ovs.html'
    """
    
    return render(request, "lista_ovs.html")

@login_required
def lista_solic_devoluciones(request):
    """
    Renderiza la página de devoluciones 
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'lista_solic_devoluciones.html'
    """

    return render(request, "lista_solic_devoluciones.html")

@login_required
def lista_clientes(request):
    """
    Renderiza la página de Listado de clientes
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'lista_clientes.html'
    """

    return render(request, "lista_clientes.html")

@login_required
def reporte_stock(request):
    """
    Renderiza la página de reportes de stock
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'reporte_stock.html'
    """

    return render(request, "reporte_stock.html")

@login_required
def micuenta(request):
    """
    Renderiza la página de cuenta de usuario
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'micuenta.html'
    """

    return render(request, "micuenta.html")

@login_required
def lista_usuarios(request):
    """
    Renderiza la página de lista de usuario
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'lista_usuarios.html'
    """

    return render(request, "lista_usuarios.html")

@login_required
def creacion_clientes(request):
    """
    Renderiza la página de lista de usuario
    
    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns:
        HttpResponse: renderiza el template 'cliente.html'
    """

    return render(request, "cliente.html")

@transaction.atomic 
@login_required
def registrarCuenta(request):

    """
        Registra nuevos usuarios en la db

        Args: 
            request (HttpsRequest): La peticion HTTP recibida

        Returns: 
            HttpResponse: Si el nombre de usuario ya existe renderiza en el template 'micuenta.html' un mensaje indicando que ya existe
            HttpResponse: Si las contraseñas no coindicen renderiza en el template 'micuenta.html' un mensaje indicando que las contraseñas no coinciden
            HttpResponse: Si la contraseña no cumple con los requisitos renderiza en el template 'micuenta.html' un mensaje indicando que la contraseña no cumple con los requisitos            
            
    """
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
        cuenta = UsuarioDB.objects.create(nombre=nombre, email=email, telefono=telefono, usuarios = usuario_login)
        return redirect('/')
        
    elif password != rep_password:
        mensaje2 = "Las contraseñas no coinciden"
        return render(request, "micuenta.html", {'email': email, "nombre": nombre, "telefono": telefono, "mensaje_error_contrasena": mensaje, "mensaje_error_repcontrasena": mensaje2})
    
    return render(request,"micuenta.html",{'email': email, "nombre": nombre, "telefono":telefono,"mensaje_error_contrasena": mensaje})

#agregaado vista para modificar los datos

@login_required
def mis_datos(request):

    usuario = UsuarioDB.objects.get(usuarios=request.user)
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
            
            usuario = UsuarioDB.objects.get(usuarios=user)
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


def actualizarAgregarDirecion(request, socio):
    if request.method == "POST":
        try:

            data = request.POST
            rut = data.get('cliente')
            carCode = SocioNegocio.generarCodigoSN(rut)

            SocioNegocio.actualizaroCrearDireccionSL(carCode, request.POST)

            conexionAPi = APIClient()
            dataMSQL = conexionAPi.obtenerDataSn(carCode, "BPAddresses")

            print(f"Data obtenida de la API: {dataMSQL}")

            
            result = Direccion().procesarDireccionDesdeAPI(dataMSQL, socio)

            #result = SocioNegocio.procesarDirecciones(request.POST, socio)
            return JsonResponse(result['data'], status=result['status'])

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

def actualizarAgregarContacto(request, socio):
    if request.method == "POST":
        try:
            data = request.POST
            rut = data.get('cliente')
            carCode = SocioNegocio.generarCodigoSN(rut)

            SocioNegocio.actualizaroCrearContactosSL(carCode, request.POST)
            print("Estos son los datos:", request.POST)

            conexionAPi = APIClient()

            dataMSQL = conexionAPi.obtenerDataSn(carCode, "ContactEmployees")

            print("Data obtenida de la API:", dataMSQL)

            result = Contacto().procesarContactosDesdeAPI(dataMSQL, socio)
            
            # Delegamos la lógica de procesamiento al servicio
            #result = SocioNegocio.procesarContactos(contactoSerializado, socio)
            

            return JsonResponse(result['data'], status=result['status'])

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

@login_required
def agregarDireccion(request, socio):
    print("estamos aqui")
    if request.method == "POST":
        nombredirecciones = request.POST.getlist('nombre_direccion[]')
        ciudades = request.POST.getlist('ciudad[]')
        callesnumeros = request.POST.getlist('direccion[]')
        tipos = request.POST.getlist('tipodireccion[]')
        paises = request.POST.getlist('pais[]')
        regiones = request.POST.getlist('region[]')
        comunas = request.POST.getlist('comuna[]')

        print(f"nombre direccion: ", nombredirecciones)
        print(f"nombres de ciudades: ", ciudades)
        print(f"tipo de direcciones: ", tipos)

        for i in range(len(nombredirecciones)):
            nombredireccion = nombredirecciones[i]
            ciudad = ciudades[i]
            callenumero = callesnumeros[i]
            tipo = tipos[i]
            pais = paises[i]
            region = regiones[i]
            comuna = comunas[i]

            if nombredireccion:  # Verificar si el nombre de la dirección está presente
                fregion = RegionDB.objects.get(numero=region)
                fcomuna = ComunaDB.objects.get(codigo=comuna)

                # Crear la dirección principal
                DireccionDB.objects.create(
                    nombreDireccion=nombredireccion,
                    ciudad=ciudad,
                    calleNumero=callenumero,
                    comuna=fcomuna,
                    region=fregion,
                    tipoDireccion=tipo,
                    SocioNegocio=socio,
                    pais=pais
                )
                print(f"Dirección {i+1} creada con éxito")

                # Verificar y duplicar si es necesario
                tipo_faltante = '12' if tipo == '13' else '13'
                DireccionDB.objects.create(
                    nombreDireccion=nombredireccion,
                    ciudad=ciudad,
                    calleNumero=callenumero,
                    comuna=fcomuna,
                    region=fregion,
                    tipoDireccion=tipo_faltante,
                    SocioNegocio=socio,
                    pais=pais
                )
                print(f"Dirección duplicada con tipo {tipo_faltante} creada con éxito")
            else:
                print(f"No se ha creado la dirección {i+1} porque algunos campos están vacíos.")
        
        return redirect("/")





@login_required
def agregarContacto(request, cliente, **kwargs):
    print(f"RUT del cliente: {cliente}")
    print("Data recibida: ", request.POST)

    clienteNoIncluido = None
    if cliente is None:
        clienteNoIncluido = "No se ha incluido el cliente en la solicitud."

    if request.method == "POST":
        # Determinar si estamos trabajando con un contacto único o múltiples
        if 'nombre' in kwargs:
            # Caso: contacto único enviado desde kwargs
            nombres = [kwargs.get('nombre')]
            apellidos = [kwargs.get('apellido')]
            telefonos = [kwargs.get('telefono')]
            celulares = [kwargs.get('celular')]
            emails = [kwargs.get('email')]
        elif 'nombre' in request.POST:
            # Caso: contacto único enviado desde POST
            nombres = [request.POST.get('nombre')]
            apellidos = [request.POST.get('apellido')]
            telefonos = [request.POST.get('telefono')]
            celulares = [request.POST.get('celular')]
            emails = [request.POST.get('email')]
        elif 'nombre[]' in request.POST:
            # Caso: múltiples contactos enviados desde POST
            nombres = request.POST.getlist('nombre[]')
            apellidos = request.POST.getlist('apellido[]')
            telefonos = request.POST.getlist('telefono[]')
            celulares = request.POST.getlist('celular[]')
            emails = request.POST.getlist('email[]')
        else:
            nombres = []
            apellidos = []
            telefonos = []
            celulares = []
            emails = []

        print(f"Contactos recibidos: {nombres}")
        print(f"Apellidos recibidos: {apellidos}")

        # Iterar sobre los contactos recibidos
        for i in range(len(nombres)):
            nombre = nombres[i]
            apellido = apellidos[i] if i < len(apellidos) else None
            telefono = telefonos[i] if i < len(telefonos) else None
            celular = celulares[i] if i < len(celulares) else None
            email = emails[i] if i < len(emails) else None

            # Verificar si los campos requeridos están completos
            if nombre and apellido:
                nombreCompleto = f"{nombre} {apellido}"

                # Crear el contacto en la base de datos
                ContactoDB.objects.create(
                    codigoInternoSap=1,  # Aquí puedes manejar la lógica del código interno si es variable
                    nombreCompleto=nombreCompleto,
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    celular=celular,
                    email=email,
                    SocioNegocio=cliente
                )
                print(f"Contacto {i+1} creado con éxito: {nombreCompleto}")
            else:
                print(f"No se ha creado el contacto {i+1} porque algunos campos están vacíos.")

    return render(request, "cotizacion.html", {'clienteNoIncluido': clienteNoIncluido})


@login_required
def guardarContactosAJAX(request):
    if request.method == "POST":
        # Parsear los datos del cliente
        cliente_id = request.POST.get('rutSN')  # Verificar que este campo corresponde al RUT
        try:
            cliente = SocioNegocioDB.objects.get(rut=cliente_id)
        except SocioNegocioDB.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cliente no encontrado'})

        # Obtener las listas de contactos desde el QueryDict
        nombres = request.POST.getlist('nombre[]')
        apellidos = request.POST.getlist('apellido[]')
        telefonos = request.POST.getlist('telefono[]')
        celulares = request.POST.getlist('celular[]')
        emails = request.POST.getlist('email[]')

        # Iterar sobre los contactos
        for i in range(len(nombres)):
            nombre = nombres[i]
            apellido = apellidos[i]
            telefono = telefonos[i] if i < len(telefonos) else None
            celular = celulares[i] if i < len(celulares) else None
            email = emails[i] if i < len(emails) else None

            # Verificar que los campos requeridos estén completos
            if nombre and apellido:
                nombre_completo = f"{nombre} {apellido}"

                # Crear o actualizar el contacto
                ContactoDB.objects.create(
                    codigoInternoSap=1,  # Ajustar esta lógica según sea necesario
                    nombreCompleto=nombre_completo,
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    celular=celular,
                    email=email,
                    SocioNegocio=cliente
                )
                print(f"Contacto {nombre_completo} creado con éxito")
            else:
                print(f"No se ha creado el contacto porque algunos campos están vacíos.")

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def busquedaProductos(request):
    if request.method == 'GET' and 'numero' in request.GET:
        numero = request.GET.get('numero')
        # Realiza la consulta a la base de datos para obtener los resultados
        resultados = ProductoDB.objects.filter(codigo__icontains=numero)
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


""" @require_http_methods(["GET"])
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
"""


def quotate_items(request, docEntry):
    client = APIClient()  

    try:
        data = client.get_quotations_items('Quotations', docEntry)  # Ajusta según el método de cliente API

        # Verificar si hay datos y procesarlos
        if 'value' in data:
            quotations = data['value']
            found_quotation = None

            # Buscar la cotización con el DocNum especificado
            for quotation in quotations:
                if quotation.get('DocEntry') == int(docEntry):  # Convertir docNum a entero si es necesario
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
    
def probandoSL(request):
    client = APIClient()
    docentry = 143563

    documentClient = client.detalleCotizacionCliente(docentry)
    documentLine = client.detalleCotizacionLineas(docentry)


    data = {
        "Client": documentClient,
        "DocumentLine": documentLine
    }

    cotiza = Cotizacion()

    lines_data = cotiza.formatearDatos(data)


    return JsonResponse(lines_data, safe=False)


def obtenerStockBodegas(request):
    producto_id = request.GET.get('idProducto')  # Obtener el ID del producto

    if not producto_id:
        return JsonResponse({'error': 'Falta el parámetro: idProducto es obligatorio'}, status=400)

    try:
        repo = StockBodegasRepository()
        stock_por_bodegas = repo.consultarStockPorProducto(producto_id)

        # Crear la respuesta con la información de todas las bodegas asociadas
        data = [
            {
                'bodega': item.idBodega.codigo,
                'stock': item.stock
            }
            for item in stock_por_bodegas
        ]

        return JsonResponse(data, safe=False, status=200)

    except StockBodegasDB.DoesNotExist:
        return JsonResponse({'error': 'No se encontró stock para este producto'}, status=404)

def obtenerRegionesId(request):
    numeroRegion = request.GET.get('numero')  # Obtener el ID de la región

    if not numeroRegion:
        return JsonResponse({'error': 'Falta el parámetro: idRegion es obligatorio'}, status=400)

    try:
        region = RegionRepository()

        region = region.obtenerRegionPorId(numeroRegion)

        print(f"Región encontrada: {region}")

        data = {
            'numero': region.numero,
            'nombre': region.nombre        
            }

        return JsonResponse(data, status=200)

    except RegionDB.DoesNotExist:
        return JsonResponse({'error': 'No se encontró la región solicitada'}, status=404)

def  obtenerComunasId(request):
    codigo_comuna = request.GET.get('codigo')  # Obtener el ID de la comuna

    if not codigo_comuna:
        return JsonResponse({'error': 'Falta el parámetro: idComuna es obligatorio'}, status=400)

    try:
        comuna = ComunaRepository()

        comuna = comuna.obtenerComunaPorId(codigo_comuna)

        data = {
            'codigo': comuna.codigo,
            'nombre': comuna.nombre,
            'region': comuna.region.nombre
        }

        return JsonResponse(data, status=200)

    except ComunaDB.DoesNotExist:
        return JsonResponse({'error': 'No se encontró la comuna solicitada'}, status=404)

def trigger_sync(request):
    try:
        sync_products.delay()  # Dispara la tarea encolada
        return JsonResponse({'status': 'Sincronización en cola'})
    except TimeoutError:
        return JsonResponse({'status': 'Error: RabbitMQ no está disponible'}, status=500)
    
def pruebas(request):
    
    pro = Producto()
    obtenerReceta = pro.obtenerReceta("B25400084K2")

    return JsonResponse(obtenerReceta, safe=False)

def pryebas(request):
    sl = APIClient()

    odv = sl.getODV()

    return JsonResponse(odv, safe=False)

def onbtenerImgProducto(request):
    codigo = request.GET.get('codigo')

    if not codigo:
        return JsonResponse({'error': 'Falta el parámetro: idProducto es obligatorio'}, status=400)

    try:
        producto = ProductoDB.objects.get(codigo=codigo)

        data = {
            'imagen': producto.imagen
        }

        return JsonResponse(data, status=200)

    except ProductoDB.DoesNotExist:
        return JsonResponse({'error': 'No se encontró el producto solicitado'}, status=404)
    

def report(request):
    #create the HttpResponse header with PDF
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    #create the PDF object, using the response object as its "file"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    #header
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30,750,'Reporte de Ventas')
    c.setFont('Helvetica', 12)
    c.drawString(30,735,'Showroom')
    
    c.setFont('Helvetica-Bold', 12)
    c.drawString(480,750,"2024")
    
    c.line(460,747,560,747)
    
    #table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]  
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10
    
    numero = Paragraph('''#''', styleBH)
    nombre = Paragraph('''Nombre''', styleBH)
    precio = Paragraph('''Precio''', styleBH)
    stock = Paragraph('''Stock''', styleBH)
    precioAnterior = Paragraph('''Precio Anterior''', styleBH)
    maxDescuento = Paragraph('''Descuento Máximo''', styleBH)
    total = Paragraph('''Total''', styleBH)
    data = []
    
    #table
    
    data.append([numero, nombre, precio, stock, precioAnterior, maxDescuento, total])
    
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7
    
    width, height = A4
    
    high = 650
    for producto in ProductoDB.objects.all():
        this_prod = [producto.codigo, producto.nombre, producto.precioVenta, producto.stockTotal, producto.precioLista, producto.dsctoMaxTienda, producto.stockTotal * producto.precioVenta]
        data.append(this_prod)
        high = high - 18
        
    #table size
    table = Table(data, colWidths=[1.9*cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    
    #pdf size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage()
    
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    
    