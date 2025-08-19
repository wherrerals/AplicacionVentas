from django.db import models


class CollectionsProducts(models.Model):
    collection = models.ForeignKey('CollectionDB', on_delete=models.CASCADE, related_name='collection_items')
    product = models.ForeignKey('ProductoDB', on_delete=models.CASCADE, related_name='product_items')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collections_products"
        unique_together = ('collection', 'product')

    def __str__(self):
        return f"{self.product} en {self.collection}"
