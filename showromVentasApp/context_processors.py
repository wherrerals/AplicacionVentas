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

def vendedor_codigo(request):
    if request.user.is_authenticated:
        usuario_db = getattr(request.user, 'usuariodb', None)  # Asegúrate de que `usuariodb` sea el related_name o nombre del modelo relacionado.
        return {'codigo_vendedor': usuario_db.vendedor_codigo if usuario_db else None}
    return {'codigo_vendedor': None}


def usuario_actual(request):
    #print("Ejecutando context processor usuario_actual")
    if isinstance(request.user, AnonymousUser):
        return {'usuario_actual': None}

    return {'usuario_actual': request.user}