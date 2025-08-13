from django.utils import timezone
from infrastructure.models.couponsdb import CouponsDB
from infrastructure.models.rulescouponsrelation import CouponRuleRelation
from domain.services.couponvalidator import CouponValidator


class Coupons():

    def __init__(self, coupon, products, doc_total):
        try:
            self.coupon = CouponsDB.objects.get(cupon_code=coupon)
            self.exist = True
            self.products = products
            self.doc_total = doc_total
        except CouponsDB.DoesNotExist:
            self.coupon = None
            self.exist = False
            self.products = None
            self.doc_total = None

    def coupon_vality_date(self):

        now = timezone.now()
        if self.coupon.valid_from and self.coupon.valid_to and not (self.coupon.valid_to <= now <= self.coupon.valid_from):
            return True
        return False

    def coupon_is_active(self):
        if self.coupon.active:
            return True
        return False        

    def get_coupon_discount(self):
        return self.coupon.discount_percentage
    
    def rules_coupon(self):

        if not self.coupon:
            return None
        rules_with_values = CouponRuleRelation.objects.filter(coupon=self.coupon).select_related('rule')

        result = []

        for rule in rules_with_values:
            result.append({
                'operator': rule.rule.operator,
                'max_value': rule.max_value,
                'min_value': rule.min_value
            })
        
        return result if result else None
    
    def products_apply_coupon(self):
        products = self.coupon.products.all()
        if not products:
            return None
        return list(products.values('codigo'))
    
    def coupon_error(self):
        
        error = []

        if not self.exist:
            error.append("El Cupon no existe")
            return ''.join(error)
        
        if not self.coupon_vality_date():
            error.append("El Cupon {coupon} ha caducado")

        if not self.coupon_is_active():
            error.append("El Cupon {coupon} no esta activo")

        return ''.join(error)
    

    def get_coupon(self):
        
        errors = self.coupon_error()
        if errors:
            return {"error": errors}
        
        discount = self.get_coupon_discount()
        rules = self.rules_coupon()
        product_codes = [p['itemCode'] for p in self.products]


        if rules and rules[0]['operator'] == 'todo':
            applicable_codes = product_codes
        else:
            valid_codes = set(p['codigo'] for p in self.coupon.products.all().values('codigo'))
            applicable_codes = list(valid_codes.intersection(product_codes))

        validator = CouponValidator(applicable_codes, rules, self.doc_total)
        filtered_products = validator.get_applicable_products()

        return {"success": True, 
                "discount": discount, 
                "products": [{"codigo": p.codigo} for p in filtered_products],
                "rules": rules[0] if rules else None,
                }