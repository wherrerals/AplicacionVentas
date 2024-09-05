# datosLsApp/repositories/grupo_repository.py
from datosLsApp.models import GrupoSNDB, TipoClienteDB, TipoSNDB

class GrupoRepository:
    
    @staticmethod
    def obtener_grupo_por_codigo(codigo):
        try:
            return GrupoSNDB.objects.get(codigo=codigo)
        except GrupoSNDB.DoesNotExist:
            return None

    @staticmethod
    def obtener_tipo_cliente_por_codigo(codigo):
        try:
            return TipoClienteDB.objects.get(codigo=codigo)
        except TipoClienteDB.DoesNotExist:
            return None

    @staticmethod
    def obtener_tipo_sn_por_codigo(codigo):
        try:
            return TipoSNDB.objects.get(codigo=codigo)
        except TipoSNDB.DoesNotExist:
            return None
