from django.contrib.auth.models import AnonymousUser

def grupos_usuario(request):
    #print("Ejecutando context processor grupos_usuario")
    if isinstance(request.user, AnonymousUser):
        return {'grupos_usuario': []}

    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    return {'grupos_usuario': grupos_usuario}

def usuario_actual(request):
    #print("Ejecutando context processor usuario_actual")
    if isinstance(request.user, AnonymousUser):
        return {'usuario_actual': None}

    return {'usuario_actual': request.user}

def vendedor_actual(request):
    #print("Ejecutando context processor vendedor_actual")
    if isinstance(request.user, AnonymousUser):
        return {'vendedor_actual': None}

    return {'vendedor_actual': request.user.vendedor}