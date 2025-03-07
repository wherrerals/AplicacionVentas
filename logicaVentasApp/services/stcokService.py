from django.db import transaction
from django.db.models import Sum
from datosLsApp.models.productodb import ProductoDB
from datosLsApp.models.stockbodegasdb import StockBodegasDB



class StockService:
    
    def __init__(self):
        self.initial_stock = {}

    def capture_initial_stock(self, sku, bodega_id, cantidad):
        """ Guarda el stock inicial antes de cualquier cambio """
        print(f"Capturando stock inicial para SKU {sku} en Bodega {bodega_id}: {cantidad}")
        key = f"{sku}-{bodega_id}"
        self.initial_stock[key] = cantidad

    def get_initial_stock(self, sku, bodega_id):
        """ Obtiene el stock inicial de memoria """
        key = f"{sku}-{bodega_id}"
        return self.initial_stock.get(key, 0)
    
    @transaction.atomic
    def actualizar_stock(self, sku, bodega_id, nueva_cantidad, stock_actual):
        """
        Actualiza el stock de una bodega específica y el stock total del producto.
        """
        print(f"Actualizando stock para SKU {sku} en Bodega {bodega_id} | Nueva Cantidad: {nueva_cantidad} (stock actual: {stock_actual})")
        stock_bodega = StockBodegasDB.objects.select_for_update().filter(idProducto__codigo=sku, idBodega=bodega_id).first()

        # Determinar si se está agregando o quitando stock
        stock_bodega.stock = nueva_cantidad + stock_actual

        stock_bodega.save()

        # Actualizar el stock total del producto
        self.actualizar_stock_total(sku)

    @transaction.atomic
    def actualizar_stock_por_diferencia(self, sku, bodega_id, ajuste, stock_actual):
        """
        Actualiza el stock basado en el ajuste necesario.
        - Si ajuste es positivo: se suma al stock
        - Si ajuste es negativo: se resta del stock
        """
        print(f"Ajustando stock para SKU {sku} en Bodega {bodega_id} | Ajuste: {ajuste} (stock actual: {stock_actual})")
        
        # Verificar si el registro existe
        stock_bodega = StockBodegasDB.objects.select_for_update().filter(
            idProducto__codigo=sku, idBodega=bodega_id
        ).first()

        if stock_bodega:
            # Aplicar el ajuste al stock actual (no reemplazar)
            nuevo_stock = stock_actual + ajuste
            stock_bodega.stock = nuevo_stock
            print(f"Nuevo stock para SKU {sku} en Bodega {bodega_id}: {nuevo_stock}")
            stock_bodega.save()

            # Actualizar el stock total del producto
            self.actualizar_stock_total(sku)
            return nuevo_stock
        else:
            # Si no existe el registro, crearlo si es necesario
            try:
                producto = ProductoDB.objects.get(codigo=sku)
                print(f"Creando nuevo registro de stock para SKU {sku} en Bodega {bodega_id}")
                
                # Para una nueva línea, el stock inicial debería ser 0 + el ajuste
                nuevo_stock = ajuste  # Esto podría ser negativo si estamos restando stock
                
                # Si el ajuste es negativo (resta stock), verificar que tenga sentido
                if ajuste < 0:
                    print(f"ADVERTENCIA: Creando stock inicial negativo ({ajuste}) para SKU {sku} en Bodega {bodega_id}")
                
                nuevo_stock_bodega = StockBodegasDB.objects.create(
                    idProducto=producto,
                    idBodega=bodega_id,
                    stock=nuevo_stock
                )
                nuevo_stock_bodega.save()
                
                # Actualizar el stock total del producto
                self.actualizar_stock_total(sku)
                return nuevo_stock
            except ProductoDB.DoesNotExist:
                print(f"Error: No existe el producto con SKU {sku}")
                return stock_actual

    def actualizar_stock_total(self, sku):
        """ Actualiza el stock total sumando los stocks de todas las bodegas del producto """
        print(f"Actualizando stock total para SKU {sku}")
        stock_total = StockBodegasDB.objects.filter(idProducto__codigo=sku).aggregate(total=Sum('stock'))['total'] or 0

        producto = ProductoDB.objects.filter(codigo=sku).first()
        if producto:
            producto.stockTotal = stock_total
            producto.save()