from django.db import transaction

from django.db.models import Sum
from datosLsApp.models.productodb import ProductoDB
from datosLsApp.models.stockbodegasdb import StockBodegasDB

class StockService:
    
    def __init__(self):
        self.initial_stock = {}

    def capture_initial_stock(self, sku, bodega_id, cantidad):
        """ Guarda el stock inicial antes de cualquier cambio """
        key = f"{sku}-{bodega_id}"
        self.initial_stock[key] = cantidad

    def get_initial_stock(self, sku, bodega_id):
        """ Obtiene el stock inicial de memoria """
        key = f"{sku}-{bodega_id}"
        return self.initial_stock.get(key, 0)

    @transaction.atomic
    def actualizar_stock(self, sku, bodega_id, nueva_cantidad):
        """
        Actualiza el stock de una bodega específica y el stock total del producto.
        """
        stock_bodega = StockBodegasDB.objects.select_for_update().filter(
            idProducto__codigo=sku, idBodega=bodega_id
        ).first()

        if not stock_bodega:
            raise ValueError(f"No se encontró stock para SKU {sku} en Bodega {bodega_id}")

        # Stock inicial antes de la actualización
        stock_inicial = self.get_initial_stock(sku, bodega_id)

        # Determinar si se está agregando o quitando stock
        if nueva_cantidad > stock_inicial:
            # Se está agregando más cantidad → RESTAR del stock
            stock_bodega.stock -= (nueva_cantidad - stock_inicial)
            stock_bodega.stockDisponibleReal -= (nueva_cantidad - stock_inicial)
        elif nueva_cantidad < stock_inicial:
            # Se está quitando cantidad → SUMAR al stock
            stock_bodega.stock += (stock_inicial - nueva_cantidad)
            stock_bodega.stockDisponibleReal += (stock_inicial - nueva_cantidad)

        stock_bodega.save()

        # Actualizar el stock total del producto
        self.actualizar_stock_total(sku)


    def actualizar_stock_total(self, sku):
        """ Actualiza el stock total sumando los stocks de todas las bodegas del producto """
        stock_total = StockBodegasDB.objects.filter(idProducto__codigo=sku).aggregate(total=Sum('stock'))['total']
        
        if stock_total is None:
            stock_total = 0

        producto = ProductoDB.objects.filter(codigo=sku).first()
        if producto:
            producto.stockTotal = stock_total
            producto.save()
