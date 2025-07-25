from django.db import models
from datosLsApp.models.tipoobjetosapdb import TipoObjetoSapDB
from datosLsApp.models.tipoentregadb import TipoEntregaDB
from datosLsApp.models.productodb import ProductoDB

class LineaDB(models.Model):
    class Meta:
        db_table = 'line_doc'
        verbose_name = 'Linea_documento'
        verbose_name_plural = 'Linea_documento'


    producto = models.ForeignKey(ProductoDB, on_delete=models.CASCADE)  # Relación uno a uno con Producto
    numLinea = models.IntegerField()
    descuento = models.FloatField(default=0)
    cantidad = models.IntegerField(default=0) # cantidad solicitada
    cantidad_solicitada = models.IntegerField(default=0) #cantidad original pendiente por cambiar nombre a cantidad_original
    precioUnitario = models.FloatField(null = True, blank=True, default=None)  # Puede ser nulo si no se ha definido
    totalNetoLinea = models.FloatField(null = False)
    totalBrutoLinea = models.FloatField(null = False)
    comentario = models.CharField(max_length=255)
    tipoObjetoDocBase = models.CharField(max_length=255)
    docEntryBase = models.IntegerField(null = False)
    numLineaBase = models.IntegerField(null = False)
    fechaEntrega = models.DateField(null = False)
    direccionEntrega = models.CharField(max_length=255)
    tipoentrega = models.ForeignKey(TipoEntregaDB, on_delete=models.CASCADE, default=1)
    estado_devolucion = models.IntegerField(null = True, blank=True, default=0)  # 1 = Activo, 0 = Devolución
    tipoobjetoSap = models.ForeignKey(TipoObjetoSapDB, on_delete=models.CASCADE)
    documento = models.ForeignKey('DocumentoDB', on_delete=models.CASCADE, related_name='lineas', default=None)
    bodega = models.CharField(max_length=10, null=True, blank=True, default="None")  # Almacena el código de la sucursal
  

    def __str__(self):
        return f'Producto {self.producto}| Linea {self.numLinea} | Cantidad: {self.cantidad} | Precio Unitario: {self.precioUnitario} | Total Neto: {self.totalNetoLinea}'