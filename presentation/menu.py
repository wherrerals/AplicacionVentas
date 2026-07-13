"""Construcción del menú principal (Home) desde la base de datos.

La estructura (cards e ítems) y la visibilidad se administran desde el admin
de Django con los modelos ``MenuGroup`` y ``MenuItem``:

- ``MenuGroup``  → la card que agrupa varios accesos.
- ``MenuItem``   → cada acceso; ``visible_para`` (M2M a Grupos) decide quién lo ve.

La plantilla ``home.html`` solo itera el resultado de ``get_menu_for_user``,
sin ninguna lógica de permisos.
"""

from infrastructure.models import MenuGroup


def get_menu_for_user(user):
    """Devuelve las cards con sus ítems visibles para ``user``.

    Estructura devuelta::

        [ {"grupo": <MenuGroup>, "items": [<MenuItem>, ...]}, ... ]

    Reglas de visibilidad de un ítem:
    - Superusuario: ve todos los ítems activos.
    - Ítem sin ``visible_para``: visible para cualquier usuario autenticado.
    - En otro caso: visible si el usuario pertenece a alguno de esos grupos.

    Solo se incluyen cards activas que tengan al menos un ítem visible.
    """
    if not user or not user.is_authenticated:
        return []

    es_super = user.is_superuser
    grupos_usuario_ids = set(user.groups.values_list("id", flat=True))

    cards = (
        MenuGroup.objects.filter(activo=True)
        .prefetch_related("items", "items__visible_para")
        .order_by("orden", "id")
    )

    menu = []
    for card in cards:
        items_visibles = []
        for item in card.items.all():
            if not item.activo:
                continue
            ids_permitidos = {g.id for g in item.visible_para.all()}
            if es_super or not ids_permitidos or (grupos_usuario_ids & ids_permitidos):
                items_visibles.append(item)
        if items_visibles:
            menu.append({"grupo": card, "items": items_visibles})
    return menu
