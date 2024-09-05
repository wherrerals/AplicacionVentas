# datosLsApp/repositories/socio_negocio_repository.py
from datosLsApp.models import SocioNegocioDB

class SocioNegocioRepository:
    
    @staticmethod
    def obtener_por_rut(rut):
        try:
            return SocioNegocioDB.objects.get(rut=rut)
        except SocioNegocioDB.DoesNotExist:
            return None

    @staticmethod
    def crear_cliente(**kwargs):
        return SocioNegocioDB.objects.create(**kwargs)
