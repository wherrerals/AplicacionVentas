from django.utils import timezone

from domain.services import producto
from infrastructure.repositories.pricelistrepository import PriceListRepository
from infrastructure.repositories.productorepository import ProductoRepository


class ListPriceService:
    """
    Lógica de negocio para validar listas de precios de un producto.
    """

    def __init__(self, sku, costo, user, cardCode=None):
        self.sku = sku
        self.costo = costo
        self.user = user
        self.rentability = 50
        self.price_list = 0
        self.list_price_product = 0
        self.cardCode = cardCode
        self.list_price_sn = None

    def load_data(self):
        """Carga datos del producto y su lista de precios usando el repository"""
        self.list_price_product = PriceListRepository.get_product_price(self.sku, self.cardCode)
        self.price_list = self.list_price_product.code_list if self.list_price_product else 0

        print(f"Lista de precios cargada: {self.price_list} para el SKU: {self.sku}")
        print(f"Producto-Lista de precios cargada: {self.list_price_product} para el SKU: {self.sku}")

    def is_valid_by_date(self) -> bool:
        """Valida que la lista de precios esté vigente en fechas"""
        if not self.price_list:
            return False

        now = timezone.now()
        valid_from = self.price_list.valid_from
        valid_to = self.price_list.valid_to

        if valid_from and valid_to:
            return valid_from <= now <= valid_to
        if valid_from and not valid_to:
            return now >= valid_from
        if not valid_from and valid_to:
            return now <= valid_to
        return False

    def list_price_is_active(self) -> bool:
        """Valida si la lista de precios está activa"""
        return bool(self.price_list and self.price_list.active is True)
    
    def get_price(self) -> float:
        """Retorna el precio de la lista de precios para el producto"""
        self.load_data()
        if not (self.is_valid_by_date() and self.list_price_is_active()):
            print("Lista de precios no válida o inactiva")
            return 0.0
        print("Lista de precios válida y activa")
        return self.list_price_product.price_list
    
    def new_discounted_price(self) -> float:
        """Calcula un nuevo precio con el descuento de rentabilidad"""
        repo = ProductoRepository()
        self.load_data()

        if not self.list_price_product:
            print("No hay lista de precios asociada")
            # No hay lista de precios asociada
            return 0.0

        print("Calculando margen y descuento...")
        margen_bruto, descuento = repo.calculate_margen_descuentos(
            float(self.list_price_product.price_list),
            self.costo,
            self.rentability
        )

        print(f"Margen bruto: {margen_bruto}, Descuento aplicado: {descuento}")
        return descuento

    

    def get_list_price_info(self) -> dict:
        """Retorna un diccionario con la información de la lista de precios"""


        new_price = self.get_price()
        print(f"validando precio: {new_price}")

        new_discounted_price = self.new_discounted_price()

        if new_price == 0.0:
            return 0.0, 0.0

        return new_price, new_discounted_price