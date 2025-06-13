from django.db import models

class TipoObjetoSapDB(models.Model):
    class Meta:
        db_table = "TipoObjetoSap"
        verbose_name = 'TipoObjetoSap'
        verbose_name_plural = 'TipoObjetoSap'
    
    codigo = models.IntegerField(null = False)
    nombre = models.CharField(max_length=50,null = False)
    descripcion = models.CharField(max_length=255,null = False)

    def __str__(self):
        return f'{self.nombre}'