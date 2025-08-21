from django.db import models
from infrastructure.models.productodb import ProductoDB
from infrastructure.models.rules_coupondb import RulesCouponDB

class CouponsDB(models.Model):
    
    class Meta:
        db_table = "Coupons"
        verbose_name = 'Coupons'
        verbose_name_plural = 'Coupons'

    cupon_code = models.CharField(primary_key=True, max_length=50, null=False)
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    max_uses = models.IntegerField(default=1)
    one_use_only = models.BooleanField(default=False)
    allows_maximum_discount = models.BooleanField(default=False)
    coupon_type = models.CharField(max_length=50)
    same_price_and_discount = models.BooleanField(default=False)
    last_modification = models.DateTimeField(auto_now=True)
    collections = models.ManyToManyField('CollectionDB', through='CouponCollectionsDB', related_name='coupons_collections', blank=True)
    bp_use = models.ManyToManyField('SocioNegocioDB', through='CouponUsageDB', related_name='available_coupons', blank=True)
    rules = models.ManyToManyField(RulesCouponDB, through='CouponRuleRelation', related_name='rules_coupons', blank=True)
    products = models.ManyToManyField(ProductoDB, related_name='products_coupons', blank=True)

    def __str__(self):
        return f"{self.cupon_code} - {self.name} - {self.active} - {self.valid_from} - {self.valid_to} - {self.discount_percentage} - {self.max_uses} - {self.one_use_only} - {self.coupon_type}"