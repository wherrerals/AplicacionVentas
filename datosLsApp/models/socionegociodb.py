from django.db import models
from datosLsApp.models.tipoclientedb import TipoClienteDB
from datosLsApp.models.tiposndb import TipoSNDB
from datosLsApp.models.gruposndb import GrupoSNDB

class SocioNegocioDB(models.Model):
    class Meta:
        db_table = "SocioNegocio"

        verbose_name = 'Socios Negocio'
        verbose_name_plural = 'Socios Negocio'

    codigoSN = models.CharField(primary_key=True, max_length=255) #Es un identiicador unico que lo diferencia de todas las otras entradas
    nombre = models.CharField(max_length=150,)
    apellido = models.CharField(max_length=150)
    razonSocial = models.CharField(max_length=255)
    rut = models.CharField(max_length=255,null = False)
    email = models.EmailField()
    telefono = models.CharField(max_length=18)
    giro = models.CharField(max_length=100)
    condicionPago = models.IntegerField(default=-1)
    plazoReclamaciones = models.CharField(max_length=255, default="STANDAR")
    clienteExportacion = models.CharField(max_length=255, default="N")
    vendedor = models.IntegerField(default=-1)
    grupoSN = models.ForeignKey(GrupoSNDB, on_delete=models.CASCADE, default=1)
    tipoSN = models.ForeignKey(TipoSNDB,on_delete=models.CASCADE, default=1)
    tipoCliente = models.ForeignKey(TipoClienteDB,on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"{self.rut}"
        