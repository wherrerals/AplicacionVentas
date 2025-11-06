from infrastructure.models.pricelistsdb import PriceListsDB
from infrastructure.models.pricelistproductdb import PriceListProductDB


class PriceListRepository:
    """
    Repository para acceder a listas de precios y sus productos.
    Encapsula toda la lógica de consultas al ORM.
    """

    @staticmethod
    def get_price_list_by_sku(sku):
        """Obtiene la lista de precios asociada a un SKU"""
        
        product_price = PriceListProductDB.objects.filter(code_product=sku).first()
        return product_price.code_list if product_price else None

    @staticmethod
    def get_product_price(sku, cardCode=None):
        """Obtiene la relación producto-lista de precios"""
        from infrastructure.models.socionegociodb import SocioNegocioDB

        socio = SocioNegocioDB.objects.filter(codigoSN=cardCode).select_related('price_list_asigned').first()
        
        print("Buscando lista de precios para el SKU:", sku)

        # validar si el sku hace parte de la lista de productos de precio del socio

        product_in_list = PriceListProductDB.objects.filter(code_product=sku, code_list=socio.price_list_asigned).first() if socio and socio.price_list_asigned else None
        if product_in_list:
            if socio and socio.price_list_asigned:
                print("Socio tiene lista de precios asignada:", socio.price_list_asigned, "para el SKU: ", sku)
                prueba = PriceListProductDB.objects.filter(code_list=socio.price_list_asigned, code_product__codigo=sku).first()
                print("Resultado de la consulta:", prueba)
                return PriceListProductDB.objects.filter(code_list=socio.price_list_asigned, code_product__codigo=sku).first()

        prueba = PriceListProductDB.objects.filter(code_product=sku).exclude(code_list__list_only_for_members=True).first()
        print("Resultado de la consulta sin socio:", prueba)
        return PriceListProductDB.objects.filter(code_product=sku).exclude(code_list__list_only_for_members=True).first()

    @staticmethod
    def get_price_list(code_list):
        """Obtiene una lista de precios por su código"""
        return PriceListsDB.objects.filter(code_list=code_list).first()