from django.urls import path
from logicaVentasApp.views.cotizacionController import CotizacionesController
from logicaVentasApp.views.clienteController import SocioNegocioController
from logicaVentasApp.views.productoController import ProductosController

urlpatterns = [
    path('listado_Cotizaciones/', CotizacionesController.as_view(), name='listado_Cotizaciones'),
    path('listado_Cotizaciones_filtrado/', CotizacionesController.as_view(), name='crearCotizacion'),
    path('crear_cotizacion/', CotizacionesController.as_view(), name='create_quotation'),
    path('agregar_editar_clientes/', SocioNegocioController.as_view(),name='agregar_editar_clientes'),
    path('generar_cotizacion/<str:DocEntry>/', SocioNegocioController.as_view(), name='generar_cotizacion'),
    path('buscarc/', SocioNegocioController.as_view(), name='busquedaClientes'),
    path('listado_productos/', ProductosController.as_view(), name='listado_productos'),
    #path('obtener_detalles_cotizacion/<int:docEntry>/', CotizacionesController.as_view(), name='obtener_detalles_cotizacion'),
    #path('listado_Cotizaciones_filtrado/', Documento.as_view(), name='filter_quotations'),
    #path('listado_Cotizaciones/', Documento.as_view(), name='listado_Cotizaciones'),
    #path('obtener_detalles_cotizacion/<int:docNum>/', CotizacionesController.as_view({'get': 'obtenerDetallesCotizacion'}), name='obtener_detalles_cotizacion'),
    #path('generar_cotizacion/<str:docNum>/', quotate_items, name='generar_cotizacion'),
    #path('buscarc/', ClienteController.as_view(), name='busquedaClientes'),
]
