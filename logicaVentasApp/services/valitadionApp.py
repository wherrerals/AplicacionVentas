from datosLsApp.models.usuariodb import UsuarioDB


class ValitadionApp:

    @staticmethod
    def user_autentication(request):
        if request.user.is_authenticated:
            return True
        else:
            return False