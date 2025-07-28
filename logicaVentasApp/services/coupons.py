from django.utils import timezone
from datosLsApp.models.couponsdb import CouponsDB


class Coupons():

    def __init__(self, coupon, products):
        try:
            self.coupon = CouponsDB.objects.get(cupon_code=coupon)
            self.exist = True
            self.products = products
        except CouponsDB.DoesNotExist:
            self.coupon = None
            self.exist = False
            self.products = None

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
        rules = self.coupon.rules.all()
        if not rules:
            return None
        return list(rules.values('operator'))
    
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
        print("rules", rules)
        products = self.products_apply_coupon()

        return {"success": True, "discount": discount, "products": products, "rules": rules[0]}

