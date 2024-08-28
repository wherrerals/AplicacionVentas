from django.db import models
from datosLsApp.models.region import Region
from datosLsApp.models.comuna import Comuna
from datosLsApp.models.socionegocio import SocioNegocio

class Direccion(models.Model):
    class Meta:
        db_table = "Direccion"

        verbose_name = 'Direccion'
        verbose_name_plural = 'Direccion'

    rowNum = models.IntegerField(default='0 ') #dato SAP por socio negocio
    nombreDireccion = models.CharField(max_length=50,null = False) #identificador natural 
    ciudad = models.CharField(max_length=50, default='prueba')
    calleNumero = models.CharField(max_length=50) #corresponde a direccio en direccion
    codigoImpuesto = models.CharField(max_length=100, default='iva')
    #tipoDireccion = models.ManyToManyField(TipoDireccion, related_name='directorios')
    tipoDireccion = models.CharField(max_length=10, null = True)
    pais = models.CharField(max_length=10, default ='Chile')
    SocioNegocio = models.ForeignKey(SocioNegocio,on_delete=models.CASCADE, default=1) 
    comuna = models.ForeignKey(Comuna,on_delete=models.CASCADE, default=1)
    region = models.ForeignKey(Region,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.rowNum}"