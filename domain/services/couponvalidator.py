from infrastructure.models.productodb import ProductoDB


class CouponValidator:
    def __init__(self, product_codes, rules, doc_total, cupon):
        """
        products: lista de diccionarios o instancias con precios
        rules: lista de reglas [{'operator': '>', 'min_value': ..., 'max_value': ...}]
        """
        self.products = ProductoDB.objects.filter(codigo__in=product_codes)
        self.rules = rules
        self.doc_total = doc_total
        self.cupon = cupon

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

        if self.cupon.same_price_and_discount:
            print("Aplicando filtro de productos con mismo precio y descuento")
            print(f"{self.cupon.same_price_and_discount}")
            # Solo productos sin diferencia de precios
            return [p for p in self.products if p.precioVenta == p.precioLista]
        
        # Si es falso, aplica a todos
        return self.products

    def get_discounted_products(self):
        """
        Retorna productos que tienen un descuento aplicado.
        """
        return [p for p in self.products if p.descuento > 0]
