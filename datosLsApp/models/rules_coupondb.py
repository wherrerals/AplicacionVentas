from django.db import models

class RulesCouponDB(models.Model):
    class Meta:
        db_table = "RulesCoupon"
        verbose_name = 'RulesCoupon'
        verbose_name_plural = 'RulesCoupons'

    rule_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    operator = models.CharField(max_length=10, null=False)  # e.g., '+', '==', '<>', etc.


    def __str__(self):
        return f"{self.name}"