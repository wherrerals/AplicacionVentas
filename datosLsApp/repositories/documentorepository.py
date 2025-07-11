from datosLsApp.models import DocumentoDB
from datosLsApp.models.condicionpagodb import CondicionPagoDB
from datosLsApp.models.lineadb import LineaDB
from datosLsApp.models.productodb import ProductoDB
from datosLsApp.models.socionegociodb import SocioNegocioDB
from datosLsApp.models.tipodoctributariodb import TipoDocTributarioDB
from datosLsApp.models.tipoentregadb import TipoEntregaDB
from datosLsApp.models.tipoobjetosapdb import TipoObjetoSapDB
from datosLsApp.models.tipoventadb import TipoVentaDB
from datosLsApp.models import UsuarioDB
from datosLsApp.models.vendedordb import VendedorDB
from django.db import connection, transaction
from datetime import datetime
from django.db.models import Q
from django.db.models import Subquery



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
        print(f"Creando documento con datos: {data}")
        business_partner = SocioNegocioDB.objects.get(codigoSN=data['CardCode'])
        document_type = TipoDocTributarioDB.objects.get(codigo=data['U_LED_TIPDOC'])
        seller = VendedorDB.objects.get(codigo=data['SalesPersonCode'])
        print(data['U_LED_TIPVTA'])
        tipo_venta = TipoVentaDB.objects.get(codigo=data['U_LED_TIPVTA'])  # puedes cambiar esto si luego usas el dato dinámico
        tipo_entrega = TipoEntregaDB.objects.get(codigo='1')
        condicion_pago = CondicionPagoDB.objects.get(codigo=data['PaymentGroupCode'])
        tipo_objeto = TipoObjetoSapDB.objects.get(codigo="1")

        # Crear el documento
        document = DocumentoDB.objects.create(
            docEntry=0,
            docNum=0,
            folio=data['U_VK_Folio'],
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
            DoctotalBase=data['DocTotalBase'],
            docEntry_relacionado=data['RefDocEntr'],
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

            # Condición para cantidad
            #cantidad = 0 if linea['EstadoCheck'] == 0 else linea['Quantity']

            LineaDB.objects.create(
                documento=document,  # ¡Aquí se establece la relación!
                producto=item_code,
                numLinea=linea_num,
                descuento=linea['DiscountPercent'],
                cantidad=linea['Quantity'], # Asignar cantidad solicitada
                cantidad_solicitada=linea['Quantity2'],  
                precioUnitario=linea['UnitPrice'],
                totalBrutoLinea=item_code.precioVenta * linea['Quantity'],
                totalNetoLinea=(item_code.precioVenta * linea['Quantity']) - 
                                (item_code.precioVenta * linea['Quantity'] * linea['DiscountPercent'] / 100),
                comentario=linea['FreeText'],
                fechaEntrega=linea['ShipDate'],
                docEntryBase=linea['DocEntryBase'],
                numLineaBase=linea['LineNum'],
                direccionEntrega=data['TaxExtension']['StreetS'],
                tipoentrega=tipo_entrega,
                tipoobjetoSap=tipo_objeto,
                estado_devolucion=linea['EstadoCheck'],
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
    def update_document_db(id, data):
        print(f"Actualizando documento con id: {id} y datos: {data}")
        try:
            document = DocumentoDB.objects.get(id=id)
        except DocumentoDB.DoesNotExist:
            raise ValueError(f"Documento con docEntry={id} no existe")

        # Actualiza campos del documento
        document.folio = data.get('U_VK_Folio', document.folio)
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
                estado_devolucion=linea['EstadoCheck'],
                precioUnitario=linea['UnitPrice'],
                totalBrutoLinea=linea['UnitPrice'] * linea['Quantity'],
                totalNetoLinea=(linea['UnitPrice'] * linea['Quantity']) - 
                                (linea['UnitPrice'] * linea['Quantity'] * linea['DiscountPercent'] / 100),
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

        # Obtener los vendedores que tengan usuarios con esa sucursal
        if filtro_sucursal:
            vendedores_en_sucursal = UsuarioDB.objects.filter(
                sucursal=filtro_sucursal
            ).values('vendedor')

        print("Vendedores en sucursal:", vendedores_en_sucursal)

        queryset = DocumentoDB.objects.filter(
            tipoobjetoSap_id=1,
            estado_documento='Borrador'
        )

        if filtro_id:
            queryset = queryset.filter(id=filtro_id)
        if filtro_nombre:
            queryset = queryset.filter(
                Q(socio_negocio__nombre__icontains=filtro_nombre) |
                Q(socio_negocio__codigoSN__icontains=filtro_nombre)
            )
        if filtro_sucursal:
            queryset = queryset.filter(vendedor__in=Subquery(vendedores_en_sucursal))
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
            queryset = queryset.filter(
                Q(socio_negocio__nombre__icontains=filtro_nombre) |
                Q(socio_negocio__codigoSN__icontains=filtro_nombre)
            )
            
        """
        if filtro_sucursal:
            vendedores_en_sucursal = UsuarioDB.objects.filter(
                sucursal=filtro_sucursal
            ).values('vendedor')
            queryset = queryset.filter(vendedor__in=Subquery(vendedores_en_sucursal))
        """

        if filtro_estado:
            queryset = queryset.filter(estado_documento=filtro_estado)

        queryset = queryset.select_related(
            'socio_negocio', 
            'socio_negocio__grupoSN'
        )[offset:offset + limite]

        documentos = []
        for doc in queryset:
            grupo_codigo = str(doc.socio_negocio.grupoSN.codigo).strip()
            if grupo_codigo == "105":
                nombre = f"{doc.socio_negocio.nombre or ''} {doc.socio_negocio.apellido or ''}".strip()
            else:
                nombre = doc.socio_negocio.razonSocial or ''

            documentos.append({
                'id': doc.id,
                'CardCode': doc.socio_negocio.codigoSN,
                'nombre_cliente': nombre,
                'SalesEmployeeCode': doc.vendedor.codigo,
                'SalesEmployeeName': doc.vendedor.nombre,
                'fechaEntrega': doc.fechaEntrega,
                'estado_documento': doc.estado_documento,
                'totalDocumento': doc.totalDocumento,
            })

        print(f"documentos: {documentos}")

        return documentos



    @staticmethod
    def get_document_data_lines(filtro_id=None):
        queryset = DocumentoDB.objects.select_related(
            'socio_negocio', 'vendedor', 'tipoentrega', 'tipo_documento'
        ).prefetch_related('lineas__producto')

        if filtro_id:
            queryset = queryset.filter(id=filtro_id)

        documentos = []

        for doc in queryset:
            sucursal_codigo = ""
            try:
                usuario = UsuarioDB.objects.select_related('sucursal', 'vendedor').get(vendedor__codigo=doc.vendedor.codigo)
                sucursal_codigo = usuario.sucursal.codigo
                print(f"Usuario encontrado: {usuario}, Sucursal: {usuario.sucursal.codigo}")
            except UsuarioDB.DoesNotExist:
                pass

            lineas_serializadas = []
            for linea in doc.lineas.all():
                lineas_serializadas.append({
                    "cantidad": linea.cantidad,
                    "cantidad_original": linea.cantidad_solicitada,
                    "producto_codigo": linea.producto.codigo,
                    "producto_nombre": linea.producto.nombre,
                    "precio_unitario": linea.precioUnitario,
                    "precio_lista": linea.producto.precioLista,
                    "total_bruto": linea.totalBrutoLinea,
                    "descuento": linea.descuento,
                    "comentario": linea.comentario,
                    "fecha_entrega": str(linea.fechaEntrega),
                    "tipo_entrega_codigo": linea.tipoentrega.codigo,
                    "num_linea": linea.numLinea,
                    "linea_base": linea.numLineaBase,
                    "imagen_url": linea.producto.imagen,
                    "warehouse": linea.direccionEntrega,
                    "estate_rr_line": linea.estado_devolucion,
                })

            documentos.append({
                "id": doc.id,
                "docNum": doc.docNum,
                "docEntry": doc.docEntry,
                "folio": doc.folio,
                "fechaEntrega": str(doc.fechaEntrega),
                "estado_documento": doc.estado_documento,
                "RefDocEntr": doc.docEntry_relacionado,
                "CardCode": doc.socio_negocio.codigoSN,
                "nombre_cliente": (
                    f"{doc.socio_negocio.nombre} {doc.socio_negocio.apellido}"
                    if doc.socio_negocio.grupoSN.codigo == "105"
                    else doc.socio_negocio.razonSocial
                ),
                "referencia": doc.referencia,
                "comentario": doc.comentario,
                "SalesEmployeeName": doc.vendedor.nombre,
                "SalesEmployeeCode": doc.vendedor.codigo,
                "U_LED_SUCURS": sucursal_codigo,
                "TransportationCode": doc.tipoentrega.codigo,
                "U_LED_TIPDEV": doc.tipoentrega.nombre,
                "U_LED_TIPDOC": doc.tipo_documento.codigo,
                "lineas": lineas_serializadas
            })

        return documentos


    @staticmethod
    def update_document_status(id, doc_num,doc_entry, estado):
        """
        actualiza el estado de un documento, su docNum y docEntry por su id
        """
        print(f"Actualizando estado del documento con id: {id}, docNum: {doc_num}, docEntry: {doc_entry}, estado: {estado}")
        try:
            document = DocumentoDB.objects.get(id=id)
        except DocumentoDB.DoesNotExist:
            raise ValueError(f"Documento con id={id} no existe")

        document.estado_documento = estado
        document.docNum = doc_num
        document.docEntry = doc_entry
        document.save()

        return True


