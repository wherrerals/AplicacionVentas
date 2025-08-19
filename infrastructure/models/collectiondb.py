from django.db import models

class CollectionDB(models.Model):

    collection_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    
    products = models.ManyToManyField(
        'ProductoDB',
        through='CollectionsProducts',
        related_name='collectionsproducts',
        blank=True
    )

    class Meta:
        db_table = "Collections"
        verbose_name = "Collection"
