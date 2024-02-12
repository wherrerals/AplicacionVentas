from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Usuario(models.Model):
    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuario'

    #user = models.OneToOneField(User,on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    usuarios = models.OneToOneField(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.nombre}'

class Pais(models.Model):
    class Meta:
        db_table = 'Pais'
        verbose_name = 'Pais'
        verbose_name_plural = 'Pais'

    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)

class Region(models.Model):
    class Meta:
        db_table = "Region"

        verbose_name = 'Region'
        verbose_name_plural = 'Region'

    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, default=1)

class Comuna(models.Model):
    class Meta:
        db_table = "Comuna"

        verbose_name = 'Comuna'
        verbose_name_plural = 'Comuna'
        
    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)

class TipoDireccion(models.Model):
    class Meta:
        db_table = "TipoDireccion"

        verbose_name = 'TipoDireccion'
        verbose_name_plural = 'TipoDireccion'
                
    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)

class TipoTelefono(models.Model):
    class Meta:
        db_table = "TipoTelefono"

        verbose_name = 'TipoDireccion'
        verbose_name_plural = 'TipoDireccion'

    tipo = models.CharField(max_length=50,null = False)


class SocioNegocio(models.Model):
    class Meta:
        pass
    nombre = models.CharField(max_length=50,null = False)
    apellido = models.CharField(max_length=50,null = False)
    razonSocial = models.CharField(max_length=255,null = False)
    codigoSN = models.CharField(max_length=255,null = False)
    rut = models.CharField(max_length=255,null = False)
    email = models.EmailField()
    telefono = models.CharField(max_length=10)
    giro = models.CharField(max_length=50,null = False)
    alias = models.CharField(max_length=55,null = False)
    condicionPago = models.IntegerField(default=-1,null = False)
    plazoReclamaciones = models.CharField(max_length=255, default="STANDAR",null = False)
    clienteExportacion = models.CharField(max_length=255, default="N",null = False)
    vendedor = models.IntegerField(default=-1,null = False)
    tipotelefono = models.ForeignKey(TipoTelefono, on_delete=models.CASCADE, default=1)


class Direccion(models.Model):
    class Meta:
        db_table = "Direccion"

        verbose_name = 'Direccion'
        verbose_name_plural = 'Direccion'

    rowNum = models.IntegerField()
    nombreDireccion = models.CharField(max_length=50,null = False)
    ciudad = models.CharField(max_length=50,null = False)
    comuna = models.CharField(max_length=50,null = False)
    calleNumero = models.CharField(max_length=50)
    codigoImpuesto = models.CharField(max_length=100, default='iva')
    tipoDireccion = models.ManyToManyField(TipoDireccion, related_name='directorios')

class TipoTelefono():
    codigo = models.IntegerField()
    tipo = models.CharField(max_length=50,null = False)



class Contacto(models.Model):
    class Meta:
        db_table = "Contacto"
        
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direccion'

    codigoInternoSap = models.IntegerField()
    nombreCompleto = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255,null = False)
    apellido = models.CharField(max_length=255,null = False)
    telefono = models.CharField(max_length=10)
    celular = models.CharField(max_length=10,null = False)
    email = models.EmailField(null = False)
    #tipotelefono = models.ForeignKey(TipoTelefono, on_delete=models.CASCADE, default=1)
    tipoDireccion = models.ManyToManyField(SocioNegocio, related_name='SociosNegocio')
 
class GrupoSN(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50,null = False)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, default=1)

class TipoSN(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=100,null = False) 
    descripcion = models.CharField(max_length=100,null = False)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, default=1)

class TipoCliente(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50,null = False)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, default=1)

class TipoDocTributario(models.Model):
    class Meta:
        db_table = 'TipoDocTributario'

        verbose_name = 'TipoDocTributario'
        verbose_name_plural = 'TipoDocTributario'
    
    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=100,null = False)
    def __str__(self):
        return f'{self.nombre}'
    
class TipoVenta(models.Model):
    class Meta:
        db_table = 'TipoVenta'

    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)
    def __str__(self):
        return f'{self.nombre}'
    
class Sucursal(models.Model):
    class Meta:
        db_table = 'Sucursal'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursal' 

    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)
    def __str__(self):
        return f'{self.nombre}'
    
class Vendedor(models.Model):
    class Meta:
        db_table = 'Vendedor'
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedor' 

    codigo = models.IntegerField()
    nombre = models.CharField(max_length=100,null = False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return f'{self.nombre}'
    
class CondicionPago(models.Model):        
    class Meta:
        db_table = 'CondicionPago' 

    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50,null = False)

class Producto(models.Model):
    class Meta:
        db_table = 'Producto'   

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50,null = False)
    imagen = models.CharField(max_length=50)
    stockTotal = models.IntegerField(default=0,null = False)
    precioLista = models.FloatField(null = False)
    precioVenta = models.FloatField(null = False)
    dsctoMaxTienda = models.FloatField()
    dctoMaxProyectos = models.FloatField()
    linkProducto = models.CharField(max_length=255,null = False)
    def __str__(self):
        return f'{self.nombre} {self.codigo}'

class Bodega(models.Model):
    class Meta:
        db_table = 'bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodega'
         
    codigo = models.CharField(max_length=255,null = False)
    nombre = models.CharField(max_length=50,null = False)
    descripcion = models.CharField(max_length=255,null = False)

    def __str__(self):
        return f'{self.nombre}'
    

class Inventario(models.Model):
    class Meta:
        db_table = 'Inventario'

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=1)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, default=1) 

class TipoEntrega(models.Model):
    class Meta:
        db_table = 'TipoEntrega'

    codigo = models.IntegerField(null = False)
    tipo = models.CharField(max_length=255,null = False)

class TipoObjetoSap(models.Model):
    class Meta:
        db_table = 'TipoObjetoSap'
    
    codigo = models.IntegerField(null = False)
    nombre = models.CharField(max_length=50,null = False)
    descripcion = models.CharField(max_length=255,null = False)


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

