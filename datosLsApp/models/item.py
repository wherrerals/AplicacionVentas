from django.db import models
from datosLsApp.models.tipoobjetosap import TipoObjetoSap
from datosLsApp.models.documento import Documento
from datosLsApp.models.tipoentrega import TipoEntrega
from datosLsApp.models.producto import Producto

class Item(models.Model):
    class Meta:
        db_table = 'item'
        verbose_name = 'Item'
        verbose_name_plural = 'Item'


    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación uno a uno con Producto
    numLinea = models.IntegerField()
    descuento = models.FloatField(default=0)
    cantidad = models.IntegerField(default=0)
    totalNetoLinea = models.FloatField(null = False)
    totalBrutoLinea = models.FloatField(null = False)
    comentario = models.CharField(max_length=255)
    tipoObjetoDocBase = models.CharField(max_length=255)
    docEntryBase = models.IntegerField(null = False)
    numLineaBase = models.IntegerField(null = False)
    fechaEntrega = models.DateField(null = False)
    direccionEntrega = models.CharField(max_length=255)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, default=1)
    tipoentrega = models.ForeignKey(TipoEntrega, on_delete=models.CASCADE, default=1)
    tipoobjetoSap = models.ForeignKey(TipoObjetoSap, on_delete=models.CASCADE, default=1)    

    def __str__(self):
        return f'Producto {self.producto}/ Numero Linea: {self.numLinea}/ Descuento: {self.descuento}'