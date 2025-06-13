from django.db import models
from datosLsApp.models.lineadb import LineaDB
from datosLsApp.models.socionegociodb import SocioNegocioDB
from datosLsApp.models.vendedordb import VendedorDB
from datosLsApp.models.condicionpagodb import CondicionPagoDB
from datosLsApp.models.tipodoctributariodb import TipoDocTributarioDB
from datosLsApp.models.tipoentregadb import TipoEntregaDB
from datosLsApp.models.tipoobjetosapdb import TipoObjetoSapDB
from datosLsApp.models.tipoventadb import TipoVentaDB

class DocumentoDB(models.Model):
    class Meta:
        db_table = 'Documento'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documento' 

    docEntry = models.IntegerField(null = True)
    docNum = models.IntegerField(null = True)
    folio = models.IntegerField(null = True)
    fechaDocumento = models.DateField(null = False)
    fechaEntrega = models.DateField(null = True)
    direccionEntrega = models.CharField(max_length=255, null = True)
    direccionDespacho = models.CharField(max_length=255, null = True)
    horarioEntrega = models.DateTimeField(null = False)
    referencia = models.CharField(max_length=255)
    comentario = models.CharField(max_length=255)
    totalAntesDelDescuento = models.FloatField()
    descuento = models.FloatField(default=0) 
    totalDocumento = models.FloatField(null = False)
    codigoVenta = models.IntegerField(null = False)
    estado_documento = models.CharField(max_length=50, null = False, default='Borrador')
    # Relaciones con otros modelos
    tipo_documento = models.ForeignKey(TipoDocTributarioDB, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(VendedorDB, on_delete=models.CASCADE, default=1)
    condi_pago = models.ForeignKey(CondicionPagoDB, on_delete=models.CASCADE, default=1)
    tipoentrega = models.ForeignKey(TipoEntregaDB, on_delete=models.CASCADE, default=1)
    tipoobjetoSap = models.ForeignKey(TipoObjetoSapDB, on_delete=models.CASCADE, default=1)    
    tipoVenta = models.ForeignKey(TipoVentaDB, on_delete=models.CASCADE, default=1)
    socio_negocio = models.ForeignKey(SocioNegocioDB, on_delete=models.CASCADE, default=1)


    
    def __str__(self):
        return f'Documento {self.docNum} - Tipo: {self.tipo_documento.nombre} - Vendedor: {self.vendedor.nombre}'