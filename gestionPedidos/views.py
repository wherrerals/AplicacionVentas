from django.shortcuts import render, redirect, HttpResponse # importa el metodo render 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from gestionPedidos.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

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
    #tipo_usuario = request.POST['tipo_usuario']
    telefono = request.POST['telefono']
    #showroom = request.POST['showroom']
    #numero_sap = request.POST['num_sap']
    #clave = request.POST['clave']

    cuenta = Usuario.objects.create(nombre=nombre, email=email, telefono=telefono)

    return redirect('/')

@login_required
def lista_usuarios(request):
    return render(request, "lista_usuarios.html")


@login_required
def clientes(request):
    return render(request, "cliente.html")

@api_view(['GET'])
def api_lista_clientes(request):
    usuarios = Usuario.objects.all()
    data = [{'nombre': usuario.nombre, 'email': str(usuario.email)} for usuario in usuarios]
    return Response(data)

@api_view(['POST'])
def guardar_clientes(request):
    usuarios = Usuario.objects.all()
    data = [{'nombre': usuario.nombre, 'email': str(usuario.email), } for usuario in usuarios]
    return Response(data)
