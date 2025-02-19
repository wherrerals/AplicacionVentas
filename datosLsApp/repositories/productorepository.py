from django.db import connection
from adapters.sl_client import APIClient
from datosLsApp.models import ProductoDB, StockBodegasDB, BodegaDB
from django.db.models import Sum
import math
from django.db.models import Sum, F



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
                try:
                    print("PROCESANDO RECETA")
                    
                    # Calcular stock y costo de la receta
                    stock_receta, costo_receta = self.calcular_stock_y_costo_receta(producto_info["codigo"])
                    
                    # Asignar stock y costo al producto
                    producto.stockTotal = stock_receta
                    producto.costo = costo_receta
                    
                    print(f"datos de descuento maximo: {precio_venta}, {costo_receta}, {rentabilidad_minima}")
                    
                    margen_bruto, descuento_maximo = self.calculate_margen_descuentos(precio_venta, costo_receta, rentabilidad_minima)
                    
                    
                    producto.dsctoMaxTienda = descuento_maximo
                    producto.dctoMaxProyectos = descuento_maximo
                    producto.save()
                    
                except Exception as e:
                    print(f"Error al calcular stock y costo de receta: {e}")
            else:
                if "Bodegas" in product_data:
                    self.sync_stock(producto, product_data["Bodegas"])
                    self.update_stock_total(producto)

        return True


    def calcular_stock_y_costo_receta(self, item_code):
        """Calcula el stock total de la receta y el costo total."""
        
        ApiClientSL = APIClient()
        componentes = ApiClientSL.productTreesComponents(item_code).get("ProductTreeLines", [])

        bodegas = ["ME", "PH", "LC"]

        # Inicializamos el stock total por bodega con infinito
        stock_por_bodega = {bodega: float('inf') for bodega in bodegas}
        stock_total_receta = float('inf')
        costo_total = 0.0

        for componente in componentes:
            item_code_componente = componente["ItemCode"]
            cantidad_necesaria = componente["Quantity"]
            
            stock_componente = self.obtener_stock_componente(item_code_componente)            
            costo_componente = self.obtener_costo_componente(item_code_componente)

            # Calcular el total del stock del componente en todas sus bodegas
            stock_total_componente = sum(stock_componente.values())
            
            # Calcular stock disponible por la cantidad requerida
            stock_disponible_componente = math.floor(stock_total_componente / cantidad_necesaria) if cantidad_necesaria > 0 else 0
            
            # Actualizar el stock total de la receta (mínimo entre todos los componentes)
            stock_total_receta = min(stock_total_receta, stock_disponible_componente)

            # Calcular el stock de la receta por bodega
            for bodega in bodegas:
                stock_bodega = stock_componente.get(bodega, 0)
                stock_disponible = math.floor(stock_bodega / cantidad_necesaria) if cantidad_necesaria > 0 else 0
                
                # Actualizar el stock de la receta por bodega
                stock_por_bodega[bodega] = min(stock_por_bodega[bodega], stock_disponible)

            # Sumar el costo total de la receta
            costo_total += costo_componente * cantidad_necesaria

            # **Sincronizar stock del componente en las bodegas**
            print(f"Sincronizando stock de {item_code} en la base de datos")
            producto = ProductoDB.objects.get(codigo=item_code)  # Obtener la instancia del producto
            bodegas_datos = [{"nombre": bodega, "stock_disponible": stock_componente.get(bodega, 0) / cantidad_necesaria, "stock_comprometido": 0} for bodega in bodegas]
            print(f"bodegas_datos: {bodegas_datos}")
            self.sync_stock(producto, bodegas_datos)

        # Si stock_total_receta sigue siendo infinito, significa que no hay stock suficiente
        stock_total_receta = stock_total_receta if stock_total_receta != float('inf') else 0

        print(f"Stock total receta final: {stock_total_receta}")

        # **Actualizar el stock total del producto después de sincronizar**
        print("Actualizando stock total del producto en la base de datos")
        self.update_stock_total(producto)

        print("******" * 100)
        return stock_total_receta, costo_total



    def obtener_stock_componente(self, item_code):
        """Obtiene el stock disponible de un componente desde la API, filtrando por bodegas específicas."""
        ApiClientSL = APIClient()
        stock_data = ApiClientSL.urlPrueba(item_code)

        # Extraer correctamente la lista de almacenes
        warehouses = stock_data.get("ItemWarehouseInfoCollection", [])

        # Lista de bodegas permitidas
        bodegas_permitidas = {"ME", "PH", "LC"}

        # Filtrar y devolver un diccionario con el stock disponible (InStock - Committed)
        return {
            bodega["WarehouseCode"]: bodega["InStock"] - bodega.get("Committed", 0)
            for bodega in warehouses
            if bodega["WarehouseCode"] in bodegas_permitidas
        }
        

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
        
        print(f"Sincronizando stock de {producto.codigo} en la base de datos")
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

    @staticmethod
    def obtener_productos(filtro_nombre=None, filtro_codigo=None, offset=0, limite=20):
        producto_query = ProductoDB.objects.annotate(
            stock_total=Sum('stockbodegasdb__stock')
        ).values(
            'codigo', 'nombre', 'marca', 'costo', 'precioVenta', 'stockTotal', "dsctoMaxTienda", "dctoMaxProyectos", "precioLista"
        )

        if filtro_nombre:
            producto_query = producto_query.filter(nombre__icontains=filtro_nombre)
        if filtro_codigo:
            producto_query = producto_query.filter(codigo=filtro_codigo)
        
        producto_query = producto_query[offset:offset + limite]

        producto_lista = list(producto_query)

        for producto in producto_lista:
            bodegas = StockBodegasDB.objects.filter(idProducto__codigo=producto['codigo']).values(
                producto_codigo=F('idProducto__codigo'),
                id_Bodega=F('idBodega'),
                stock_V=F('stock')
            )
            producto['bodegas'] = list(bodegas)

        return producto_lista

    @staticmethod
    def obtener_total_productos(filtro_nombre=None, filtro_codigo=None):
        # Crear la consulta base
        query = """
            SELECT COUNT(*) as total
            FROM Producto
            WHERE 1=1
        """
        params = []

        # Agregar filtros si existen
        if filtro_nombre:
            query += " AND nombre LIKE %s"
            params.append(f"%{filtro_nombre}%")
        
        if filtro_codigo:
            query += " AND codigo LIKE %s"
            params.append(f"%{filtro_codigo}%")

        # Ejecutar la consulta
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result[0] if result else 0