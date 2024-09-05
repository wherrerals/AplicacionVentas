from datosLsApp.models import GrupoSNDB
from django.core.exceptions import ValidationError

class GrupoSNRepository:
    
    @staticmethod
    def obtenerGrupoSNPorCodigo(codigo):
        try:
            return GrupoSNDB.objects.get(codigo=codigo)
        except GrupoSNDB.DoesNotExist:
            raise ValidationError(f"GrupoSN no encontrado para el código: {codigo}")
