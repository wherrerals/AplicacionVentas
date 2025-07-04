from django import models

class RulesCouponDB(models.Model):
    class Meta:
        db_table = "RulesCoupon"
        verbose_name = 'RulesCoupon'
        verbose_name_plural = 'RulesCoupons'

    rule_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    operator = models.CharField(max_length=10, null=False)  # e.g., '+', '==', '<>', etc.
    coupons = models.ManyToManyField('CouponsDB', related_name='RulesCoupons', blank=True)


    def __str__(self):
        return f"{self.name} - {self.operator} - {', '.join([coupon.cupon_code for coupon in self.coupons.all()]) if self.coupons.exists() else 'No Coupons'}"


class rulesCouponsDB(models.Model):
    class Meta:
        db_table = "RulesCoupons"
        verbose_name = 'RulesCoupons'
        verbose_name_plural = 'RulesCoupons'

    rules_coupons_id = models.AutoField(primary_key=True)
    rules_coupon = models.ForeignKey(RulesCouponDB, on_delete=models.CASCADE, related_name='rules_coupons')
    coupon = models.ForeignKey('CouponsDB', on_delete=models.CASCADE, related_name='rules_coupons')

    def __str__(self):
        return f"{self.rules_coupon.name} - {self.coupon.cupon_code}"