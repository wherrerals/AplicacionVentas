from django.db import models

class TipoObjetoSap(models.Model):
    class Meta:
        db_table = "TipoObjetoSap"
        verbose_name = 'TipoObjetoSap'
        verbose_name_plural = 'TipoObjetoSap'
    
    codigo = models.IntegerField(null = False)
    nombre = models.CharField(max_length=50,null = False)
    descripcion = models.CharField(max_length=255,null = False)