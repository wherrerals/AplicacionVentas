from django.db import models

class ConfiDescuentosDB(models.Model):
    class Meta:
        db_table = "Descuento"
        
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuento'

    codigo = models.CharField(primary_key= True,max_length=50,null = False)
    descripcion = models.CharField(max_length=50,null = False)
    tipoVenta = models.CharField(max_length=50,null = False)
    limiteDescuentoMaximo = models.IntegerField(null = False)
    tipoDeMarca = models.CharField(max_length=50,null = False)


    def __str__(self):
        return f"{self.descripcion}"
    