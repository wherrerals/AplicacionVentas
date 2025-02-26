

from datosLsApp.models.usuariodb import UsuarioDB


class User:

    @staticmethod
    def user_data(request):
        
        user = request.user

        codigoVendedor = UsuarioDB.objects.get(usuarios=user).vendedor.codigo

        return {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'vendedor': codigoVendedor
        }
    
    @staticmethod
    def validar_vendedor(vendedor1, vendedor2):
        if vendedor1 == vendedor2:
            return True
        else:
            return False