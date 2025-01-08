from django.db import models
from datosLsApp.models.socionegociodb import SocioNegocioDB

class ContactoDB(models.Model):
    class Meta:
        db_table = "Contacto"
        
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contacto'

    codigoInternoSap = models.IntegerField(default=0)
    nombreCompleto = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20,null = False)
    email = models.EmailField(null = False)
    SocioNegocio = models.ForeignKey(SocioNegocioDB, on_delete=models.CASCADE, default=1, null=True)

    def __str__(self):
        return f"{self.nombreCompleto}"