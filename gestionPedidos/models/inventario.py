from django.db import models
from .producto import Producto
from .bodega import Bodega

class Inventario(models.Model):
    class Meta:
        db_table = "Inventario"
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventario'

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=1)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, default=1) 
