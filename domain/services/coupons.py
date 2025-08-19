from django.utils import timezone
from infrastructure.models.couponsdb import CouponsDB
from infrastructure.models.rulescouponsrelation import CouponRuleRelation
from domain.services.couponvalidator import CouponValidator


class Coupons():

    def __init__(self, coupon, products, doc_total, users_data, sncode):
        try:
            self.coupon = CouponsDB.objects.get(cupon_code=coupon)
            self.exist = True
            self.products = products
            self.doc_total = doc_total
            self.users_data = users_data
            self.sncode = sncode
        except CouponsDB.DoesNotExist:
            self.coupon = None
            self.exist = False
            self.products = None
            self.doc_total = None
            self.users_data = None
            self.sncode = None

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
    
    def count_use_cupon(self):
        from infrastructure.repositories.couponrepository import CouponRepository
        print(f"user: {self.sncode}")
        uses = CouponRepository.count_coupon_uses(self.coupon.cupon_code, self.sncode)
        print("Número de usos del cupón:", uses)
        return uses

    def validate_sales_after_coupon(self):
        from adapters.sl_client import APIClient
        sl_conect = APIClient()
        sales_count = sl_conect.get_sales_or_orders(self.sncode)
        if sales_count > 0:
            return True
        return False

    def coupon_error(self):
        
        error = []

        if not self.exist:
            error.append("El Cupon no existe")
            return ''.join(error)

        if self.coupon.one_use_only:
            if self.count_use_cupon() >= self.coupon.max_uses:
                error.append(f"El Cliente {self.sncode} ha alcanzado el limite de usos de este Cupon \n")

        else:
            if self.count_use_cupon() >= self.coupon.max_uses:
                error.append(f"El Cupon {self.coupon.cupon_code} ha alcanzado su limite de usos \n")

        if not self.coupon_vality_date():
            error.append(f"El Cupon {self.coupon.cupon_code} ha caducado \n")

        if not self.coupon_is_active():
            error.append(f"El Cupon {self.coupon.cupon_code} no esta activo \n")

        rules = self.rules_coupon()
        if rules and rules[0]['min_value']:
            if float(self.doc_total) < float(rules[0]['min_value']):
                min_value = int(rules[0]['min_value'])
                error.append(f"El valor de la factura debe ser mayor a $ {min_value:,}".replace(',', '.'))
        
        if self.validate_sales_after_coupon():
            error.append(f"El Cliente {self.sncode} ya tiene ventas posteriores a la aplicacion del Cupon \n")

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

        validator = CouponValidator(applicable_codes, rules, self.doc_total, self.coupon, users_data=self.users_data)
        filtered_products = validator.get_applicable_products()
        products_with_discounts = validator.get_discounted_products(filtered_products, discount)

        print("Productos con descuentos aplicados:", products_with_discounts)

        return {"success": True, 
                "products": products_with_discounts,
                "rules": rules[0] if rules else None,
                }