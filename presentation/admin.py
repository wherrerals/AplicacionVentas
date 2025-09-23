import csv
from pyexpat.errors import messages
from django import forms
from django.contrib import admin
from django.shortcuts import render
from django.db import transaction
from infrastructure.models import (
    CondicionPagoDB,
    DocumentoDB,
    TipoDocTributarioDB,
    SucursalDB,
    TipoVentaDB,
    VendedorDB,
    ProductoDB,
    BodegaDB,
    InventarioDB,
    LineaDB,
    SocioNegocioDB,
    UsuarioDB,
    ContactoDB,
    DireccionDB,
    ComunaDB,
    GrupoSNDB,
    TipoSNDB,
    TipoClienteDB,
    TipoEntregaDB,
    TipoObjetoSapDB,
    CollectionDB
)

from infrastructure.models.couponsdb import CouponsDB
from infrastructure.models.pricelistsdb import PriceListsDB
from infrastructure.models.pricelistproductdb import PriceListProductDB
from infrastructure.models.regiondb import RegionDB
from infrastructure.models.stockbodegasdb import StockBodegasDB
from infrastructure.models.confiDescuentosDB import ConfiDescuentosDB
from infrastructure.models.confiEmpresaDB import ConfiEmpresaDB


import logging

logger = logging.getLogger(__name__)

# Modificaciones en administrador
admin.site.site_header = "Led Studio"
admin.site.site_title = "Led Studio Admin"
admin.site.index_title = "Aplicacion Ventas Led Studio"
 

# Mejora interfaz modelos
class TipoDocTributarioDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")

class CuponesDBper(admin.ModelAdmin):
    list_display = (
        "cupon_code",
        "name",
        "description",
        "active",
        "valid_from",
        "valid_to",
        "discount_percentage",
        "max_uses",
        "one_use_only",
        "coupon_type",
        "same_price_and_discount",
        "last_modification",
    )
    search_fields = ["cupon_code", "name"]
    list_filter = ("active", "coupon_type")
    ordering = ("-last_modification",)

class TipoEntregaDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")

class TipoObjetoSapDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "descripcion")

class SucursalDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")


class TipoVentaDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")


class BodegaDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "descripcion")


class CondicionPagoper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")


class VendedorDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "tipoVendedor")


class DocumentoDBper(admin.ModelAdmin):
    list_display = (
        "id",
        "docEntry",
        "folio",
        "totalAntesDelDescuento",
        "totalDocumento",
        "socio_negocio",
    )


class InventarioDBper(admin.ModelAdmin):
    list_display = ("producto", "bodega")


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Selecciona archivo CSV",
        help_text="El archivo debe tener las columnas: codigo, imagen",
    )


class Productosper(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "stockTotal",
        "precioLista",
        "precioVenta",
        "imagen",
        "dsctoMaxTienda",
    )
    search_fields = ["codigo", "nombre"]
    change_list_template = "admin/productos_changelist.html"

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        try:
            if request.method == "POST":
                form = CsvImportForm(request.POST, request.FILES)
                logger.debug(f"Form data: {request.POST}")
                logger.debug(f"Files: {request.FILES}")

                if form.is_valid():
                    csv_file = request.FILES["csv_file"]
                    if not csv_file.name.endswith(".csv"):
                        self.message_user(
                            request, "El archivo debe ser CSV", level=40
                        )  # ERROR
                        return render(request, "admin/csv_form.html", {"form": form})

                    try:
                        # Leer el archivo CSV correctamente
                        decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
                        reader = csv.DictReader(decoded_file, delimiter=";")

                        # Registrar las columnas detectadas
                        logger.debug(f"Column names: {reader.fieldnames}")

                        updated_count = 0
                        errors = []
                        for row in reader:
                            if "codigo" in row and "imagen" in row:
                                try:
                                    producto = self.model.objects.get(
                                        codigo=row["codigo"]
                                    )
                                    producto.imagen = row["imagen"]
                                    producto.save()
                                    updated_count += 1
                                except self.model.DoesNotExist:
                                    errors.append(
                                        f'Producto con código {row["codigo"]} no encontrado'
                                    )
                                    continue
                            else:
                                errors.append(
                                    'El CSV debe contener las columnas "codigo" e "imagen"'
                                )
                                break

                        if errors:
                            for error in errors:
                                self.message_user(request, error, level=30)  # WARNING
                        if updated_count:
                            self.message_user(
                                request,
                                f"Se actualizaron {updated_count} imágenes correctamente",
                                level=25,  # SUCCESS
                            )
                        return self.changelist_view(request)

                    except Exception as e:
                        logger.error(f"Error processing CSV: {str(e)}")
                        self.message_user(
                            request,
                            f"Error procesando el archivo: {str(e)}",
                            level=40,  # ERROR
                        )
                        return render(request, "admin/csv_form.html", {"form": form})
                else:
                    logger.error(f"Form errors: {form.errors}")
                    for field, errors in form.errors.items():
                        for error in errors:
                            self.message_user(
                                request, f"Error en {field}: {error}", level=40  # ERROR
                            )
                    return render(request, "admin/csv_form.html", {"form": form})

            form = CsvImportForm()
            return render(request, "admin/csv_form.html", {"form": form})

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            self.message_user(request, f"Error inesperado: {str(e)}", level=40)  # ERROR


class LineaDBper(admin.ModelAdmin):
    list_display = ("producto", "cantidad", "precioUnitario", "totalNetoLinea", "totalBrutoLinea")


