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
from django.db import connection, transaction
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
        tipo_venta = TipoVentaDB.objects.get(codigo='PROY')  # puedes cambiar esto si luego usas el dato dinámico
        tipo_entrega = TipoEntregaDB.objects.get(codigo='1')
        condicion_pago = CondicionPagoDB.objects.get(codigo=data['PaymentGroupCode'])
        tipo_objeto = TipoObjetoSapDB.objects.get(codigo="1")

        # Crear el documento
        document = DocumentoDB.objects.create(
            docEntry=0,
            docNum=0,
            folio=0,
            fechaDocumento=data['DocDate'],
            fechaEntrega=data['DocDate'],
            direccionEntrega=data['TaxExtension']['StreetS'],
            direccionDespacho=data['TaxExtension']['StreetB'],
            horarioEntrega=datetime.now(),
            referencia=data.get('NumAtCard', ''),
            comentario=data.get('Comments', ''),
            totalAntesDelDescuento=data['DocTotal'],
            descuento=0,
            totalDocumento=data['DocTotal'],
            codigoVenta=data['SalesPersonCode'],
            tipo_documento=document_type,
            vendedor=seller,
            condi_pago=condicion_pago,
            tipoentrega=tipo_entrega,
            tipoobjetoSap=tipo_objeto,
            tipoVenta=tipo_venta,
            socio_negocio=business_partner,
        )

        # Crear líneas relacionadas al documento
        for linea_num, linea in enumerate(data['DocumentLines'], start=1):
            item_code = ProductoDB.objects.get(codigo=linea['ItemCode'])

            LineaDB.objects.create(
                documento=document,  # ¡Aquí se establece la relación!
                producto=item_code,
                numLinea=linea_num,
                descuento=linea['DiscountPercent'],
                cantidad=linea['Quantity'],
                precioUnitario=linea['UnitPrice'],
                totalBrutoLinea=item_code.precioVenta * linea['Quantity'],
                totalNetoLinea=(item_code.precioVenta * linea['Quantity']) - 
                                (item_code.precioVenta * linea['Quantity'] * linea['DiscountPercent'] / 100),
                comentario=linea['FreeText'],
                fechaEntrega=linea['ShipDate'],
                docEntryBase=0,
                numLineaBase=0,
                direccionEntrega=data['TaxExtension']['StreetS'],
                tipoentrega=tipo_entrega,
                tipoobjetoSap=tipo_objeto,
            )

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


    @staticmethod
    @transaction.atomic
    def update_document_db(docEntry, data):
        try:
            document = DocumentoDB.objects.get(docEntry=docEntry)
        except DocumentoDB.DoesNotExist:
            raise ValueError(f"Documento con docEntry={docEntry} no existe")

        # Actualiza campos del documento
        document.fechaDocumento = data.get('DocDate', document.fechaDocumento)
        document.fechaEntrega = data.get('DocDate', document.fechaEntrega)
        document.direccionEntrega = data['TaxExtension']['StreetS']
        document.direccionDespacho = data['TaxExtension']['StreetB']
        document.referencia = data.get('NumAtCard', document.referencia)
        document.comentario = data.get('Comments', document.comentario)
        document.totalAntesDelDescuento = data.get('DocTotal', document.totalAntesDelDescuento)
        document.totalDocumento = data.get('DocTotal', document.totalDocumento)
        
        # Actualiza relaciones si cambia el vendedor o condición de pago
        if 'SalesPersonCode' in data:
            document.vendedor = VendedorDB.objects.get(codigo=data['SalesPersonCode'])

        if 'PaymentGroupCode' in data:
            document.condi_pago = CondicionPagoDB.objects.get(codigo=data['PaymentGroupCode'])

        document.save()

        # Borrar líneas anteriores y recrearlas (opcional, o puedes hacer update por ID si las tienes)
        LineaDB.objects.filter(documento=document).delete()

        for linea_num, linea in enumerate(data['DocumentLines'], start=1):
            item_code = ProductoDB.objects.get(codigo=linea['ItemCode'])

            LineaDB.objects.create(
                documento=document,
                producto=item_code,
                numLinea=linea_num,
                descuento=linea['DiscountPercent'],
                cantidad=linea['Quantity'],
                precioUnitario=linea['UnitPrice'],
                totalBrutoLinea=item_code.precioVenta * linea['Quantity'],
                totalNetoLinea=(item_code.precioVenta * linea['Quantity']) - 
                                (item_code.precioVenta * linea['Quantity'] * linea['DiscountPercent'] / 100),
                comentario=linea['FreeText'],
                fechaEntrega=linea['ShipDate'],
                docEntryBase=0,
                numLineaBase=0,
                direccionEntrega=data['TaxExtension']['StreetS'],
                tipoentrega=document.tipoentrega,
                tipoobjetoSap=document.tipoobjetoSap,
            )

        return document

    @staticmethod
    def get_total_documents(filtro_id=None, filtro_nombre=None, filtro_sucursal=None, filtro_estado=None):
        queryset = DocumentoDB.objects.filter(
            tipoobjetoSap_id=1,
            estado_documento='Borrador'
        )

        if filtro_id:
            queryset = queryset.filter(id=filtro_id)
        if filtro_nombre:
            queryset = queryset.filter(referencia__icontains=filtro_nombre)
        if filtro_sucursal:
            queryset = queryset.filter(sucursal=filtro_sucursal)
        if filtro_estado:
            queryset = queryset.filter(estado_documento=filtro_estado)

        return queryset.count()


    @staticmethod
    def get_document(filtro_id=None, filtro_nombre=None, filtro_sucursal=None, filtro_estado=None, offset=0, limite=20):
        queryset = DocumentoDB.objects.filter(
            tipoobjetoSap_id=1,
            estado_documento='Borrador'
        )

        if filtro_id:
            queryset = queryset.filter(id=filtro_id)
        if filtro_nombre:
            queryset = queryset.filter(referencia__icontains=filtro_nombre)
        if filtro_sucursal:
            queryset = queryset.filter(socio_negocio__sucursal=filtro_sucursal)  # Ajusta si no aplica
        if filtro_estado:
            queryset = queryset.filter(estado_documento=filtro_estado)

        queryset = queryset.select_related('socio_negocio', 'socio_negocio__grupoSN')[offset:offset + limite]

        documentos = []
        for doc in queryset:
            grupo_codigo = str(doc.socio_negocio.grupoSN.codigo).strip()
            if grupo_codigo == "105":
                nombre = f"{doc.socio_negocio.nombre or ''} {doc.socio_negocio.apellido or ''}".strip()
            else:
                nombre = doc.socio_negocio.razonSocial or ''

            documentos.append({
                'id': doc.id,
                'CardCode': doc.socio_negocio.codigoSN,  # Este campo es usado en la segunda columna del JS
                'nombre_cliente': nombre,
                'SalesEmployeeName': doc.vendedor.codigo,  # Ajusta según modelo
                'fechaEntrega': doc.fechaEntrega,
                'estado_documento': doc.estado_documento,
                'totalDocumento': doc.totalDocumento,
            })

        return documentos




