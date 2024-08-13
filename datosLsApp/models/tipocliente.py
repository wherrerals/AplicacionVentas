from django.db import models

class TipoCliente(models.Model):
    class Meta:
        db_table = "TipoCliente"
        verbose_name = 'TipoCliente'
        verbose_name_plural = 'TipoCliente'
    codigo = models.CharField(primary_key=True,max_length=1)#Es un identiicador unico que lo diferencia de todas las otras entradas
    nombre = models.CharField(max_length=50,null = False)
