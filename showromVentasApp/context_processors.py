from django.contrib.auth.models import AnonymousUser

def grupos_usuario(request):
    if isinstance(request.user, AnonymousUser):
        return {'grupos_usuario': []}
    grupos_usuario = list(request.user.groups.values_list('name', flat=True))
    print(f"Grupos del usuario: {grupos_usuario}")
    return {'grupos_usuario': grupos_usuario}

def usuario_actual(request):
    if isinstance(request.user, AnonymousUser):
        return {'usuario_actual': None}
    
    return {'usuario_actual': request.user}

def vendedor_codigo(request):
    if request.user.is_authenticated:
        usuario_db = getattr(request.user, 'usuariodb', None)  # Relación con UsuarioDB
        
        # Obtener nombre del vendedor
        vendedor_nombre = usuario_db.vendedor.nombre if usuario_db and hasattr(usuario_db, 'vendedor') else None
        vendedor_codigo = usuario_db.vendedor.codigo if usuario_db and hasattr(usuario_db, 'vendedor') else None

        # Obtener showroom del usuario
        showroom = usuario_db.sucursal.nombre if usuario_db and hasattr(usuario_db, 'sucursal') else "No asignado"

        # Logs para depuración
        print(f"Vendedor Nombre: {vendedor_nombre}")
        print(f"Vendedor Código: {vendedor_codigo}")
        print(f"Showroom: {showroom}")
        
        return {
            'vendedor_nombre': vendedor_nombre,
            'codigo_vendedor': vendedor_codigo,
            'showroom': showroom
        }

    return {'vendedor_nombre': None, 'codigo_vendedor': None, 'showroom': "No asignado"}
