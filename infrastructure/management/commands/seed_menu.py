"""Carga inicial del menú (cards e ítems) reproduciendo la estructura actual.

Es idempotente: se puede ejecutar varias veces sin duplicar datos. Solo crea
lo que falta y actualiza los datos de cada ítem. La asignación de visibilidad
(``visible_para``) usa los grupos existentes (no crea grupos de auth).

Uso:
    python manage.py seed_menu
"""

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from infrastructure.models import MenuGroup, MenuItem

# (nombre_card, orden, [(titulo, url_name, descripcion, [grupos_visibilidad]), ...])
MENU_SEED = [
    ("Cotizaciones", 1, [
        ("Nueva Cotización", "generar_cotizacion", "Ingresa para crear una nueva cotización.", ["Vendedor", "Administrador"]),
        ("Listado Cotizaciones", "lista_cotizaciones", "Lista de cotizaciones SAP.", ["Vendedor", "Administrador"]),
    ]),
    ("Órdenes de Venta", 2, [
        ("Nueva Órden de Venta", "ordenesVentas", "Ingresa para crear una nueva Órden.", ["Vendedor", "Administrador"]),
        ("Listado Órdenes de Venta", "lista_ovs", "Lista de órdenes de venta SAP.", ["Vendedor", "Administrador"]),
    ]),
    ("Devoluciones", 3, [
        ("Listado Solicitudes Devolución", "lista_solic_devoluciones", "Lista de solicitudes de devolución SAP.", ["Vendedor", "Administrador", "Supervisor"]),
        ("Listado Solicitudes Pendientes", "pending_rr", "Ingresa para ver las Solicitudes D. Pendientes.", ["Administrador", "Supervisor"]),
    ]),
    ("Clientes", 4, [
        ("Crear Clientes", "creacion_clientes", "Ingresa para crear nuevos clientes.", ["Vendedor", "Administrador"]),
        ("Listado Clientes", "lista_clientes", "Lista de clientes SAP.", ["Vendedor", "Administrador"]),
    ]),
    ("Ventas y Reportes", 5, [
        ("Consulta de Ventas", "lista_ventas", "Consulta de boletas y facturas.", ["Vendedor", "Administrador"]),
        ("Reportes de productos", "reporte_stock", "Reportes de stock, precios y descuentos.", ["Vendedor", "Administrador", "Comex"]),
    ]),
    ("Mi Cuenta", 6, [
        ("Mis Datos", "mis_datos", "Modificación de datos personales.", ["Vendedor", "Administrador"]),
    ]),
]


class Command(BaseCommand):
    help = "Crea/actualiza las cards e ítems del menú por defecto (idempotente)."

    def handle(self, *args, **options):
        for card_nombre, card_orden, items in MENU_SEED:
            card, _ = MenuGroup.objects.get_or_create(nombre=card_nombre)
            card.orden = card_orden
            card.activo = True
            card.save()

            for i, (titulo, url_name, descripcion, roles) in enumerate(items, start=1):
                item, _ = MenuItem.objects.get_or_create(titulo=titulo, grupo=card)
                item.url_name = url_name
                item.descripcion = descripcion
                item.orden = i
                item.activo = True
                item.save()

                grupos = Group.objects.filter(name__in=roles)
                faltantes = set(roles) - set(grupos.values_list("name", flat=True))
                if faltantes:
                    self.stdout.write(self.style.WARNING(
                        f"  · '{titulo}': grupos inexistentes {sorted(faltantes)} (se omiten)"
                    ))
                item.visible_para.set(grupos)

            self.stdout.write(self.style.SUCCESS(f"Card '{card_nombre}' con {len(items)} ítem(s)"))

        self.stdout.write(self.style.SUCCESS("Seed de menú completado."))
