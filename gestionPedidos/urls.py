from django.urls import path
from gestionPedidos import views
from .views import ejemplo


urlpatterns = [
    path('', views.home, name="home"),
    path('lista_cotizaciones', views.lista_cotizaciones, name="lista_cotizaciones"),
    path('lista_ovs', views.lista_ovs, name='lista_ovs'),
    path('lista_solic_devoluciones', views.lista_solic_devoluciones, name='lista_solic_devoluciones'),
    path('lista_clientes', views.lista_clientes, name='lista_clientes'),
    path('reporte_stock', views.reporte_stock, name='reporte_stock'),
    path('micuenta', views.micuenta, name='micuenta'),
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('salir/', views.salir, name='salir'),
    path('clientes/', views.clientes, name='clientes/'),
    path('registrarCuenta/', views.registrarCuenta),
    path('ejemplo/', ejemplo.as_view(), name="ejemplo")


]

