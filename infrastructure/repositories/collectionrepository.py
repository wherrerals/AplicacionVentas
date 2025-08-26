from infrastructure.models.collectionproductsdb import CollectionsProducts


class CollectionRepository:
    @staticmethod
    def product_in_collections(product_codigo, collections) -> bool:
        """
        Verifica si un producto pertenece a alguna de las colecciones dadas.
        
        Args:
            product_codigo: Código del producto a verificar
            collections: QuerySet de colecciones donde buscar
            
        Returns:
            bool: True si el producto está en alguna colección, False en caso contrario
        """
        return CollectionsProducts.objects.filter(
            product__codigo=product_codigo,
            collection__in=collections
        ).exists()


    @staticmethod
    def validate_coupon_does_not_apply(collections) -> bool:
        """
        Valida el campo coupon_does_not_apply de la colección asociada al cupón.
        
        Args:
            collections: QuerySet de colecciones asociadas al cupón
            
        Returns:
            bool: True si es colección exclusiva (coupon_does_not_apply=True)
                False si es colección inclusiva (coupon_does_not_apply=False)
                
        Note: Asume que solo hay una colección por cupón según reglas de negocio
        """
        collection = collections.first()
        if collection:
            return collection.coupon_does_not_apply
        return False
    
