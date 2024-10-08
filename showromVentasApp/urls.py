from django.urls import path
from showromVentasApp.views.cotizacionview import CotizacionView
from showromVentasApp.views.socionegocioview import SocioNegocioView
from showromVentasApp.views.productoview import Productos
from showromVentasApp.views import view

cotizacionView = CotizacionView()


urlpatterns = [
    path('', view.home, name="home"),
    path('listado_Cotizaciones/', CotizacionView.as_view(), name='listado_Cotizaciones'),
    path('listado_Cotizaciones_filtrado/', CotizacionView.as_view(), name='listado_Cotizaciones_filtrado'),
    path('agregar_editar_clientes/', SocioNegocioView.as_view(), name='agregar_editar_clientes'),
    path('buscar_clientes/', SocioNegocioView.as_view(), name='busquedaClientes'),
    path('verificar_cliente/', SocioNegocioView.as_view(), name='verificar_cliente'),
    path('listado_productos/', Productos.as_view(), name='listado_productos'),
    path('crear_cotizacion/', CotizacionView.as_view(), name='crear_cotizacion'),
    path('crear_cliente/', SocioNegocioView.as_view(), name='crear_cliente'),
    path('cambiar_estado_cotizacion/', CotizacionView.as_view(), name='cambiar_estado_cotizacion'),
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
    path('obtener_detalles_cotizacion/<int:docEntry>/', cotizacionView.obtenerDetallesCotizacion, name='obtener_detalles_cotizacion'),
    path('guardar_contactos/', view.guardarContactosAJAX, name='guardar_contactos_ajx'), 
]

""" Este es el path que estaba probando
    path('guardar_contactos/', view.guardarContactosAJAX, name='guardar_contactos_ajx'), 
"""