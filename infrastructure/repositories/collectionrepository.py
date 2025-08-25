from infrastructure.models.collectionproductsdb import CollectionsProducts


class CollectionRepository:
    @staticmethod
    def product_in_collections(product_codigo, collections):
        """
        Verifica si un producto pertenece a alguna de las colecciones dadas.
        Retorna una lista de colecciones donde aparece.
        """
        return CollectionsProducts.objects.filter(
            product__codigo=product_codigo,
            collection__in=collections
        ).values_list("collection__coupon_does_not_apply", flat=True)
