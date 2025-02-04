from adapters.sl_client import APIClient
from datosLsApp.models import ProductoDB, StockBodegasDB, BodegaDB
from django.db.models import Sum


class ProductoRepository:
    def calculate_margen_descuentos(self, precio_venta, costo, rentabilidad_minima):
        """
        Calcula el margen bruto y el descuento máximo.
        
        Args:
            precio_venta (float): Precio de venta del producto.
            costo (float): Costo del producto.
            rentabilidad_minima (float): Rentabilidad mínima en porcentaje.

        Returns:
            tuple: Margen bruto y descuento máximo.
        """
        if precio_venta <= 0:
            print("Advertencia: El precio de venta debe ser mayor a 0.")
            return 0, 0
        
        precio_sin_iva = precio_venta / 1.19  # Calcular el precio sin IVA
        margen_bruto = (precio_sin_iva - costo) / precio_sin_iva
        descuento_maximo = margen_bruto - (rentabilidad_minima / 100)
        
        return margen_bruto, max(descuento_maximo, 0)  # Asegurar que no sea negativo

    def sync_products_and_stock(self, products):
        """
        Sincroniza los productos y su stock en bodegas.
        
        Args:
            products (list): Lista de diccionarios con datos de productos y su stock.
        """
        rentabilidad_minima = 50
        
        for product_data in products:
            producto_info = product_data.get("Producto", {}).get("Producto")
            if not producto_info or "codigo" not in producto_info:
                print(f"Advertencia: Producto inválido o sin código. Datos: {product_data}")
                continue

            precio_venta = next(
                (precio["precio"] for precio in product_data.get("Precios", []) if precio["priceList"] == 2),
                0.0,
            )
            costo = producto_info.get("costo", 0.0)

            margen_bruto, descuento_maximo = self.calculate_margen_descuentos(
                precio_venta, costo, rentabilidad_minima
            )

            producto, _ = ProductoDB.objects.update_or_create(
                codigo=producto_info["codigo"],
                defaults={
                    "nombre": producto_info.get("nombre", "Nombre no disponible"),
                    "marca": producto_info.get("marca", "Sin Marca"),
                    "costo": costo,
                    "precioLista": next(
                        (precio["precio"] for precio in product_data.get("Precios", []) if precio["priceList"] == 3),
                        0.0,
                    ),
                    "precioVenta": precio_venta,
                    "dsctoMaxTienda": descuento_maximo,
                    "dctoMaxProyectos": descuento_maximo,
                    "linkProducto": product_data.get("linkProducto", ""),
                },
            )
            print("******" * 100)
            
            print(f'TreeType: {producto_info.get("TreeType")},')
            print(f'producto:  {producto_info.get("nombre")},')
            
            # Si el producto es una receta, calcular stock y costo de receta
            if producto_info.get("TreeType") == "iSalesTree":
                print("Es una receta")
                stock_receta, costo_receta = self.calcular_stock_y_costo_receta(producto_info["codigo"])
                producto.stock_total = stock_receta
                print(f"Stock total receta xxx: {stock_receta}")
                producto.costo = costo_receta
                print(f"Costo total receta xxx: {costo_receta}")
                producto.save()
            else:
                if "Bodegas" in product_data:
                    self.sync_stock(producto, product_data["Bodegas"])
                    self.update_stock_total(producto)

        return True

    def calcular_stock_y_costo_receta(self, item_code):
        """Calcula el stock y costo total de una receta."""
        print(f"Calculando stock y costo de receta para {item_code}")

        ApiClientSL = APIClient()
        componentes = ApiClientSL.productTreesComponents(item_code).get("ProductTreeLines", [])
        bodegas = ["ME", "TR_ME", "PH", "TR_PH", "LC", "TR_LC"]
        
        stock_por_bodega = {bodega: float("inf") for bodega in bodegas}
        costo_total = 0.0
        
        for componente in componentes:
            item_code_componente = componente["ItemCode"]
            cantidad_necesaria = componente["Quantity"]
            stock_componente = self.obtener_stock_componente(item_code_componente)
            costo_componente = self.obtener_costo_componente(item_code_componente)
            
            for bodega in bodegas:
                stock_bodega = stock_componente.get(bodega, 0) // cantidad_necesaria
                stock_por_bodega[bodega] = min(stock_por_bodega[bodega], stock_bodega)
            
            costo_total += costo_componente * cantidad_necesaria
        
        stock_total_receta = min(stock_por_bodega.values())
        

        return stock_total_receta, costo_total

    def obtener_stock_componente(self, item_code):
        """Obtiene el stock de un componente desde la API."""
        ApiClientSL = APIClient()
        stock_data = ApiClientSL.urlPrueba(item_code)

        # Extraer correctamente la lista de almacenes
        warehouses = stock_data.get("ItemWarehouseInfoCollection", [])

        # Devolver un diccionario con el stock por bodega
        return {bodega["WarehouseCode"]: bodega["InStock"] for bodega in warehouses}


    def obtener_costo_componente(self, item_code):
        """Obtiene el costo promedio del componente desde la API."""
        ApiClientSL = APIClient()
        item_data = ApiClientSL.urlPrueba(item_code)
        return item_data.get("AvgStdPrice", 0.0)



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
            
            stockVentaDAto = bodega_data.get("stock_disponible", -1) - bodega_data.get("stock_comprometido", -1),
            
            stockVenta = stockVentaDAto[0]            
            

            # Sincronizar el stock de la bodega para este producto
            StockBodegasDB.objects.update_or_create(
                idProducto=producto,
                idBodega=bodega,
                defaults={
                    "stock": stockVenta,
                    "stockDisponibleReal": bodega_data.get("stock_disponible", -1),
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


    def descuentoMax(sku):
        """
        metodo para obtener el descuento maximo del producto
        """
        producto = ProductoDB.objects.get(codigo=sku)
        
        print(f"Descuento max {producto.dsctoMaxTienda}")
        return producto.dsctoMaxTienda
    
    def obtenerPrecioLista(sku):
        """
        metodo para obtener el precio de lista del producto
        """
        producto = ProductoDB.objects.get(codigo=sku)
        return producto.precioLista
    
    def obtenerImagenProducto(codigo):
        """
        metodo para obtener la imagen por medio del codigo del producto
        """
        
        producto = ProductoDB.objects.get(codigo=codigo)
        return producto.imagen
    
    def obtenerMarcaProducto(codigo):
        """
        metodo para obtener la marca por medio del codigo del producto
        """
        
        producto = ProductoDB.objects.get(codigo=codigo)
        return producto.marca

    
