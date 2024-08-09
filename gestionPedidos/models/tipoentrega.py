from django.db import models

class TipoEntrega(models.Model):
    class Meta:
        db_table = "TipoEntrega"
        verbose_name = 'TipoEntrega'
        verbose_name_plural = 'TipoEntrega'
    codigo = models.IntegerField(primary_key=True)#Es un identiicador unico que lo diferencia de todas las otras entradas
    nombre = models.CharField(max_length=255,null = False)
    descripcion = models.CharField(max_length=255,null = False)
