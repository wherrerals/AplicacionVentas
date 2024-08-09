from django.db import models
from .region import Region

class Comuna(models.Model):
    class Meta:
        db_table = "Comuna"

        verbose_name = 'Comuna'
        verbose_name_plural = 'Comuna'
        
    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    #El parametro to_field='atributo_En_otro_modelo' es solo necesario si la relacion es con algo que no sea la llave primaria