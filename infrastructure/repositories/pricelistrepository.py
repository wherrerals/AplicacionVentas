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
    def get_product_price(sku):
        """Obtiene la relación producto-lista de precios"""
        return PriceListProductDB.objects.filter(code_product=sku).first()

    @staticmethod
    def get_price_list(code_list):
        """Obtiene una lista de precios por su código"""
        return PriceListsDB.objects.filter(code_list=code_list).first()
