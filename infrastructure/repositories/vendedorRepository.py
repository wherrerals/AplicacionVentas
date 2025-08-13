from infrastructure.models import VendedorDB
from infrastructure.models.usuariodb import UsuarioDB

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

    def get_sucursal(codigo_vendedor):
        """Obtiene la sucursal del vendedor a partir del código de vendedor."""
        try:
            vendedor_usuario = UsuarioDB.objects.get(vendedor__codigo=codigo_vendedor)
            return vendedor_usuario.sucursal_id
        except UsuarioDB.DoesNotExist:
            return None

