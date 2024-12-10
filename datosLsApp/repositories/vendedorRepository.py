from datosLsApp.models import VendedorDB

class VendedorRepository:
    def obtenerTipoVendedor(self, codigo):
        """
        Obtiene el tipo de vendedor.
        """

        vendedor = VendedorDB.objects.get(codigo=codigo)
        return vendedor.tipoVendedor
