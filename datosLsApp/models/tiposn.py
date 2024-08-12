from django.db import models

class TipoSN(models.Model):
    class Meta:
        db_table = "TipoSN"
        verbose_name = 'TipoSN'
        verbose_name_plural = 'TipoSN'

    codigo = models.CharField(primary_key=True,max_length=1)#Es un identiicador unico que lo diferencia de todas las otras entradas
    nombre = models.CharField(max_length=100,null = False) 
    descripcion = models.CharField(max_length=100,null = False)