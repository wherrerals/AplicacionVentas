from django.db import models
from infrastructure.models.bodegadb import BodegaDB
from infrastructure.models.productodb import ProductoDB

class StockBodegasDB(models.Model):
    idProducto = models.ForeignKey(ProductoDB, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(BodegaDB, on_delete=models.CASCADE)
    stock = models.IntegerField(default=-1)
    stockDisponibleReal = models.IntegerField(default=-1)

    class Meta:
        db_table = "StockBodegas"
        verbose_name = 'Stock Bodegas'
        verbose_name_plural = 'Stock Bodegas'
        constraints = [
            models.UniqueConstraint(fields=['idProducto', 'idBodega'], name='unique_producto_bodega')
        ]

    def __str__(self):
        return f"{self.idProducto} - {self.idBodega}"
