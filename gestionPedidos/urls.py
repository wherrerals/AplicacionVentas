from django.urls import path
from gestionPedidos import views
from .views import Funciones, BusquedaClientes


urlpatterns = [
    path('', views.home, name="home"),
    path('lista_cotizaciones', views.lista_cotizaciones, name="lista_cotizaciones"),
    path('generar_cotizacion', views.cotizacion, name="generar_cotizacion"),
    path('lista_ovs', views.lista_ovs, name='lista_ovs'),
    path('lista_solic_devoluciones', views.lista_solic_devoluciones, name='lista_solic_devoluciones'),
    path('lista_clientes', views.lista_clientes, name='lista_clientes'),
    path('creacion_clientes/', views.creacion_clientes, name='creacion_clientes'),
    path('reporte_stock', views.reporte_stock, name='reporte_stock'),
    path('micuenta', views.micuenta, name='micuenta'),
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('salir/', views.salir, name='salir'),
    path('registrarCuenta/', views.registrarCuenta),
    path('funciones/<str:motor>/<str:accion>/<str:param>/', Funciones.as_view(), name="funciones"),
    path('obtener-datos-producto/<int:producto_id>/', views.obtenerDatosProducto, name='obtenerDatosProducto'),
    path('buscar/', views.busquedaProductos, name='busquedaProductos'),
    path('mis_datos/', views.mis_datos, name='mis_datos'),
    path('agregar_editar_clientes/',views.agregar_editar_clientes,name='agregar_editar_clientes'),
    path('agregar_direccion/',views.agregar_direccion,name='agregar_direccion'),
    #path('buscarc/', views.busquedaClientes, name='busquedaClientes'),
    path('buscarc/', BusquedaClientes.as_view(), name='busquedaClientes'),
    path('test/', views.test_connection, name='test'),
]

