# datosLsApp/repositories/grupo_repository.py
from datosLsApp.models import TipoSNDB

class TipoSNRepository:
    """
    
    Repositorio de Tipos de Socios de Negocio

    Metodos disponibles:

    - obtenerTipoSnPorCodigo(codigo)

    """

    @staticmethod
    def obtenerTipoSnPorCodigo(codigo):

        """
        Obtiene un objeto TipoSNDB basado en el código proporcionado.

        Params:
            codigo (str): El código del tipo de socio de negocio que se desea obtener.

        Returns:

            TipoSNDB: El objeto TipoSNDB correspondiente al código.
        """
        try:
            return TipoSNDB.objects.get(codigo=codigo)
        except TipoSNDB.DoesNotExist:
            return None
