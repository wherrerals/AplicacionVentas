from django.db import models

class Producto(models.Model):
    class Meta:
        db_table = "Producto"
        verbose_name = 'Producto'
        verbose_name_plural = 'Producto'

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255,null = False)
    imagen = models.CharField(max_length=255)
    stockTotal = models.IntegerField(default=0,null = False)
    precioLista = models.FloatField(null = False)
    precioVenta = models.FloatField(null = False)
    dsctoMaxTienda = models.FloatField()
    dctoMaxProyectos = models.FloatField()
    linkProducto = models.CharField(max_length=255,null = False)