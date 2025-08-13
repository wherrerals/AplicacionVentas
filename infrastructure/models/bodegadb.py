from django.db import models

class BodegaDB(models.Model):
    class Meta:
        db_table = 'bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodega'
         
    codigo = models.CharField(primary_key=True,max_length=255) #Es un identiicador unico que lo diferencia de todas las otras entradas
    nombre = models.CharField(max_length=50,null = False)
    descripcion = models.CharField(max_length=255,null = False)

    def __str__(self):
        return f'{self.nombre}'
    