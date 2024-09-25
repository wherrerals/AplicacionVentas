from django.db import models
from datosLsApp.models.productodb import ProductoDB
from datosLsApp.models.bodegadb import BodegaDB

class InventarioDB(models.Model):
    class Meta:
        db_table = "Inventario"
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventario'

    producto = models.ForeignKey(ProductoDB, on_delete=models.CASCADE, default=1)
    bodega = models.ForeignKey(BodegaDB, on_delete=models.CASCADE, default=1) 
