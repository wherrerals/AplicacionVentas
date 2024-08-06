from django.db import models
from .tipocliente import TipoCliente
from .tiposn import TipoSN
from .gruposn import GrupoSN

class SocioNegocio(models.Model):
    class Meta:
        db_table = "SocioNegocio"

        verbose_name = 'Socios Negocio'
        verbose_name_plural = 'Socios Negocio'

    codigoSN = models.CharField(primary_key=True, max_length=255) #Es un identiicador unico que lo diferencia de todas las otras entradas
    nombre = models.CharField(max_length=50,)
    apellido = models.CharField(max_length=50)
    razonSocial = models.CharField(max_length=255)
    rut = models.CharField(max_length=255,null = False)
    email = models.EmailField()
    telefono = models.CharField(max_length=11)
    giro = models.CharField(max_length=50)
    condicionPago = models.IntegerField(default=-1)
    plazoReclamaciones = models.CharField(max_length=255, default="STANDAR")
    clienteExportacion = models.CharField(max_length=255, default="N")
    vendedor = models.IntegerField(default=-1)
    contacto_cliente = models.ManyToManyField('Contacto', blank=True)
    grupoSN = models.ForeignKey(GrupoSN, on_delete=models.CASCADE, default=1)
    tipoSN = models.ForeignKey(TipoSN,on_delete=models.CASCADE, default=1)
    tipoCliente = models.ForeignKey(TipoCliente,on_delete=models.CASCADE, default=1)