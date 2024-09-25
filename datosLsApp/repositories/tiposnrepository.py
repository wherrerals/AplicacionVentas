# datosLsApp/repositories/grupo_repository.py
from datosLsApp.models import TipoSNDB

class TipoSNRepository:

    @staticmethod
    def obtenerTipoSnPorCodigo(codigo):
        try:
            return TipoSNDB.objects.get(codigo=codigo)
        except TipoSNDB.DoesNotExist:
            return None
