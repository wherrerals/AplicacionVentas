from datosLsApp.models import DocumentoDB

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
    def crearDocumento(**kwargs):
        """
        Crea un documento en la base de datos
        
        params:
            kwargs: dict

            - Datos del documento a crear
        
        return:
            DocumentoDB
        """
        return DocumentoDB.objects.create(**kwargs)
    
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