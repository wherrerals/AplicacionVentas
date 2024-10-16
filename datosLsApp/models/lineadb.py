from django.db import models
from datosLsApp.models.tipoobjetosapdb import TipoObjetoSapDB
from datosLsApp.models.documentodb import DocumentoDB
from datosLsApp.models.tipoentregadb import TipoEntregaDB
from datosLsApp.models.productodb import ProductoDB

class LineaDB(models.Model):
    class Meta:
        db_table = 'item'
        verbose_name = 'Item'
        verbose_name_plural = 'Item'


    producto = models.ForeignKey(ProductoDB, on_delete=models.CASCADE)  # Relación uno a uno con Producto
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
    documento = models.ForeignKey(DocumentoDB, on_delete=models.CASCADE, default=1)
    tipoentrega = models.ForeignKey(TipoEntregaDB, on_delete=models.CASCADE, default=1)
    tipoobjetoSap = models.ForeignKey(TipoObjetoSapDB, on_delete=models.CASCADE, default=1)    

    def __str__(self):
        return f'Producto {self.producto}/ Numero Linea: {self.numLinea}/ Descuento: {self.descuento}'