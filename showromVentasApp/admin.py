from django.contrib import admin
from datosLsApp.models import (
    CondicionPagoDB, DocumentoDB, TipoDocTributarioDB, SucursalDB, 
    TipoVentaDB, VendedorDB, ProductoDB, BodegaDB, InventarioDB, 
    ItemDB, SocioNegocioDB, UsuarioDB, ContactoDB, DireccionDB, ComunaDB
)

# Modificaciones en administrador
admin.site.site_header = 'Led Studio'
admin.site.site_title = 'Led Studio Admin'
admin.site.index_title = 'Aplicacion Ventas Led Studio'

# Mejora interfaz modelos
class TipoDocTributarioDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class SucursalDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class TipoVentaDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class BodegaDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'descripcion')

class CondicionPagoper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class VendedorDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'sucursal')

class DocumentoDBper(admin.ModelAdmin):
    list_display = ('docEntry', 'folio', 'totalAntesDelDescuento', 'totalDocumento', 'vendedor')

class InventarioDBper(admin.ModelAdmin):
    list_display = ('producto', 'bodega')

class Productosper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'stockTotal', 'precioLista', 'precioVenta')

class ItemDBper(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'descuento')

class SocioNegocioDBper(admin.ModelAdmin):
    list_display = ('nombre', 'razonSocial', 'email', 'telefono', 'condicionPago')

class UsuarioDBper(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono')

class ContactoDBper(admin.ModelAdmin):
    list_display = ('nombreCompleto',)
 
class DireccionDBper(admin.ModelAdmin):
    list_display = ('nombre', 'region', 'socioNegocio')

# Register your models here.
admin.site.register(TipoDocTributarioDB, TipoDocTributarioDBper)
admin.site.register(SucursalDB, SucursalDBper)
admin.site.register(TipoVentaDB, TipoVentaDBper)
admin.site.register(VendedorDB, VendedorDBper)
admin.site.register(DocumentoDB, DocumentoDBper)
admin.site.register(CondicionPagoDB, CondicionPagoper)
admin.site.register(ProductoDB, Productosper)
admin.site.register(BodegaDB, BodegaDBper)
admin.site.register(InventarioDB, InventarioDBper)
admin.site.register(ItemDB, ItemDBper)
admin.site.register(SocioNegocioDB, SocioNegocioDBper)
admin.site.register(UsuarioDB, UsuarioDBper)
admin.site.register(ContactoDB, ContactoDBper)
#admin.site.register(DireccionDB, DireccionDBper)
admin.site.register(ComunaDB)
