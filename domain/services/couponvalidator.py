from infrastructure.models.productodb import ProductoDB
from infrastructure.repositories.collectionrepository import CollectionRepository


class CouponValidator:
    def __init__(self, product_codes, rules, doc_total, coupon, users_data=None):

        print(f"Inicializando CouponValidator con cupon: {coupon}")
        """
        products: lista de diccionarios o instancias con precios
        rules: lista de reglas [{'operator': '>', 'min_value': ..., 'max_value': ...}]
        """
        self.products = list(ProductoDB.objects.filter(codigo__in=product_codes))
        self.rules = rules
        self.doc_total = doc_total
        self.coupon = coupon
        self.users_data = users_data

        print(f"cupon: {self.coupon}")

    def _apply_rule(self, rule):
        op = rule['operator']
        min_val = rule.get('min_value')
        max_val = rule.get('max_value')
        document_total = float(self.doc_total if self.doc_total else 0)
        
        if op == '==':
            return document_total == min_val
        elif op == '>':
            return document_total > min_val
        elif op == '<':
            return document_total < max_val
        elif op == '!=':
            return document_total != min_val
        return False

    def get_applicable_products(self):
        """
        Retorna productos aplicables según criterios del cupón.
        - same_price_and_discount=True: productos sin descuento (precioVenta == precioLista)
        - same_price_and_discount=False: todos los productos
        """

        print(f"validando productos: {[p.codigo for p in self.products]}")
        if not self.products:
            return []

        if self.coupon.same_price_and_discount:
            print("Aplicando filtro de productos con mismo precio y descuento")
            print(f"{self.coupon.same_price_and_discount}")
            # Solo productos sin diferencia de precios
            return [p for p in self.products if p.precioVenta == p.precioLista]
        
        # Si es falso, aplica a todos
        return self.products
    

    def validate_products(self, product_list):
        """
        Retorna lista final de productos aplicando las reglas de collections.
        
        Reglas:
        - Si no hay colecciones: todos los productos son válidos
        - Si coupon_does_not_apply = False: solo productos EN la colección
        - Si coupon_does_not_apply = True: solo productos FUERA de la colección
        """
        collections = self.coupon.collections.all()
        
        # Si no hay colecciones asociadas, todos los productos son válidos
        if not collections.exists():
            return product_list
        
        # Obtener la configuración global de la colección
        is_exclusive_collection = CollectionRepository.validate_coupon_does_not_apply(collections)
        print(f"Colección es exclusiva (coupon_does_not_apply): {is_exclusive_collection}")
        
        productos_validos = []
        
        for product in product_list:
            # Verificar si el producto está en alguna colección
            product_is_in_collection = CollectionRepository.product_in_collections(product.codigo, collections)
            print(f"Producto {product.codigo} está en colección: {product_is_in_collection}")
            
            # Aplicar lógica según el tipo de colección
            if is_exclusive_collection:
                # Colección exclusiva: solo productos FUERA de la colección
                if not product_is_in_collection:
                    productos_validos.append(product)
            else:
                # Colección inclusiva: solo productos DENTRO de la colección
                if product_is_in_collection:
                    productos_validos.append(product)
        
        return productos_validos


    def get_discounted_products(self, filtered_products, discount):
        filtered_products = self.validate_products(filtered_products)
        print(f"Productos filtrados después de omitir colecciones: {filtered_products}")

        products_with_discounts = []
        for product in filtered_products:
            if self.coupon.exceed_maximum_discount:
                final_discount = discount
            else:
                from presentation.views.view import limitar_descuento
                limite_producto = limitar_descuento(product, self.users_data, 0.0, 0.0) / 100
                final_discount = min(discount, limite_producto)

            products_with_discounts.append({
                "codigo": product.codigo,
                "descuento": final_discount
            })

        return products_with_discounts
    
    
    