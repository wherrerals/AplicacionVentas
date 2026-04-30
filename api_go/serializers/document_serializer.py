from rest_framework import serializers
from datetime import datetime


class DocumentLineSerializer(serializers.Serializer):
    LineNum = serializers.IntegerField()
    sku = serializers.CharField(source="ItemCode")
    imagen = serializers.SerializerMethodField()
    comentarios = serializers.CharField(source="FreeText", allow_blank=True)
    descripcion = serializers.CharField(source="ItemDescription")
    cantidad = serializers.SerializerMethodField()
    porcentaje_descuento = serializers.FloatField(source="DiscountPercent")
    descuento = serializers.SerializerMethodField()
    precio_unitario = serializers.SerializerMethodField()
    subtotal_neto = serializers.SerializerMethodField()

    def get_cantidad(self, obj):
        return str(int(obj.get("Quantity", 0)))

    def _format_currency(self, value):
        return f"$ {int(round(value, 0)):,}".replace(",", ".")

    def get_descuento(self, obj):
        return self._format_currency(obj.get("PriceAfterVAT", 0))

    def get_precio_unitario(self, obj):
        return self._format_currency(obj.get("PriceAfterVAT", 0))

    def get_subtotal_neto(self, obj):
        return self._format_currency(obj.get("PriceAfterVAT", 0))

    def get_imagen(self, obj):
        from infrastructure.models.productodb import ProductoDB

        item_code = obj.get("ItemCode")

        if not item_code:
            return None

        # cache para evitar N queries
        if not hasattr(self, "_producto_cache"):
            self._producto_cache = {}

        if item_code in self._producto_cache:
            return self._producto_cache[item_code]

        producto = ProductoDB.objects.filter(
            codigo=item_code
        ).only("imagen").first()

        if not producto or not producto.imagen:
            self._producto_cache[item_code] = None
            return None

        # si es ImageField
        imagen_url = producto.imagen

        self._producto_cache[item_code] = imagen_url
        return imagen_url

class CotizacionSerializer(serializers.Serializer):
    tipo_documento = serializers.SerializerMethodField()
    numero = serializers.CharField(source="Cliente.Quotations.DocNum")
    fecha = serializers.CharField(source="Cliente.Quotations.DocDate")
    valido_hasta = serializers.CharField(source="Cliente.Quotations.DocDate")
    rut = serializers.CharField(source="Cliente.Quotations.CardCode")
    vendedor = serializers.CharField(source="Cliente.SalesPersons.SalesEmployeeCode")

    DocumentLines = DocumentLineSerializer(many=True)

    totalbruto = serializers.SerializerMethodField()
    iva = serializers.SerializerMethodField()
    totalNeto = serializers.SerializerMethodField()

    direccion = serializers.SerializerMethodField()
    contacto = serializers.SerializerMethodField()
    sucursal = serializers.CharField(source="Cliente.SalesPersons.U_LED_SUCURS")
    observaciones = serializers.CharField(source="Cliente.Quotations.Comments", allow_blank=True)

    pdf_button = serializers.SerializerMethodField()

    # -----------------------
    # Métodos custom
    # -----------------------

    def get_tipo_documento(self, obj):
        return "COTI"


    def _format_currency(self, value):
        return f"$ {int(round(value, 0)):,}".replace(",", ".")

    def get_totalbruto(self, obj):
        return self._format_currency(obj["Cliente"]["Quotations"]["DocTotal"])

    def get_iva(self, obj):
        return self._format_currency(obj["Cliente"]["Quotations"]["VatSum"])

    def get_totalNeto(self, obj):
        return self._format_currency(obj["Cliente"]["Quotations"]["DocTotalNeto"])

    def get_pdf_button(self, obj):
        return 2
            
    def get_direccion(self, obj):
        from infrastructure.models.direcciondb import DireccionDB

        codigo_sn = obj["Cliente"]["Quotations"].get("CardCode")

        if not codigo_sn:
            return None

        # cache para evitar múltiples queries
        if not hasattr(self, "_direccion_cache"):
            self._direccion_cache = {}

        if codigo_sn in self._direccion_cache:
            return self._direccion_cache[codigo_sn]

        direccion = DireccionDB.objects.filter(
            SocioNegocio__codigoSN=codigo_sn,
            es_principal=True  # 👈 importante
        ).only("id").first()

        # fallback si no hay principal
        if not direccion:
            direccion = DireccionDB.objects.filter(
                SocioNegocio__codigoSN=codigo_sn
            ).only("id").first()

        if not direccion:
            self._direccion_cache[codigo_sn] = None
            return None

        self._direccion_cache[codigo_sn] = direccion.id
        return direccion.id
    
    def get_contacto(self, obj):
        from infrastructure.models.contactodb import ContactoDB

        codigo_sn = obj["Cliente"]["Quotations"].get("CardCode")

        if not codigo_sn:
            return None
        
        if not hasattr(self, "_contacto_cache"):
            self._contacto_cache = {}

        if codigo_sn in self._contacto_cache:
            return self._contacto_cache[codigo_sn]
        
        contacto = ContactoDB.objects.filter(
            SocioNegocio__codigoSN=codigo_sn
        ).only("id").first()

        if not contacto:
            self._contacto_cache[codigo_sn] = None
            return None

        self._contacto_cache[codigo_sn] = contacto.id
        return contacto.id