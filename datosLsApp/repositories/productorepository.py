from datosLsApp.models import ProductoDB, StockBodegasDB, BodegaDB

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
                    "imagen": producto_info.get("imagen", ""),
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
                defaults={
                    "descripcion": bodega_data.get("descripcion", ""),
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
