from django.urls import path
from logicaVentasApp.views.cotizacionController import CotizacionesController

urlpatterns = [
    path('listado_Cotizaciones/', CotizacionesController.as_view(), name='listado_Cotizaciones'),
    path('listado_Cotizaciones_filtrado/', CotizacionesController.as_view(), name='filter_quotations'),
]
