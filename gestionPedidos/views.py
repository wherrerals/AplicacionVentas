#Django modulos
from django.shortcuts import render, redirect  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.http import JsonResponse
#Modulos Diseñados
from gestionPedidos.models import *
from .api_client import APIClient
from .vtex_client import VTEXClient
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
    else:
        return render(request, '/')

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

    Captura de la url el parametro DocNum y, si este no esta presente, lo establece en null
    También obtiene todas las instancias del modelo 'Region' para ser utilizadas en el template.

    Args: 
        request (HttpsRequest): La peticion HTTP recibida
    
    Returns: 
        HttpResponse: Renderiza el template 'cotizacion.html' con el nombre de usuario y el DocNum
        HttpResponse: Si el usuario no esta autenticado redirige a el template del inicio.
    """

    if request.user.is_authenticated:
        username = request.user.username
    
        doc_num = request.GET.get('docNum', None)

        regiones = Region.objects.all()


        context = {
            'docnum': doc_num,
            'username': username,
            'regiones': regiones
        }

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
#desde ambos botones se puede llamar y usar el tipo para ver donde se muestra en "barras (ajax)"
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


def busquedaClientes(request):
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
        
        return JsonResponse({'resultadosClientes': resultados_formateados})
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
    
def oredenes(request):
        
    return render(request, "manejo_ordenes.html")

def cambio_ordenes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_number = data.get('orderNumber')

            # Consulta a la API de Service Layer
            client = APIClient()
            service_layer_data = client.get_orders(order_number)
            
            if 'value' in service_layer_data and len(service_layer_data['value']) > 0:
                first_item = service_layer_data['value'][0]  # Tomamos el primer elemento de 'value'
                folio_number = first_item.get('FolioNumber')
                u_report_pdf = first_item.get('U_ReportPdf')

                print(f'FolioNumber: {folio_number}')
                print(f'U_ReportPdf: {u_report_pdf}')
            else:
                return JsonResponse({'message': 'No se encontraron datos en Service Layer para el número de orden especificado'}, status=404)
            
            # Consulta a la API de VTEX
            vtex_client = VTEXClient()
            vtex_data = vtex_client.get_order_details(order_number)

            value = vtex_data.get('value')
            creation_date = vtex_data.get('creationDate')

            print(f'value: {value}')
            print(f'creationDate: {creation_date}')

            # Construir el JSON y enviarlo a otra URL de VTEX
            payload = {
                "type":'Output', #string
                "issuanceDate": creation_date, #string
                # Agregar otros campos del payload según sea necesario
                "invoiceNumber": folio_number, #string
                "invoiceValue": value, #string revisar que el campo en el excel sea si o si tipo numero, luego de agg los dos 00 adicionales
                "invoiceKey": '', #string 
                "invoiceUrl": u_report_pdf, #string 
                "courier": '', #string 
                "trackingNumber": '', #string 
                "trackingUrl": '', #string 
                "dispatchedDate": '', #string 
            }

            vtex_post_url = f'https://ledstudiocl.myvtex.com/api/oms/pvt/orders/{order_number}/invoice'
            vtex_post_response = requests.post(vtex_post_url, json=payload, headers=vtex_client.headers)
            vtex_post_response.raise_for_status()

            return JsonResponse({'message': 'Proceso completado exitosamente', 'data': vtex_post_response.json()})
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Error al decodificar JSON en la solicitud'}, status=400)
        
        except requests.RequestException as e:
            return JsonResponse({'message': 'Error al hacer la solicitud a VTEX', 'error': str(e)}, status=500)
        
        except Exception as e:
            return JsonResponse({'message': 'Error al procesar la solicitud', 'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_exempt
@require_POST
def filter_quotations(request):
    print("Request body:", request.body)  # Verifica el cuerpo de la solicitud JSON recibida
    
    client = APIClient()

    try:
        data = json.loads(request.body)
        print("Received data:", data)  # Verifica los datos JSON recibidos
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    filters = {}

    # Agregar filtros solo si se proporcionan datos válidos
    if data.get('fecha_inicio'):
        filters['Quotations/DocDate ge'] = f"'{data.get('fecha_inicio')}'"
    if data.get('fecha_fin'):
        filters['Quotations/DocDate le'] = f"'{data.get('fecha_fin')}'"
    if data.get('docNum'):
        filters['contains(Quotations/DocNum,'] = data.get('docNum')
    if data.get('carCode'):
        filters['contains(Quotations/CardCode,'] = f"'{data.get('carCode')}'"
    if data.get('cardNAme'):
        filters['contains(Quotations/CardName,'] = f"'{data.get('cardNAme')}'"
    if data.get('salesEmployeeName'):
        filters['contains(SalesPersons/SalesEmployeeName,'] = f"'{data.get('salesEmployeeName')}'"
    if data.get('DocumentStatus'):
        filters['Quotations/DocumentStatus eq'] = f"'{data.get('DocumentStatus')}'"
    if data.get('docTotal'):
        filters['contains(Quotations/DocTotal,'] = data.get('docTotal')
    if data.get('cancelled'):
        filters['Quotations/Cancelled eq'] = f"'{data.get('cancelled')}'"

    # Limpiar los filtros vacíos o con valores inválidos
    filters = {k: v for k, v in filters.items() if v and v != "''"}

    try:
        top = int(data.get('top', 20))
        skip = int(data.get('skip', 0))
    except ValueError:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    print("Applying filters:", filters)  # Verifica los filtros aplicados

    try:
        data = client.get_quotations2(top=top, skip=skip, filters=filters)
        return JsonResponse({'data': data}, safe=False)
    except Exception as e:
        print("Error:", e)  # Verifica el error específico que está ocurriendo
        return JsonResponse({'error': str(e)}, status=500)

