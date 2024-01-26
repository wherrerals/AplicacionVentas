from django.contrib import admin
from gestionPedidos.models import *

#Modicaciones en administrador 
admin.site.site_header = 'Led Studio'
admin.site.site_title = 'Led Studio Admin'
admin.site.index_title = 'Aplicacion Ventas Led Studio'

# Register your models here.
admin.site.register(TipoDocTributario)
admin.site.register(Sucursal)
admin.site.register(TipoVenta)
admin.site.register(Vendedor)
admin.site.register(Documento)
admin.site.register(CondicionPago)
admin.site.register(Producto)
admin.site.register(Bodega)
admin.site.register(Inventario)
admin.site.register(Item)
admin.site.register(SocioNegocio)
admin.site.register(Usuario)









