from django.db import models

class CollectionDB(models.Model):

    collection_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, null=False)
    products = models.ManyToManyField('ProductoDB', through='CollectionsProducts', related_name='collectionsproducts', blank=True)
    coupon_does_not_apply = models.BooleanField(default=False)

    class Meta:
        db_table = "Collections"
        verbose_name = "Collection"

    def __str__(self):
        return self.name 