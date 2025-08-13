from django.db import models

class CouponRuleRelation(models.Model):
    coupon = models.ForeignKey('CouponsDB', on_delete=models.CASCADE)
    rule = models.ForeignKey('RulesCouponDB', on_delete=models.CASCADE)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #condition = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('coupon', 'rule')
        db_table = "CouponRuleRelation"
        verbose_name = "Coupon Rule Relation"
        verbose_name_plural = "Coupon Rule Relations"

    def __str__(self):
        return f"{self.coupon.cupon_code} - {self.rule.name} (Max: {self.max_value})"
