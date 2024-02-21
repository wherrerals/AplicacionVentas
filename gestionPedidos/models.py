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

""" class Pais(models.Model): se comenta, pues se considera el pais no es necesario mantenerlo como entidad
    class Meta:
        db_table = 'Pais'
        verbose_name = 'Pais'
        verbose_name_plural = 'Pais'

    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False) """

class Region(models.Model):
    class Meta:
        db_table = "Region"

        verbose_name = 'Region'
        verbose_name_plural = 'Region'

    numero = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50,null = False)
    #pais = models.ForeignKey(Pais, on_delete=models.CASCADE, default=1) Al eliminar pais, esto queda comentado 

class Comuna(models.Model):
    class Meta:
        db_table = "Comuna"

        verbose_name = 'Comuna'
        verbose_name_plural = 'Comuna'
        
    codigo = models.CharField(max_length=50,null = False)
    nombre = models.CharField(max_length=50,null = False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,to_field='numero', default=1)#Se elimina campo default = 1, no se considera necesario
    

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

        verbose_name = 'TipoTelefono'
        verbose_name_plural = 'TipoTelefono'

    tipo = models.CharField(max_length=50,null = False)

class GrupoSN(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50,null = False)
    

class TipoSN(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=100,null = False) 
    descripcion = models.CharField(max_length=100,null = False)

class TipoCliente(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=50,null = False)

class SocioNegocio(models.Model):
    class Meta:
        db_table = "SocioNegocio"

        verbose_name = 'Socios Negocio'
        verbose_name_plural = 'Socios Negocio'

    codigoSN = models.CharField(primary_key=True, max_length=255)
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


""" class Direccion(models.Model):
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
    tipoDireccion = models.ManyToManyField(TipoDireccion, related_name='directorios') """

class Direccion(models.Model):
    class Meta:
        db_table = "Direccion"

        verbose_name = 'Direccion'
        verbose_name_plural = 'Direccion'

    rowNum = models.IntegerField()
    nombreDireccion = models.CharField(max_length=50,null = False)
    comuna = models.ForeignKey(Comuna,on_delete=models.CASCADE, default=1)
    region = models.ForeignKey(Region,on_delete=models.CASCADE, default=1)
    pais = models.CharField(max_length=10, default ='Chile')
    calleNumero = models.CharField(max_length=50)
    codigoImpuesto = models.CharField(max_length=100, default='iva')
    tipoDireccion = models.ManyToManyField(TipoDireccion, related_name='directorios')
    SocioNegocio = models.ForeignKey(SocioNegocio,on_delete=models.CASCADE, default=1) 
    

class TipoTelefono():
    codigo = models.IntegerField()
    tipo = models.CharField(max_length=50,null = False)



class Contacto(models.Model):
    class Meta:
        db_table = "Contacto"
        
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contacto'

    codigoInternoSap = models.IntegerField()
    nombreCompleto = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255,null = False)
    apellido = models.CharField(max_length=255,null = False)
    telefono = models.CharField(max_length=10)
    celular = models.CharField(max_length=10,null = False)
    email = models.EmailField(null = False)
    #tipotelefono = models.ForeignKey(TipoTelefono, on_delete=models.CASCADE, default=1)
    tipoDireccion = models.ManyToManyField(SocioNegocio, related_name='SociosNegocio')
    SocioNegocio = models.ManyToManyField('SocioNegocio', blank=True)
 


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
    nombre = models.CharField(max_length=255,null = False)
    imagen = models.CharField(max_length=255)
    stockTotal = models.IntegerField(default=0,null = False)
    precioLista = models.FloatField(null = False)
    precioVenta = models.FloatField(null = False)
    dsctoMaxTienda = models.FloatField()
    dctoMaxProyectos = models.FloatField()
    linkProducto = models.CharField(max_length=255,null = False)


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

