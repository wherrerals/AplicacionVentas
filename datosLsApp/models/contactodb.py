from django.db import models
from datosLsApp.models.socionegociodb import SocioNegocioDB

class ContactoDB(models.Model):
    class Meta:
        db_table = "Contacto"
        
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contacto'

    codigoInternoSap = models.IntegerField(default=0, null=True, blank=True)
    nombreCompleto = models.CharField(max_length=255, null=True, blank=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    SocioNegocio = models.ForeignKey(SocioNegocioDB, on_delete=models.CASCADE, default=1, null=True)

    def __str__(self):
        return f"{self.nombreCompleto}"