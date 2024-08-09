from django.db import models
from .vendedor import Vendedor
from .condicionpago import CondicionPago
from .tipodoctributario import TipoDocTributario
from .tipoentrega import TipoEntrega
from .tipoobjetosap import TipoObjetoSap

class Documento(models.Model):
    class Meta:
        db_table = 'Documento'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documento' 


    docEntry = models.IntegerField(null = False)
    docNum = models.IntegerField(null = False)
    folio = models.IntegerField(null = False)
    fechaDocumento = models.DateField(null = False)
    fechaEntrega = models.DateField(null = False)
    horarioEntrega = models.DateTimeField(null = False)
    referencia = models.CharField(max_length=255)
    comentario = models.CharField(max_length=255)  # Corregí el nombre del campo aquí
    totalAntesDelDescuento = models.FloatField()
    descuento = models.FloatField(default=0) 
    totalDocumento = models.FloatField(null = False)
    codigoVenta = models.IntegerField(null = False)
    tipo_documento = models.ForeignKey(TipoDocTributario, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, default=1)
    condi_pago = models.ForeignKey(CondicionPago, on_delete=models.CASCADE, default=1)
    tipoentrega = models.ForeignKey(TipoEntrega, on_delete=models.CASCADE, default=1)
    tipoobjetoSap = models.ForeignKey(TipoObjetoSap, on_delete=models.CASCADE, default=1)    
    # Otros campos que puedas tener
    
    def __str__(self):
        return f'Documento {self.docNum} - Tipo: {self.tipo_documento.nombre} - Vendedor: {self.nombre_vendedor.nombre}'