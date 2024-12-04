from django.db import models
from datosLsApp.models.bodegadb import BodegaDB
from datosLsApp.models.productodb import ProductoDB


class StockBodegasDB(models.Model):

    class Meta:
        db_table = "StockBodegas"

        verbose_name = 'Stock Bodegas'
        verbose_name_plural = 'Stock Bodegas'

    id = models.AutoField(primary_key=True)
    idProducto = models.ForeignKey(ProductoDB, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(BodegaDB, on_delete=models.CASCADE)
    stock = models.IntegerField(default=-1)
    stockDisponibleReal = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.idProducto}"