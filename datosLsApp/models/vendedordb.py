from django.db import models
from datosLsApp.models.sucursaldb import SucursalDB

class VendedorDB(models.Model):
    class Meta:
        db_table = 'Vendedor'
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedor' 

    codigo = models.IntegerField()
    nombre = models.CharField(max_length=100,null = False)
    #sucursal = models.ForeignKey(SucursalDB, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f'{self.nombre}'