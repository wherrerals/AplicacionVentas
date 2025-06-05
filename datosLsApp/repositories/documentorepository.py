from datosLsApp.models import DocumentoDB
from datosLsApp.models.condicionpagodb import CondicionPagoDB
from datosLsApp.models.lineadb import LineaDB
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
        tipo_venta = TipoVentaDB.objects.get(codigo=data['U_LED_TIPVTA'])
        tipo_entrega = TipoEntregaDB.objects.get(codigo=data['U_LED_FORENV'])
        condicion_pago = CondicionPagoDB.objects.get(codigo=data['PaymentGroupCode']) if data['PaymentGroupCode'] != -1 else None
        tipo_objeto = TipoObjetoSapDB.objects.get(codigo="17")


        document = DocumentoDB.objects.create(
            fechaDocumento = data['DocDate'],
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
            tipoobjetoSap= tipo_objeto,
            tipoVenta=  tipo_venta,
            socio_negocio=business_partner,
        )

    # Crear líneas
        for linea in data['DocumentLines']:
            nueva_linea = LineaDB.objects.create(
                item_code=linea['ItemCode'],
                cantidad=linea['Quantity'],
                precio_unitario=linea['UnitPrice'],
                fecha_despacho=linea['ShipDate'],
                bodega=linea['WarehouseCode'],
                metodo_envio=linea['ShippingMethod'],
                comentario=linea['FreeText'],
                descuento=linea['DiscountPercent'],
                centro_costo=linea['CostingCode'],
                centro_costo_2=linea['CostingCode2']
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