from django.contrib.auth.models import AnonymousUser

def grupos_usuario(request):
    print("Ejecutando context processor grupos_usuario")
    if isinstance(request.user, AnonymousUser):
        return {'grupos_usuario': []}

    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return {'grupos_usuario': grupos_usuario}
