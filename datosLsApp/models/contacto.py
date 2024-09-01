from django.db import models
from datosLsApp.models.socionegocio import SocioNegocio

class Contacto(models.Model):
    class Meta:
        db_table = "Contacto"
        
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contacto'

    codigoInternoSap = models.IntegerField()
    nombreCompleto = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255,null = False)
    apellido = models.CharField(max_length=255,null = False)
    telefono = models.CharField(max_length=10)
    celular = models.CharField(max_length=10,null = False)
    email = models.EmailField(null = False)
    SocioNegocio = models.ForeignKey(SocioNegocio,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.nombreCompleto}"