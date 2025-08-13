from django.db import models
from django.contrib.auth.models import User

from infrastructure.models.couponsdb import CouponsDB


class CouponUsage(models.Model):
    coupon = models.ForeignKey(CouponsDB, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    remaining_uses = models.IntegerField(default=0)

    class Meta:
        unique_together = ('coupon', 'user')  # Para no repetir vinculación
        verbose_name = 'coupon_usage'
        verbose_name_plural = 'coupon_usage'

    def __str__(self):
        return f"{self.user.username} - {self.coupon.cupon_code}"
