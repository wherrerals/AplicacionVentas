from django.db import models

class CouponCollectionsDB(models.Model):
    class Meta:
        db_table = "CouponCollections"
        verbose_name = "CouponCollection"
        verbose_name_plural = "CouponCollections"
        unique_together = ("coupon", "collection")

    coupon = models.ForeignKey('CouponsDB', on_delete=models.CASCADE)
    collection = models.ForeignKey('CollectionDB', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.coupon.cupon_code} -> {self.collection.collection_id}"