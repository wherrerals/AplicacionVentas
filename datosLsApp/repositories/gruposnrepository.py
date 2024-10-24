from datosLsApp.models import GrupoSNDB
from django.core.exceptions import ValidationError

class GrupoSNRepository:
    """
    Repositorio de GruposSN

    Metodos disponibles:

    - obtenerGrupoSNPorCodigo(codigo)
    """
    @staticmethod
    def obtenerGrupoSNPorCodigo(codigo):

        """
        Obtiene un GrupoSN por su código

        params:

            codigo: str - Código del GrupoSN

        return:
            GrupoSNDB - GrupoSN encontrado
        """
        try:
            return GrupoSNDB.objects.get(codigo=codigo)
        except GrupoSNDB.DoesNotExist:
            raise ValidationError(f"GrupoSN no encontrado para el código: {codigo}")
