from django.contrib import admin
from datosLsApp.models import (
    CondicionPagoDB, DocumentoDB, TipoDocTributarioDB, SucursalDB, 
    TipoVentaDB, VendedorDB, ProductoDB, BodegaDB, InventarioDB, 
    LineaDB, SocioNegocioDB, UsuarioDB, ContactoDB, DireccionDB, ComunaDB,
    GrupoSNDB, TipoSNDB, TipoClienteDB
)
from datosLsApp.models.regiondb import RegionDB

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
    search_fields = ['codigo', 'nombre']

class LineaDBper(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'descuento')

class SocioNegocioDBper(admin.ModelAdmin):
    list_display = ('nombre', 'razonSocial', 'email', 'telefono', 'condicionPago')
    search_fields = ['codigoSN', 'nombre']


class UsuarioDBper(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'sucursal', 'usuarios')

class ContactoDBper(admin.ModelAdmin):
    list_display = ('nombreCompleto',)
 
class DireccionDBper(admin.ModelAdmin):
    list_display = ('rowNum', 'nombreDireccion')

class GrupoSnDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class TipoSNDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class TipoClienteDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class RegionDBper(admin.ModelAdmin):
    list_display = ('numero', 'nombre')

class ComunaDBper(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'region')

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
admin.site.register(LineaDB, LineaDBper)
admin.site.register(SocioNegocioDB, SocioNegocioDBper)
admin.site.register(UsuarioDB, UsuarioDBper)
admin.site.register(ContactoDB, ContactoDBper)
admin.site.register(DireccionDB, DireccionDBper)
admin.site.register(GrupoSNDB, GrupoSnDBper)
admin.site.register(TipoSNDB, TipoSNDBper)
admin.site.register(TipoClienteDB, TipoClienteDBper)
#admin.site.register(DireccionDB, DireccionDBper)
admin.site.register(ComunaDB, ComunaDBper)
admin.site.register(RegionDB, RegionDBper)
