from django.db import models
from datosLsApp.models.socionegocio import SocioNegocio
<<<<<<< HEAD

=======
>>>>>>> e5c20535e421447a3ea3ae61c9aa9d8ff99e2e4e

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
<<<<<<< HEAD
    SocioNegocio = models.ForeignKey(SocioNegocio,on_delete=models.CASCADE, default=1) 
    #tipotelefono = models.ForeignKey(TipoTelefono, on_delete=models.CASCADE, default=1)
    #tipoDireccion = models.ManyToManyField(SocioNegocio, related_name='SociosNegocio')
    #SocioNegocio = models.ManyToManyField('SocioNegocio', blank=True)
=======
    SocioNegocio = models.ForeignKey(SocioNegocio,on_delete=models.CASCADE, default=1)
>>>>>>> e5c20535e421447a3ea3ae61c9aa9d8ff99e2e4e

    def __str__(self):
        return f"{self.nombreCompleto}"