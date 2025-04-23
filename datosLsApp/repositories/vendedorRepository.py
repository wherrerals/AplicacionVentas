from datosLsApp.models import VendedorDB

class VendedorRepository:
    
    def obtenerTipoVendedor(self, codigo):
        """
        Obtiene el tipo de vendedor.
        """

        try:
            vendedor = VendedorDB.objects.get(codigo=codigo)
            return vendedor.tipoVendedor
        except VendedorDB.DoesNotExist:
            return 'NA'
    
    def obtenerNombreVendedor(codigo):
        """
        Obtiene el nombre del vendedor.
        """

        vendedor = VendedorDB.objects.get(codigo=codigo)
        return vendedor.nombre
    
    def get_branch_code(codigo):

        vendedor = VendedorDB.objects.get(codigo=codigo)

        return vendedor.sucursal.codigoSucursal
