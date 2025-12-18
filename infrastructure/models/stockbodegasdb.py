from django.db import models
from infrastructure.models.bodegadb import BodegaDB
from infrastructure.models.productodb import ProductoDB

class StockBodegasDB(models.Model):
    idProducto = models.ForeignKey(ProductoDB, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(BodegaDB, on_delete=models.CASCADE)
    stock_disponible = models.IntegerField(default=-1) # stock disponible Real anteriormente stock, instock - commited
    stock_fisico = models.IntegerField(default=-1) #antes stockDisponibleReal
    stock_disponible_real = models.IntegerField(default=-1) # stock procesado por studio Go
    stock_comprometido = models.IntegerField(default=0) # stock comprometido para ventas

    class Meta:
        db_table = "StockBodegas"
        verbose_name = 'Stock Bodegas'
        verbose_name_plural = 'Stock Bodegas'
        constraints = [
            models.UniqueConstraint(fields=['idProducto', 'idBodega'], name='unique_producto_bodega')
        ]

    def __str__(self):
        return f"{self.idProducto} - {self.idBodega}"