class SocioNegocioDBper(admin.ModelAdmin):
    list_display = ("nombre", "razonSocial", "email", "telefono", "condicionPago")
    search_fields = ["codigoSN", "nombre"]


class UsuarioDBper(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono", "usuarios", "sucursal", "vendedor")


class ContactoDBper(admin.ModelAdmin):
    list_display = ("nombreCompleto",)


class DireccionDBper(admin.ModelAdmin):
    list_display = ("rowNum", "nombreDireccion")


class GrupoSnDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")


class TipoSNDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")


class TipoClienteDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre")


class RegionDBper(admin.ModelAdmin):
    list_display = ("numero", "nombre")


class ComunaDBper(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "region")


class stockBodegasDBper(admin.ModelAdmin):
    list_display = ("idProducto", "idBodega", "stock", "stockDisponibleReal")
    search_fields = ["idProducto", "idBodega"]


class ConfiDescuentosDBper(admin.ModelAdmin):
    list_display = (
        "codigo",
        "descripcion",
        "tipoVenta",
        "limiteDescuentoMaximo",
        "tipoDeMarca",
    )


class ConfiEmpresaDBper(admin.ModelAdmin):
    list_display = (
        "id",
        "razonsocial",
        "rut",
        "direccion",
        "rentabilidadBrutaMin",
        "rentabilidadBrutaConAut",
    )

class CollectionDBper(admin.ModelAdmin):
    list_display = ("collection_id", "coupon_does_not_apply", "coupon_does_not_apply")

class PriceListsDBper(admin.ModelAdmin):
    list_display = ("code_list", "name", "description", "valid_from", "valid_to", "active", "last_modification")
    search_fields = ["code_list", "name"]
    list_filter = ("active",)
    ordering = ("-last_modification",)


class PriceListProductDBper(admin.ModelAdmin):
    list_display = ("code_list", "code_product", "price_list")
    search_fields = ["code_list__code_list", "code_product__codigo"]
    list_filter = ("code_list",)
    ordering = ("code_list", "code_product")

    change_list_template = "admin/pricelistproduct_changelist.html"

    def get_urls(self):

        from django.urls import path

        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls


    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                if not csv_file.name.endswith(".csv"):
                    self.message_user(request, "El archivo debe ser CSV", level=40)  # ERROR
                    return render(request, "admin/csv_form2.html", {"form": form})

                try:
                    decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
                    reader = csv.DictReader(decoded_file, delimiter=";")

                    created_count = 0
                    updated_count = 0
                    errors = []

                    with transaction.atomic():
                        for row in reader:
                            if "code_list" in row and "code_product" in row and "price_list" in row:
                                try:
                                    # Buscar FKs usando los códigos
                                    code_list = PriceListsDB.objects.get(code_list=row["code_list"])
                                    code_product = ProductoDB.objects.get(codigo=row["code_product"])

                                    # Crear o actualizar
                                    obj, created = self.model.objects.update_or_create(
                                        code_list=code_list,
                                        code_product=code_product,
                                        defaults={"price_list": row["price_list"]},
                                    )

                                    if created:
                                        created_count += 1
                                    else:
                                        updated_count += 1

                                except PriceListsDB.DoesNotExist:
                                    errors.append(f'Lista de precios con código {row["code_list"]} no existe')
                                except ProductoDB.DoesNotExist:
                                    errors.append(f'Producto con código {row["code_product"]} no existe')
                                except Exception as e:
                                    errors.append(
                                        f"Error con fila {row}: {str(e)}"
                                    )
                            else:
                                errors.append(
                                    'El CSV debe contener las columnas "code_list", "code_product" y "price_list"'
                                )
                                break

                    # Mensajes al usuario
                    if created_count:
                        self.message_user(
                            request,
                            f"✅ Se crearon {created_count} precios nuevos",
                            level=25,
                        )
                    if updated_count:
                        self.message_user(
                            request,
                            f"🔄 Se actualizaron {updated_count} precios",
                            level=25,
                        )
                    if errors:
                        for error in errors:
                            self.message_user(request, f"⚠️ {error}", level=30)

                    return self.changelist_view(request)

                except Exception as e:
                    self.message_user(
                        request,
                        f"Error procesando el archivo: {str(e)}",
                        level=40,  # ERROR
                    )
                    return render(request, "admin/csv_form2.html", {"form": form})
            else:
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        self.message_user(request, f"Error en {field}: {error}", level=40)
                return render(request, "admin/csv_form2.html", {"form": form})

        # GET → mostrar formulario vacío
        form = CsvImportForm()
        return render(request, "admin/csv_form2.html", {"form": form})



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
# admin.site.register(DireccionDB, DireccionDBper)
admin.site.register(ComunaDB, ComunaDBper)
admin.site.register(RegionDB, RegionDBper)
admin.site.register(StockBodegasDB, stockBodegasDBper)
admin.site.register(ConfiDescuentosDB, ConfiDescuentosDBper)
admin.site.register(ConfiEmpresaDB, ConfiEmpresaDBper)
admin.site.register(TipoEntregaDB, TipoEntregaDBper)
admin.site.register(TipoObjetoSapDB, TipoObjetoSapDBper)
admin.site.register(CouponsDB, CuponesDBper)
admin.site.register(CollectionDB, CollectionDBper)
admin.site.register(PriceListsDB, PriceListsDBper)
admin.site.register(PriceListProductDB, PriceListProductDBper)