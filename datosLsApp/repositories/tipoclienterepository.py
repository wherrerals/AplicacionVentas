from datosLsApp.models import TipoClienteDB

class TipoClienteRepository:
    
    @staticmethod
    def obtenerTipoClientePorCodigo(codigo):
        """
        Obtiene un objeto TipoClienteDB basado en el código proporcionado.
        
        Params:
            codigo (str): El código del tipo de cliente que se desea obtener.
        
        Returns:
            TipoClienteDB: El objeto TipoClienteDB correspondiente al código.
        """
        try:
            return TipoClienteDB.objects.get(codigo=codigo)
        except TipoClienteDB.DoesNotExist:
            return None
    
    @staticmethod
    def obtenerTodosTiposClientes():
        """
        Obtiene todos los objetos TipoClienteDB.
        
        Returns:
            QuerySet: Un conjunto de objetos TipoClienteDB.
        """
        return TipoClienteDB.objects.all()
