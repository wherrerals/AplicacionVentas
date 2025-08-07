from datosLsApp.models.productodb import ProductoDB


class CouponValidator:
    def __init__(self, product_codes, rules, doc_total):
        """
        products: lista de diccionarios o instancias con precios
        rules: lista de reglas [{'operator': '>', 'min_value': ..., 'max_value': ...}]
        """
        self.products = ProductoDB.objects.filter(codigo__in=product_codes)
        self.rules = rules
        self.doc_total = doc_total

    def _apply_rule(self, product_price, rule):
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
        if not self.rules:
            return []

        rule = self.rules[0]

        applicable = []
        
        for product in self.products:
            price = product.precioVenta  # o precioLista, según el negocio
            if self._apply_rule(price, rule):
                applicable.append(product)

        return applicable
