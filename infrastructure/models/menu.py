from django.contrib.auth.models import Group
from django.db import models


class MenuGroup(models.Model):
    """Grupo de menú = una 'card' del Home que agrupa varios accesos.

    El administrador crea las cards y define su orden desde el admin de Django.
    """

    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField(default=0, help_text="Posición de la card en el Home (menor = primero).")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "menu_group"
        verbose_name = "Grupo de menú"
        verbose_name_plural = "Grupos de menú"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.nombre


class MenuItem(models.Model):
    """Ítem de menú = un enlace (acceso) que se muestra dentro de una card.

    La visibilidad se controla con ``visible_para``: el ítem se muestra a los
    usuarios que pertenezcan a alguno de esos grupos. Si se deja vacío, el ítem
    es visible para todos los usuarios autenticados.
    """

    titulo = models.CharField(max_length=100)
    url_name = models.CharField(
        max_length=100,
        help_text="Nombre de la URL en urls.py, ej: lista_clientes",
    )
    descripcion = models.CharField(max_length=255, blank=True)
    grupo = models.ForeignKey(
        MenuGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
        verbose_name="Card (grupo de menú)",
    )
    visible_para = models.ManyToManyField(
        Group,
        blank=True,
        related_name="menu_items",
        verbose_name="Visible para los grupos",
        help_text="Grupos que pueden ver este acceso. Vacío = visible para todos los usuarios autenticados.",
    )
    orden = models.PositiveIntegerField(default=0, help_text="Posición dentro de la card (menor = primero).")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "menu_item"
        verbose_name = "Ítem de menú"
        verbose_name_plural = "Ítems de menú"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo
