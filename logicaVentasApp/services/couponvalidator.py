from datosLsApp.models.productodb import ProductoDB


class CouponValidator:
    def __init__(self, product_codes, rules):
        """
        products: lista de diccionarios o instancias con precios
        rules: lista de reglas [{'operator': '>', 'min_value': ..., 'max_value': ...}]
        """
        self.products = ProductoDB.objects.filter(codigo__in=product_codes)
        self.rules = rules

    def _apply_rule(self, product_price, rule):
        op = rule['operator']
        min_val = rule.get('min_value')
        max_val = rule.get('max_value')

        print(f"Applying rule: {op}, min: {min_val}, max: {max_val} on price: {product_price}")

        if op == '==':
            return product_price == min_val
        elif op == '>':
            return product_price > min_val
        elif op == '<':
            return product_price < max_val
        elif op == '!=':
            return product_price != min_val
        elif op == 'todo':  # aplica a todos
            return True
        return False

    def get_applicable_products(self):
        if not self.rules:
            return []

        rule = self.rules[0]

        applicable = []
        
        for product in self.products:
            price = product.precioVenta  # o precioLista, según el negocio
            if self._apply_rule(price, rule):
                applicable.append(product)

        return applicable
