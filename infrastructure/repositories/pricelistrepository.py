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
        """Obtiene el precio del producto según prioridad: 
        1. Lista asignada al cliente
        2. Lista activa general
        """

        from infrastructure.models.socionegociodb import SocioNegocioDB

        # 1. Buscar socio
        socio = None
        if cardCode:
            socio = (SocioNegocioDB.objects.filter(codigoSN=cardCode).select_related('price_list_asigned').first())

        # 2. Prioridad: lista asignada al socio
        if socio and socio.price_list_asigned:
            lista_cliente = socio.price_list_asigned

            product = (
                PriceListProductDB.objects.filter(code_list=lista_cliente, code_product__codigo=sku).first()
                )

            if product:
                return product

        # 3. Sin socio o sin precio en la lista del socio: usar la lista activa
        lista_activa = (
            PriceListsDB.objects.filter(active=True).exclude(list_only_for_members=True).first()
        )

        if not lista_activa:
            return None

        return (
            PriceListProductDB.objects.filter(code_list=lista_activa, code_product__codigo=sku).first()
        )

    
    @staticmethod
    def get_price_list(code_list):
        """Obtiene una lista de precios por su código"""
        return PriceListsDB.objects.filter(code_list=code_list).first()