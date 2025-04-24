from datosLsApp.models.usuariodb import UsuarioDB


class UserContext:

    def user_context(authenticated, request):

        context = {
            'doc_num': request.GET.get('doc_num'),
            'regiones': request.GET.get('regiones'),
        }

        if authenticated:
            context['username'] = request.user.username

            try:
                usuario = UsuarioDB.objects.get(usuarios=request.user)
                context.update({
                    'sucursal': usuario.sucursal,
                    'nombreuser': usuario.nombre,
                    'codeVendedor': usuario.vendedor.codigo,
                })

            except UsuarioDB.DoesNotExist:
                context.update({
                    'sucursal': 'No se encontró la sucursal',
                    'nombreuser': 'No se encontró el usuario',
                    'codeVendedor': 'No se encontró el vendedor',
                })
                
        return context