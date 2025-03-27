from django.db import models

class ProductoDB(models.Model):
    class Meta:
        db_table = "Producto"
        verbose_name = 'Producto'
        verbose_name_plural = 'Producto'

    codigo = models.CharField(primary_key=True, max_length=50, unique=True)
    nombre = models.CharField(max_length=255,null = False)
    imagen = models.CharField(max_length=255, default="https://ledstudiocl.vtexassets.com/assets/vtex.file-manager-graphql/images/14ecba9f-2814-4029-9e0e-e5e6b9e2869c___b2a5497dbc81c0adc5576c48b2eeb27b.jpg")
    stockTotal = models.IntegerField(default=0,null = False)
    precioLista = models.FloatField(null = False)
    precioVenta = models.FloatField(null = False)
    dsctoMaxTienda = models.FloatField()
    dctoMaxProyectos = models.FloatField()
    linkProducto = models.CharField(max_length=255, null=False)
    marca = models.CharField(max_length=20, default="Sin Marca", null=True) 
    costo = models.FloatField(default=0,null=False)
    descontinuado = models.BooleanField(default=False, db_default='0')
    inactivo = models.BooleanField(default=False, db_default='tNO')

    def __str__(self):
        return self.codigo