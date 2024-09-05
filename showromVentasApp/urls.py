from django.urls import path
from showromVentasApp.views.cotizacionesview import Cotizaciones
from showromVentasApp.views.socionegocioview import SocioNegocioView
from showromVentasApp.views.productoview import Productos
from showromVentasApp.views import view

urlpatterns = [
    path('', view.home, name="home"),
    path('listado_Cotizaciones/', Cotizaciones.as_view(), name='listado_Cotizaciones'),
    path('listado_Cotizaciones_filtrado/', Cotizaciones.as_view(), name='crearCotizacion'),
    path('crear_cotizacion/', Cotizaciones.as_view(), name='create_quotation'),
    path('agregar_editar_clientes/', SocioNegocioView.as_view(), name='agregar_editar_clientes'),
    path('buscar_clientes/', SocioNegocioView.as_view(), name='busquedaClientes'),
    path('listado_productos/', Productos.as_view(), name='listado_productos'),
    # Rutas adicionales
    path('lista_cotizaciones/', view.list_quotations, name="lista_cotizaciones"),
    path('generar_cotizacion/', view.quotations, name="generar_cotizacion"),
    path('lista_ovs/', view.lista_ovs, name='lista_ovs'),
    path('lista_solic_devoluciones/', view.lista_solic_devoluciones, name='lista_solic_devoluciones'),
    path('lista_clientes/', view.lista_clientes, name='lista_clientes'),
    path('creacion_clientes/', view.creacion_clientes, name='creacion_clientes'),
    path('reporte_stock/', view.reporte_stock, name='reporte_stock'),
    path('micuenta/', view.micuenta, name='micuenta'),
    path('lista_usuarios/', view.lista_usuarios, name='lista_usuarios'),
    path('salir/', view.userLogout, name='salir'),
    path('registrarCuenta/', view.registrarCuenta, name='registrarCuenta'),
    path('buscarproductos/', view.busquedaProductos, name='busquedaProductos'),
    path('mis_datos/', view.mis_datos, name='mis_datos'),
    path('agregar_direccion/', view.agregarDireccion, name='agregar_direccion'),
    path('generar_cotizacion/<str:docEntry>/', view.quotate_items, name='generar_cotizacion'),
]