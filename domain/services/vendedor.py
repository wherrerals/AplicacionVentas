from infrastructure.repositories.vendedorRepository import VendedorRepository


class Seller:

    @staticmethod
    def tipoVentaTipoVendedor(codigo_vendedor):
        """
        Asigna el tipo de venta a la cotización.

        Args:
            tipo_venta (str): Tipo de venta.
        """
        repo = VendedorRepository()

        tipo_vendedor = repo.obtenerTipoVendedor(codigo_vendedor)

        if tipo_vendedor == 'P':
            return 'PROY'
        
        elif tipo_vendedor == 'CD':
            return 'ECCO'
        
        else:
            return 'NA'

