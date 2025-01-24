from datosLsApp.models import ProductoDB, StockBodegasDB, BodegaDB
from django.db.models import Sum


class ProductoRepository:
    def sync_products_and_stock(self, products):
        """
        Sincroniza los productos y su stock en bodegas.
        
        Args:
            products (list): Lista de diccionarios con datos de productos y su stock.
        """
        for product_data in products:
            # Acceder al producto correctamente
            producto_info = product_data.get("Producto", {}).get("Producto")
            if not producto_info or "codigo" not in producto_info:
                print(f"Advertencia: Producto inválido o sin código. Datos: {product_data}")
                continue  # Saltar este producto

            # Sincronizar ProductoDB
            producto, _ = ProductoDB.objects.update_or_create(
                codigo=producto_info["codigo"],
                defaults={
                    "nombre": producto_info.get("nombre", "Nombre no disponible"),
                    "marca": producto_info.get("marca", "Sin Marca"),
                    "costo": producto_info.get("costo", 0.0),
                    "precioLista": next(
                        (precio["precio"] for precio in product_data.get("Precios", []) if precio["priceList"] == 1),
                        0.0,
                    ),
                    "precioVenta": next(
                        (precio["precio"] for precio in product_data.get("Precios", []) if precio["priceList"] == 2),
                        0.0,
                    ),
                    "dsctoMaxTienda": product_data.get("dsctoMaxTienda", 0.0),
                    "dctoMaxProyectos": product_data.get("dctoMaxProyectos", 0.0),
                    "linkProducto": product_data.get("linkProducto", ""),
                },
            )

            # Sincronizar bodegas y stock
            if "Bodegas" in product_data:
                self.sync_stock(producto, product_data["Bodegas"])

                # Calcular y actualizar el stock total del producto
                self.update_stock_total(producto)

        return True

    def sync_stock(self, producto, bodegas):
        """
        Sincroniza la información de stock para un producto en las bodegas.

        Args:
            producto (ProductoDB): Instancia del producto.
            bodegas (list): Lista de diccionarios con datos de las bodegas y su stock.
        """
        for bodega_data in bodegas:
            # Validar que la bodega tenga el nombre requerido
            if "nombre" not in bodega_data:
                print(f"Advertencia: Bodega sin nombre. Datos: {bodega_data}")
                continue  # Saltar esta bodega

            # Sincronizar o crear la bodega
            bodega, _ = BodegaDB.objects.update_or_create(
                nombre=bodega_data["nombre"],
                codigo=bodega_data["nombre"],
                defaults={
                    "descripcion": bodega_data.get("nombre", ""),
                },
            )

            # Sincronizar el stock de la bodega para este producto
            StockBodegasDB.objects.update_or_create(
                idProducto=producto,
                idBodega=bodega,
                defaults={
                    "stock": bodega_data.get("stock_disponible", -1),
                    "stockDisponibleReal": bodega_data.get("stock_comprometido", -1),
                },
            )

    def update_stock_total(self, producto):
        """
        Calcula y actualiza el stock total del producto sumando el stock disponible en las bodegas.

        Args:
            producto (ProductoDB): Instancia del producto.
        """
        stock_total = StockBodegasDB.objects.filter(idProducto=producto).aggregate(
            total_stock=Sum('stock')
        )['total_stock'] or 0

        # Actualizar el campo stockTotal en el producto
        producto.stockTotal = stock_total
        producto.save()


    def descuentoMax():
        pass