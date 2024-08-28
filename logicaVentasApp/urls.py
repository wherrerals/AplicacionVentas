from django.urls import path
from logicaVentasApp.views.cotizacionController import CotizacionesController
from logicaVentasApp.views.documentoController import Documento

urlpatterns = [
    path('listado_Cotizaciones/', CotizacionesController.as_view(), name='listado_Cotizaciones'),
    path('listado_Cotizaciones_filtrado/', CotizacionesController.as_view(), name='crearCotizacion'),
    path('crear_cotizacion/', CotizacionesController.as_view(), name='create_quotation'),
    #path('listado_Cotizaciones_filtrado/', Documento.as_view(), name='filter_quotations'),
    #path('listado_Cotizaciones/', Documento.as_view(), name='listado_Cotizaciones'),
]
