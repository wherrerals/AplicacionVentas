from django.db import models


class CouponUsageDB(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['coupon', 'user'], name='unique_coupon_user')
        ]
        
        db_table = "CouponUsage"
        verbose_name = 'CouponUsage'
        verbose_name_plural = 'CouponUsage'

    coupon = models.ForeignKey('CouponsDB', on_delete=models.CASCADE)
    user = models.ForeignKey('SocioNegocioDB', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    remaining_uses = models.IntegerField(default=0)



    def __str__(self):
        return f"{self.user.codigoSN} - {self.coupon.cupon_code}"
