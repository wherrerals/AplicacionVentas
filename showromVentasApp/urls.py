from django.urls import path
from showromVentasApp import views
from .views import  *

urlpatterns = [
    path('', views.home, name="home"),
    path('lista_cotizaciones', views.list_quotations, name="lista_cotizaciones"),
    path('generar_cotizacion', views.quotations, name="generar_cotizacion"),
    path('lista_ovs', views.lista_ovs, name='lista_ovs'),
    path('lista_solic_devoluciones', views.lista_solic_devoluciones, name='lista_solic_devoluciones'),
    path('lista_clientes', views.lista_clientes, name='lista_clientes'),
    path('creacion_clientes/', views.creacion_clientes, name='creacion_clientes'),
    path('reporte_stock', views.reporte_stock, name='reporte_stock'),
    path('micuenta', views.micuenta, name='micuenta'),
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('salir/', views.userLogout, name='salir'),
    path('registrarCuenta/', views.registrarCuenta),
    #path('funciones/<str:motor>/<str:accion>/<str:param>/', Funciones.as_view(), name="funciones"),
    path('buscar/', views.busquedaProductos, name='busquedaProductos'),
    path('mis_datos/', views.mis_datos, name='mis_datos'),
    path('agregar_direccion/',views.agregar_direccion,name='agregar_direccion'),
    #path('ordenes/', views.cambio_ordenes, name='ordenes'),
    path('generar_cotizacion/<str:docEntry>/', quotate_items, name='generar_cotizacion'),

]

