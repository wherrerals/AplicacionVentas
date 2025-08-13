from django.db import models

class SucursalDB(models.Model):
    class Meta:
        db_table = 'Sucursal'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursal' 

    codigo = models.CharField(primary_key=True,max_length=50)
    nombre = models.CharField(max_length=50,null = False)
    ubicacion = models.CharField(max_length=100,null = False, default="NO DATA")
    def __str__(self):
        return f'{self.nombre}'
    