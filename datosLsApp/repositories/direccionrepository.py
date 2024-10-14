from datosLsApp.models import DireccionDB

class DireccionRepository:

    def obtenerDireccionesPorCliente(self, cliente):
        """
        Obtiene las direcciones de un cliente

        params:
            cliente: SocioNegocioDB

            - Cliente al que pertenecen las direcciones

        return:
            QuerySet
        """
        return DireccionDB.objects.filter(SocioNegocio=cliente)

    def prueba(self):
        pass
