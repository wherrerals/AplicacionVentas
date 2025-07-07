from django.db import models
class CollectionsDB(models.Model):
    
    class Meta:
        db_table = "Collections"
        verbose_name = 'Collections'
        verbose_name_plural = 'Collections'
    
    colletion_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    rules_coupons = models.ManyToManyField('RulesCouponDB', related_name='collections', blank=True)
    products = models.ManyToManyField('ProductDB', related_name='ProductsCollections', blank=True)


class ProductsCollectionsDB(models.Model):
    
    class Meta:
        db_table = "ProductsCollections"
        verbose_name = 'ProductsCollections'
        verbose_name_plural = 'ProductsCollections'
    
    product_collection_id = models.AutoField(primary_key=True)
    collection = models.ForeignKey(CollectionsDB, on_delete=models.CASCADE, related_name='product_collections')
    product = models.ForeignKey('ProductDB', on_delete=models.CASCADE, related_name='product_collections')
    
    def __str__(self):
        return f"{self.collection.name} - {self.product.name}"