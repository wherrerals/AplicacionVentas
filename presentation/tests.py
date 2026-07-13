"""Validación del menú administrable (cards + ítems) y su visibilidad por grupo.

Regla: un ítem se muestra si el usuario pertenece a alguno de los grupos de
``visible_para``. Si el ítem no tiene grupos, es visible para todos los
autenticados. Los superusuarios ven todo. Solo aparecen cards activas con al
menos un ítem visible.

Ejecutar:  python manage.py test presentation
"""

from django.contrib.auth.models import Group, User
from django.test import TestCase

from infrastructure.models import MenuGroup, MenuItem
from presentation.menu import get_menu_for_user


def titulos(menu):
    return [item.titulo for card in menu for item in card["items"]]


class MenuAdministrableTest(TestCase):

    def setUp(self):
        self.card = MenuGroup.objects.create(nombre="Cotizaciones", orden=1)
        self.vendedor = Group.objects.create(name="Vendedor")

        self.item_restringido = MenuItem.objects.create(
            titulo="Nueva Cotización", url_name="generar_cotizacion", grupo=self.card, orden=1
        )
        self.item_restringido.visible_para.add(self.vendedor)

        # Sin visible_para => visible para todos los autenticados.
        self.item_publico = MenuItem.objects.create(
            titulo="Mis Datos", url_name="mis_datos", grupo=self.card, orden=2
        )

    def test_usuario_en_grupo_ve_item_de_ese_grupo(self):
        u = User.objects.create_user("vendedor1", password="x")
        u.groups.add(self.vendedor)
        u = User.objects.get(pk=u.pk)
        self.assertIn("Nueva Cotización", titulos(get_menu_for_user(u)))

    def test_usuario_sin_grupo_no_ve_items_restringidos(self):
        u = User.objects.create_user("sin_grupo", password="x")
        self.assertNotIn("Nueva Cotización", titulos(get_menu_for_user(u)))

    def test_item_sin_grupos_es_visible_para_todos(self):
        u = User.objects.create_user("cualquiera", password="x")
        self.assertEqual(titulos(get_menu_for_user(u)), ["Mis Datos"])

    def test_superusuario_ve_todo(self):
        su = User.objects.create_superuser("admin1", "admin@test.cl", "x")
        self.assertEqual(set(titulos(get_menu_for_user(su))), {"Nueva Cotización", "Mis Datos"})

    def test_card_inactiva_no_aparece(self):
        self.card.activo = False
        self.card.save()
        su = User.objects.create_superuser("admin2", "admin2@test.cl", "x")
        self.assertEqual(get_menu_for_user(su), [])

    def test_item_inactivo_no_aparece(self):
        self.item_publico.activo = False
        self.item_publico.save()
        u = User.objects.create_user("cualquiera2", password="x")
        self.assertNotIn("Mis Datos", titulos(get_menu_for_user(u)))

    def test_estructura_devuelta_es_card_con_items(self):
        su = User.objects.create_superuser("admin3", "admin3@test.cl", "x")
        menu = get_menu_for_user(su)
        self.assertEqual(len(menu), 1)
        self.assertEqual(menu[0]["grupo"], self.card)
        self.assertTrue(all(isinstance(i, MenuItem) for i in menu[0]["items"]))
