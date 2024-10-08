#Django modulos
from django.shortcuts import render, redirect  
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


#librerias Python usadas
import requests
import json

#Inicio vistas Renderizadoras

"""
Decoradores usados: 
    @login_required: Decorador que indica que solo se ejecuta el template si el usurio esta logeado
    @transaction.atomic: Decorador usado para vistas que realizan  un conjunto de operaciones sobre la db, permitiendo que todas se ejecuten con exito o ninguna se aplique si ocurre un error. 
"""

@login_required
def home(request):
    """
    Rendereriza la pagina principal y muestra el nombre del usuario que ha iniciado sesión

    Args: 
        request (HttpRequest): La petición HTTP recibida.

    Returns:
        HttpResponse: Si el ususario esta autenticado renderiza el template 'home.html' con el nombre de usuario.
        HttpResponse: Si el usuario no esta autenticado redirige a el template del login.
    """

    if request.user.is_authenticated:
        username = request.user.username 
        return render(request, 'home.html', {'username': username}) # Accede al nombre de usuario y permite su uso en el template


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
        
        except UsuarioDB.DoesNotExist: 
            pass

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
            'nombreuser': nombreUser
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


@login_required
def agregarDireccion(request, socio):
    if request.method == "POST":
        nombredirecciones = request.POST.getlist('nombre_direccion[]')
        ciudades = request.POST.getlist('ciudad[]')
        callesnumeros = request.POST.getlist('direccion[]')
        tipos = request.POST.getlist('tipodireccion[]')
        paises = request.POST.getlist('pais[]')
        regiones = request.POST.getlist('region[]')
        comunas = request.POST.getlist('comuna[]')
        print(f"nombre direccion: " , nombredirecciones)
        print(f"nombres de cuidades: " , ciudades)
        print(f"tipo de direcciones: " , tipos)



        for i in range(len(nombredirecciones)):
            nombredireccion = nombredirecciones[i]
            ciudad = ciudades[i]
            callenumero = callesnumeros[i]
            tipo = tipos[i]
            pais = paises[i]
            region = regiones[i]
            comuna = comunas[i]

            # Verificar si existe un campo requerido
            if nombredireccion:
                fregion = RegionDB.objects.get(numero=region)
                fcomuna = ComunaDB.objects.get(codigo=comuna)

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
            else:
                print(f"No se ha creado la dirección {i+1} porque algunos campos están vacíos.")
    return redirect("/")




@login_required
def agregarContacto(request, cliente):
    if request.method == "POST":
        nombres = request.POST.getlist('nombre[]')
        apellidos = request.POST.getlist('apellido[]')
        telefonos = request.POST.getlist('telefono[]')
        celulares = request.POST.getlist('celular[]')
        emails = request.POST.getlist('email[]')

        clienteNoIncluido = None

        if cliente is None:
            clienteNoIncluido = "No se ha incluido el cliente en la solicitud."


        print(f"contactos recibidos: " ,nombres)
        print(f"contactos recibidos: " ,apellidos)

        for i in range(len(nombres)):
            nombre = nombres[i]
            apellido = apellidos[i]
            telefono = telefonos[i]
            celular = celulares[i]
            email = emails[i]

            # Verificar si los campos requeridos están completos
            if nombre and apellido:
                nombreCompleto = f"{nombre} {apellido}"

                ContactoDB.objects.create(
                    codigoInternoSap=1,  # Aquí deberías manejar la lógica del código interno si es variable
                    nombreCompleto=nombreCompleto,
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    celular=celular,
                    email=email,
                    SocioNegocio=cliente
                )
                print(f"Contacto {i+1} creado con éxito")
            else:
                print(f"No se ha creado el contacto {i+1} porque algunos campos están vacíos.")
    return render(request, "cotizacion.html", {'clienteNoIncluido': clienteNoIncluido})

"""
Este metodo sirve para poder guardar los contactos de un cliente en la base de datos a traves de una peticion AJAX
        creada en los modales, cuando se desea agregar un contacto o editar un contacto de un cliente ya existente.
        Con este estaba probando pero no lo logre. (no empece con el de direcciones)
"""

@login_required
def guardarContactosAJAX(request):
    
    if request.method == "POST":
        # Parsear los datos de contactos desde el request
        contactos_json = request.POST.get('contactos')
        contactos = json.loads(contactos_json)

        cliente_id = request.POST.get('cliente')
        cliente = SocioNegocioDB.objects.get(rut=cliente_id)

        # Verificar que el cliente exista
        if not cliente:
            return JsonResponse({'success': False, 'message': 'Cliente no encontrado'})

        # Iterar sobre los contactos recibidos
        for contacto in contactos:
            nombre = contacto['nombre']
            apellido = contacto['apellido']
            telefono = contacto.get('telefono')
            celular = contacto.get('celular')
            email = contacto.get('email')

            # Verificar si los campos requeridos están completos
            if nombre and apellido:
                nombreCompleto = f"{nombre} {apellido}"

                # Crear o actualizar el contacto
                ContactoDB.objects.create(
                    codigoInternoSap=1,  # Aquí deberías manejar la lógica del código interno si es variable
                    nombreCompleto=nombreCompleto,
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    celular=celular,
                    email=email,
                    SocioNegocio=cliente
                )
                print(f"Contacto {nombreCompleto} creado con éxito")
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
    
