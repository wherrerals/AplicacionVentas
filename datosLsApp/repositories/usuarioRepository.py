from datosLsApp.models.usuariodb import UsuarioDB


class UserRepository:
    @staticmethod
    def get_sucursal(codigo_vendedor):
        """Obtiene la sucursal del vendedor a partir del código de vendedor."""
        try:
            vendedor_usuario = UsuarioDB.objects.get(vendedor__codigo=codigo_vendedor)
            return vendedor_usuario.sucursal_id
        except UsuarioDB.DoesNotExist:
            return None