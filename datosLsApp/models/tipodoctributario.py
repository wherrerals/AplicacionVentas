from django.db import models

class TipoDocTributario(models.Model):
    class Meta:
        db_table = 'TipoDocTributario'

        verbose_name = 'TipoDocTributario'
        verbose_name_plural = 'TipoDocTributario'
    
    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=100,null = False)
    def __str__(self):
        return f'{self.nombre}'