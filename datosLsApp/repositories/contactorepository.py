from datosLsApp.models import ContactoDB

class ContactoRepository:

    def obtenerContactosPorCliente(self, cliente):
        """
        Obtiene las direcciones de un cliente

        params:
            cliente: SocioNegocioDB

            - Cliente al que pertenecen las direcciones

        return:
            QuerySet
        """
        return ContactoDB.objects.filter(SocioNegocio=cliente)
