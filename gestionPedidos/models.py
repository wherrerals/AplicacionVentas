from django.db import models
from django.contrib.auth.models import User
import bcrypt

# Create your models here.
class Usuario(models.Model):
    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuario'

    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    usuarios = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f'{self.nombre}'

class Pais(models.Model):
    class Meta:
        db_table = 'Pais'
        verbose_name = 'Pais'
        verbose_name_plural = 'Pais'

    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)

class Region(models.Model):
    class Meta:
        db_table = "Region"

        verbose_name = 'Region'
        verbose_name_plural = 'Region'

    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, default=1)

class Comuna(models.Model):
    class Meta:
        db_table = "Comuna"

        verbose_name = 'Comuna'
        verbose_name_plural = 'Comuna'
        
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)

class TipoDireccion(models.Model):
    class Meta:
        db_table = "TipoDireccion"

        verbose_name = 'TipoDireccion'
        verbose_name_plural = 'TipoDireccion'
                
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)

class TipoTelefono(models.Model):
    class Meta:
        db_table = "TipoTelefono"

        verbose_name = 'TipoDireccion'
        verbose_name_plural = 'TipoDireccion'

    tipo = models.CharField(max_length=50)


class SocioNegocio(models.Model):
    class Meta:
        pass
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    razonSocial = models.CharField(max_length=255)
    codigoSN = models.CharField(max_length=255)
    rut = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=10)
    giro = models.CharField(max_length=50)
    alias = models.CharField(max_length=55)
    condicionPago = models.IntegerField(default=-1)
    plazoReclamaciones = models.CharField(max_length=255, default="STANDAR")
    clienteExportacion = models.CharField(max_length=255, default="N")
    vendedor = models.IntegerField(default=-1)
    tipotelefono = models.ForeignKey(TipoTelefono, on_delete=models.CASCADE, default=1)


class Direccion(models.Model):
    class Meta:
        db_table = "Direccion"

        verbose_name = 'Direccion'
        verbose_name_plural = 'Direccion'

    rowNum = models.IntegerField()
    nombreDireccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)
    calleNumero = models.CharField(max_length=50)
    codigoImpuesto = models.CharField(max_length=100, default='iva')
    tipoDireccion = models.ManyToManyField(TipoDireccion, related_name='directorios')

class TipoTelefono():
    codigo = models.IntegerField()
    tipo = models.CharField(max_length=50)



class Contacto(models.Model):
    class Meta:
        db_table = "Contacto"
        
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direccion'

    codigoInternoSap = models.IntegerField()
    nombreCompleto = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.CharField(max_length=10)
    celular = models.CharField(max_length=10)
    email = models.EmailField()
    #tipotelefono = models.ForeignKey(TipoTelefono, on_delete=models.CASCADE, default=1)
    tipoDireccion = models.ManyToManyField(SocioNegocio, related_name='SociosNegocio')
 
class GrupoSN(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, default=1)

class TipoSN(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=100) 
    descripcion = models.CharField(max_length=100)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, default=1)

class TipoCliente(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, default=1)

class TipoDocTributario(models.Model):
    class Meta:
        db_table = 'TipoDocTributario'

        verbose_name = 'TipoDocTributario'
        verbose_name_plural = 'TipoDocTributario'
    
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.nombre}'
    
class TipoVenta(models.Model):
    class Meta:
        db_table = 'TipoVenta'

    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.nombre}'
    
class Sucursal(models.Model):
    class Meta:
        db_table = 'Sucursal' 

    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.nombre}'
    
class Vendedor(models.Model):
    class Meta:
        db_table = 'Vendedor' 

    codigo = models.IntegerField()
    nombre = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return f'{self.nombre}'
    
class CondicionPago(models.Model):        
    class Meta:
        db_table = 'CondicionPago' 

    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)

class Producto(models.Model):
    class Meta:
        db_table = 'Producto'   

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    imagen = models.CharField(max_length=50)
    stockTotal = models.IntegerField()
    precioLista = models.FloatField()
    precioVenta = models.FloatField()
    dsctoMaxTienda = models.FloatField()
    dctoMaxProyectos = models.FloatField()
    linkProducto = models.CharField(max_length=255)

class Bodega(models.Model):
    class Meta:
        db_table = 'bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodega'
         
    codigo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f'Producto {self.codigo}/ Numero Linea: {self.nombre}/ Descuento: {self.descripcion}'
    

class Inventario(models.Model):
    class Meta:
        db_table = 'Inventario'

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=1)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, default=1) 

class TipoEntrega(models.Model):
    class Meta:
        db_table = 'TipoEntrega'

    codigo = models.IntegerField()
    tipo = models.CharField(max_length=255)

class TipoObjetoSap(models.Model):
    class Meta:
        db_table = 'TipoObjetoSap'
    
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)


class Documento(models.Model):
    class Meta:
        db_table = 'Documento'

    docEntry = models.IntegerField()
    docNum = models.IntegerField()
    folio = models.IntegerField()
    fechaDocumento = models.DateField()
    fechaEntrega = models.DateField()
    horarioEntrega = models.DateTimeField()
    referencia = models.CharField(max_length=255)
    comentario = models.CharField(max_length=255)  # Corregí el nombre del campo aquí
    totalAntesDelDescuento = models.FloatField()
    descuento = models.FloatField(default=0)
    totalDocumento = models.FloatField()
    codigoVenta = models.IntegerField()
    tipo_documento = models.ForeignKey(TipoDocTributario, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, default=1)
    condi_pago = models.ForeignKey(CondicionPago, on_delete=models.CASCADE, default=1)
    tipoentrega = models.ForeignKey(TipoEntrega, on_delete=models.CASCADE, default=1)
    tipoobjetoSap = models.ForeignKey(TipoObjetoSap, on_delete=models.CASCADE, default=1)    
    # Otros campos que puedas tener
    
    def __str__(self):
        return f'Documento {self.docNum} - Tipo: {self.tipo_documento.nombre} - Vendedor: {self.nombre_vendedor.nombre}'
    

class Item(models.Model):
    class Meta:
        db_table = 'item'
        verbose_name = 'Item'
        verbose_name_plural = 'Item'


    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación uno a uno con Producto
    numLinea = models.IntegerField()
    descuento = models.FloatField(default=0)
    cantidad = models.IntegerField()
    totalNetoLinea = models.FloatField()
    totalBrutoLinea = models.FloatField()
    comentario = models.CharField(max_length=255)
    tipoObjetoDocBase = models.CharField(max_length=255)
    docEntryBase = models.IntegerField()
    numLineaBase = models.IntegerField()
    fechaEntrega = models.DateField()
    direccionEntrega = models.CharField(max_length=255)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, default=1)
    tipoentrega = models.ForeignKey(TipoEntrega, on_delete=models.CASCADE, default=1)
    tipoobjetoSap = models.ForeignKey(TipoObjetoSap, on_delete=models.CASCADE, default=1)    

    def __str__(self):
        return f'Producto {self.producto}/ Numero Linea: {self.numLinea}/ Descuento: {self.descuento}'

