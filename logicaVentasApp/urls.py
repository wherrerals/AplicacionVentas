from django.urls import path
from logicaVentasApp.views.cotizaciones import Cotizaciones
from logicaVentasApp.views.socioNegocio import SocioNegocio
from logicaVentasApp.views.producto import Productos

urlpatterns = [
    path('listado_Cotizaciones/', Cotizaciones.as_view(), name='listado_Cotizaciones'),
    path('listado_Cotizaciones_filtrado/', Cotizaciones.as_view(), name='crearCotizacion'),
    path('crear_cotizacion/', Cotizaciones.as_view(), name='create_quotation'),
    path('ventas/agregar_editar_clientes/', SocioNegocio.as_view(),name='agregar_editar_clientes'),
    path('ventas/buscarc/', SocioNegocio.as_view(), name='busquedaClientes'),
    path('listado_productos/', Productos.as_view(), name='listado_productos'),
    #path('obtener_detalles_cotizacion/<int:docEntry>/', CotizacionesController.as_view(), name='obtener_detalles_cotizacion'),
    #path('listado_Cotizaciones_filtrado/', Documento.as_view(), name='filter_quotations'),
    #path('listado_Cotizaciones/', Documento.as_view(), name='listado_Cotizaciones'),
    #path('obtener_detalles_cotizacion/<int:docNum>/', CotizacionesController.as_view({'get': 'obtenerDetallesCotizacion'}), name='obtener_detalles_cotizacion'),
    #path('generar_cotizacion/<str:docNum>/', quotate_items, name='generar_cotizacion'),
    #path('buscarc/', ClienteController.as_view(), name='busquedaClientes'),
]
