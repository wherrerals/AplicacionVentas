from django.db import models

class TipoVentaDB(models.Model):
    class Meta:
        db_table = "TipoVenta"
        verbose_name = 'TipoVenta'
        verbose_name_plural = 'TipoVenta'

    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)
    
    def __str__(self):
        return f'{self.codigo}'
    