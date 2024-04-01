from django.contrib import admin
from gestionPedidos.models import *

#Modicaciones en administrador 
admin.site.site_header = 'Led Studio'
admin.site.site_title = 'Led Studio Admin'
admin.site.index_title = 'Aplicacion Ventas Led Studio'

#mejora interfaz modelos
class TipoDocTributarioper(admin.ModelAdmin): #revisar
    list_display = ('codigo','nombre')

class Sucursalper(admin.ModelAdmin):
    list_display = ('codigo','nombre')

class TipoVentaper(admin.ModelAdmin):
    list_display = ('codigo','nombre')

class bodegaper(admin.ModelAdmin):
    list_display = ('codigo','nombre','descripcion')

class condicionPagoper(admin.ModelAdmin):
    list_display = ('codigo','nombre')

class vendedorper(admin.ModelAdmin):
    list_display = ('codigo','nombre','sucursal')

class documentoper(admin.ModelAdmin): 
    list_display = ('docEntry','folio','totalAntesDelDescuento','totalDocumento','vendedor')

class Inventarioper(admin.ModelAdmin):
    list_display = ('producto','bodega')

class productosper(admin.ModelAdmin):
    list_display = ('codigo','nombre','stockTotal','precioLista','precioVenta')

class itemper(admin.ModelAdmin):
    list_display = ('producto','cantidad','descuento')

class SocioNegocioper(admin.ModelAdmin):
    list_display = ('nombre','razonSocial','email','telefono','condicionPago')

class Usuarioper(admin.ModelAdmin):
    list_display = ('nombre', 'email','telefono')

class Contactoper(admin.ModelAdmin):
    list_display = ('nombreCompleto',)



# Register your models here.
admin.site.register(TipoDocTributario,TipoDocTributarioper)
admin.site.register(Sucursal,Sucursalper)
admin.site.register(TipoVenta,TipoVentaper)
admin.site.register(Vendedor,vendedorper)
admin.site.register(Documento,documentoper)
admin.site.register(CondicionPago,condicionPagoper)
admin.site.register(Producto,productosper)
admin.site.register(Bodega,bodegaper)
admin.site.register(Inventario,Inventarioper)
admin.site.register(Item,itemper)
admin.site.register(SocioNegocio,SocioNegocioper)
admin.site.register(Usuario,Usuarioper)
admin.site.register(Contacto, Contactoper)













