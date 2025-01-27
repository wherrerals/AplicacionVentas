from django.db import models
from datosLsApp.models.regiondb import RegionDB

class ComunaDB(models.Model):
    class Meta:
        db_table = "Comuna"

        verbose_name = 'Comuna'
        verbose_name_plural = 'Comuna'

    codigo = models.CharField(primary_key= True,max_length=50,null = False)
    codgio_postal = models.CharField(max_length=50, default='0')
    nombre = models.CharField(max_length=50,null = False)
    region = models.ForeignKey(RegionDB, on_delete=models.CASCADE, default=1)
    #El parametro to_field='atributo_En_otro_modelo' es solo necesario si la relacion es con algo que no sea la llave primaria

    def __str__(self):
        return f'{self.nombre}'