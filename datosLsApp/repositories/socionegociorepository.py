from datosLsApp.models import SocioNegocioDB

class SocioNegocioRepository:
    
    @staticmethod
    def obtenerPorRut(rut):
        """
        Obtiene un socio de negocio por su rut
        
        params:
            rut: str

            - Rut del socio de negocio a buscar
        
        return:
            SocioNegocioDB | None
        """
        try:
            return SocioNegocioDB.objects.get(rut=rut)
        except SocioNegocioDB.DoesNotExist:
            return None

    @staticmethod
    def crearCliente(**kwargs):
        """
        Crea un cliente en la base de datos
        
        params:
            kwargs: dict

            - Datos del cliente a crear
        
        return:
            SocioNegocioDB
        """
        return SocioNegocioDB.objects.create(**kwargs)

    @staticmethod

    @staticmethod
    def buscarClientesPorRut(rut):
        return SocioNegocioDB.objects.filter(rut__icontains=rut)

    @staticmethod
    def buscarClientesPorNombre(nombre):
        return SocioNegocioDB.objects.filter(nombre__icontains=nombre)

