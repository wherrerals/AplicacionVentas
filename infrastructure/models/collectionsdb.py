from django.db import models

from infrastructure.models.productodb import ProductoDB
class CollectionsDB(models.Model):
    
    class Meta:
        db_table = "Collections"
        verbose_name = 'Collections'
        verbose_name_plural = 'Collections'
    
    colletion_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    rules_coupons = models.ManyToManyField('RulesCouponDB', related_name='collections', blank=True)
    products = models.ManyToManyField(ProductoDB, related_name='ProductsCollections', blank=True)

    def __str__(self):
        return self.name if self.name else f"Collection {self.colletion_id}"