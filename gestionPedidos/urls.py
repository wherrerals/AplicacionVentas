from django.urls import path
from gestionPedidos import views
from .views import  *

urlpatterns = [
    path('', views.home, name="home"),
    path('lista_cotizaciones', views.list_quotations, name="lista_cotizaciones"),
    path('generar_cotizacion', views.quotations, name="generar_cotizacion"),
    path('cotizacion/', views.quotations_view, name='cotizacion'),
    path('lista_ovs', views.lista_ovs, name='lista_ovs'),
    path('generar_cotizacion/<str:docNum>/', quotate_items, name='generar_cotizacion'),
    path('post-quotations/', post_quotations, name='post_quotations'),
    path('lista_solic_devoluciones', views.lista_solic_devoluciones, name='lista_solic_devoluciones'),
    path('lista_clientes', views.lista_clientes, name='lista_clientes'),
    path('creacion_clientes/', views.creacion_clientes, name='creacion_clientes'),
    path('reporte_stock', views.reporte_stock, name='reporte_stock'),
    path('micuenta', views.micuenta, name='micuenta'),
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('salir/', views.salir, name='salir'),
    path('registrarCuenta/', views.registrarCuenta),
    #path('funciones/<str:motor>/<str:accion>/<str:param>/', Funciones.as_view(), name="funciones"),
    path('obtener-datos-producto/<int:producto_id>/', views.obtenerDatosProducto, name='obtenerDatosProducto'),
    #path('buscar/', views.busquedaProductos, name='busquedaProductos'),
    path('mis_datos/', views.mis_datos, name='mis_datos'),
    path('agregar_editar_clientes/',views.agregar_editar_clientes,name='agregar_editar_clientes'),
    path('agregar_direccion/',views.agregar_direccion,name='agregar_direccion'),
    #path('buscarc/', views.busquedaClientes, name='busquedaClientes'),
    path('buscarc/', BusquedaClientes.as_view(), name='busquedaClientes'),
    path('buscar/', BusquedaProductosView.as_view(), name='buscar/'),
    path('listado_Cotizaciones/', views.list_quotations_2, name='listado_Cotizaciones'),
    path('ordenes/', views.cambio_ordenes, name='ordenes'),
    path('probandoVtex/', views.oredenes, name='probandoVtex'),
]

