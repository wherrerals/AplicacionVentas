from django.urls import path
from showromVentasApp.views.cotizacionview import CotizacionView
from showromVentasApp.views.devolucionesview import ReturnsView
from showromVentasApp.views.odvView import OdvView
from showromVentasApp.views.invoiceView import InvoiceView
from showromVentasApp.views.socionegocioview import SocioNegocioView
from showromVentasApp.views.productoview import Productos
from showromVentasApp.views import view

cotizacionView = CotizacionView()


urlpatterns = [
    path('', view.home, name="home"),
    path('agregar_editar_clientes/', SocioNegocioView.as_view(), name='agregar_editar_clientes'),
    path('listado_socios_negocio/', SocioNegocioView.as_view(), name='listado_socios_negocio'),
    path('informacion_cliente/', SocioNegocioView.as_view(), name='informacion_cliente'),
    path('buscar_clientes/', SocioNegocioView.as_view(), name='busquedaClientes'),
    path('verificar_cliente/', SocioNegocioView.as_view(), name='verificar_cliente'),
    path('filtrar_socios_negocio/', SocioNegocioView.as_view(), name='filtrar_socios_negocio'),
    path('crear_cotizacion/', CotizacionView.as_view(), name='crear_cotizacion'),
    path('copiar_a_odv/', CotizacionView.as_view(), name='copiar_a_odv'),
    path('cambiar_estado_cotizacion/', CotizacionView.as_view(), name='cambiar_estado_cotizacion'),
    path('listado_Cotizaciones/', CotizacionView.as_view(), name='listado_Cotizaciones'),
    path('listado_Cotizaciones_filtrado/', CotizacionView.as_view(), name='listado_Cotizaciones_filtrado'),
    path('listado_odv/', OdvView.as_view(), name='listado_odv'),
    path('crear_odv/', OdvView.as_view(), name='crear_odv'),
    path('detalles_ODV/', OdvView.as_view(), name='detalles_ODV'),
    path('detalles_devolucion/', ReturnsView.as_view(), name='detalles_devolucion'),
    path('detalles_devolucion_pendiente/', ReturnsView.as_view(), name='detalles_devolucion_pendiente'),
    path('listado_solicitudes_devolucion/', ReturnsView.as_view(), name='listado_solicitudes_devolucion'),
    path('crear_devolucion/', ReturnsView.as_view(), name='crear_devolucion'),
    path('productos/', Productos.as_view(), name='productos'),
    path('solicitudes_pendientes/', ReturnsView.as_view(), name='solicitudes_pendientes'),
    path('consulta-ventas/', InvoiceView.as_view(), name='consulta_ventas'),
    path('lista-ventas/', InvoiceView.as_view(), name='lista_ventas'),
    path('lista_cotizaciones/', view.list_quotations, name="lista_cotizaciones"),
    path('generar_cotizacion/', view.quotations, name="generar_cotizacion"),
    path('lista_ovs/', view.lista_ovs, name='lista_ovs'),
    path('lista_solic_devoluciones/', view.lista_solic_devoluciones, name='lista_solic_devoluciones'),
    path('pending_rr/', view.return_request_pending, name='pending_rr'),
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
    path('guardar_contactos/', view.guardarContactosAJAX, name='guardar_contactos_ajx'), 
    path('guardar_direcciones/<str:socio>/', view.actualizarAgregarDirecion, name='guardar_direccion'),
    path('guardar_contactos/<str:socio>/', view.actualizarAgregarContacto, name='guardar_contactos'),
    path('obtener_comunas_por_region/', view.enlazarComunas, name='obtener_comunas_por_region'),
    path('obter_region_id/', view.obtenerRegionesId, name='obtener_region_id'),
    path('obtener_comuna_id/', view.obtenerComunasId, name='obtener_comuna_id'),
    path('obtener_stock_bodegas/', view.obtenerStockBodegas, name='obtener_stock'),
    path('detalles_cotizacion/', cotizacionView.detallesCotizacion, name='detalles_cotizacion'),
    path('get_docEntry/', cotizacionView.get_docEntry, name='get_docEntry'),    
    path('duplicar_cotizacion/', cotizacionView.duplicarCotizacion, name='duplicar_cotizacion'),
    path('ordenesVentas/', view.odv, name='ordenesVentas'),
    path('solicitudes_devolucion/', view.return_requests, name='solicitudes_devolucion'),
    path('imagen/', view.onbtenerImgProducto, name='imagen'),
    path('pruebas/', view.pryebas, name='pruebas'),
    path('cotizacion/<int:cotizacion_id>/pdf/', view.generar_cotizacion_pdf_2, name='cotizacion_pdf'),
    path('get_vendedor_sucursal/', view.get_vendedor_sucursal, name='get_vendedor_sucursal'),
    path('generar_cotizacion_pdf/<int:cotizacion_id>/pdf/', view.generar_cotizacion_pdf, name='generar_cotizacion_pdf'),
    path('verificar_estado_pdf/<str:task_id>/', view.verificar_estado_pdf, name='verificar_estado_pdf'),
    path('prueba/', view.prueba, name='prueba'),
    path('actualizando_recetas/', view.probandoActualizador, name='actualizando_recetas'),
    path('obtener-ventas/', InvoiceView.as_view(), name='obtener_ventas'),
    path('detalles-ventas/', InvoiceView.as_view(), name='detalles_ventas'),
    path('duplicar-documento/', InvoiceView.as_view(), name='duplicar_documento'),
    path('get_doctotal/', view.get_doctotal, name='get_doctotal'),

]