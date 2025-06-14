from datosLsApp.models import DocumentoDB
from datosLsApp.models.condicionpagodb import CondicionPagoDB
from datosLsApp.models.lineadb import LineaDB
from datosLsApp.models.productodb import ProductoDB
from datosLsApp.models.socionegociodb import SocioNegocioDB
from datosLsApp.models.tipodoctributariodb import TipoDocTributarioDB
from datosLsApp.models.tipoentregadb import TipoEntregaDB
from datosLsApp.models.tipoobjetosapdb import TipoObjetoSapDB
from datosLsApp.models.tipoventadb import TipoVentaDB
from datosLsApp.models.vendedordb import VendedorDB
from datetime import datetime


class DocumentoRepository:
    
    """
    Repositorio de Documentos

    Metodos disponibles:

    - obtenerPorId(id)
    - crearDocumento(**kwargs)
    - buscarDocumentosPorNombre(nombre)
    - obtenerPorCodigoDocumento(codigoDocumento)

    """
    
    @staticmethod
    def obtenerPorId(id):
        """
        Obtiene un documento por su id
        
        params:
            id: int

            - Id del documento a buscar
        
        return:
            DocumentoDB | None
        """
        try:
            return DocumentoDB.objects.get(id=id)
        except DocumentoDB.DoesNotExist:
            return None

    @staticmethod
    def create_document_db(data):

        business_partner = SocioNegocioDB.objects.get(codigoSN=data['CardCode'])
        document_type = TipoDocTributarioDB.objects.get(codigo=data['U_LED_TIPDOC'])
        seller = VendedorDB.objects.get(codigo=data['SalesPersonCode'])
        tipo_venta = TipoVentaDB.objects.get(codigo='PROY') #TipoVentaDB.objects.get(codigo=data['U_LED_TIPVTA'])
        tipo_entrega = TipoEntregaDB.objects.get(codigo='1')#(codigo=data['U_LED_FORENV'])
        condicion_pago = CondicionPagoDB.objects.get(codigo=data['PaymentGroupCode'])
        tipo_objeto = TipoObjetoSapDB.objects.get(codigo="1")


        document = DocumentoDB.objects.create(
            docEntry = 0,
            docNum = 0,
            folio = 0,
            fechaDocumento = data['DocDate'],
            fechaEntrega = data['DocDate'],
            direccionEntrega = data['TaxExtension']['StreetS'],
            direccionDespacho = data['TaxExtension']['StreetB'],
            horarioEntrega = datetime.now(),
            referencia=data.get('NumAtCard', ''),
            comentario=data.get('Comments', ''),
            totalAntesDelDescuento=data['DocTotal'],
            descuento=0,
            totalDocumento=data['DocTotal'],
            codigoVenta=data['SalesPersonCode'],
            tipo_documento= document_type, 
            vendedor= seller,
            condi_pago= condicion_pago,
            tipoentrega= tipo_entrega,
            tipoobjetoSap= tipo_objeto, # 
            tipoVenta=  tipo_venta, #
            socio_negocio=business_partner,
        )

    # Crear líneas
        linea_num = 0
        for linea in data['DocumentLines']:

            item_code = ProductoDB.objects.get(codigo=linea['ItemCode'])

            nueva_linea = LineaDB.objects.create(
                producto= item_code,
                numLinea = linea_num + 1,
                descuento=linea['DiscountPercent'],
                cantidad=linea['Quantity'],
                totalBrutoLinea = item_code.precioVenta * linea['Quantity'],
                totalNetoLinea= (item_code.precioVenta * linea['Quantity']) - (item_code.precioVenta * linea['Quantity'] * linea['DiscountPercent'] / 100),
                comentario=linea['FreeText'],
                fechaEntrega=linea['ShipDate'],
                docEntryBase=0,
                numLineaBase=0,
                direccionEntrega=data['TaxExtension']['StreetS'],
                tipoentrega = tipo_entrega,
                tipoobjetoSap = tipo_objeto,
            )
            
            document.document_lineas.add(nueva_linea)

        return document













            







    
    @staticmethod
    def buscarDocumentosPorNombre(nombre):
        """
        Busca documentos por su nombre
        
        params:
            nombre: str

            - Nombre del documento a buscar
        
        return:
            QuerySet
        """
        return DocumentoDB.objects.filter(nombre__icontains=nombre)
    
    @staticmethod
    def obtenerPorCodigoDocumento(codigoDocumento):
        """
        Obtiene un documento por su codigoDocumento
        
        params:
            codigoDocumento: str

            - Codigo del documento a buscar
        
        return:
            DocumentoDB | None
        """
        try:
            return DocumentoDB.objects.get(codigoDocumento=codigoDocumento)
        except DocumentoDB.DoesNotExist:
            return None