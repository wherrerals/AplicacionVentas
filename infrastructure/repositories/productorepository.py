from django.db import connection
from adapters.sl_client import APIClient
from infrastructure.models import ProductoDB, StockBodegasDB, BodegaDB
from django.db.models import Sum
import math
from django.db.models import Sum, F

from infrastructure.repositories.stockbodegasrepository import StockBodegasRepository




class ProductoRepository:
    def calculate_margen_descuentos(self, precio_venta, costo, rentabilidad_minima):

        if precio_venta <= 0 or costo <= 0:
            return 0, 0
        else:
            precio_sin_iva = precio_venta / 1.19  # Calcular el precio sin IVA
            margen_bruto = (precio_sin_iva - costo) / precio_sin_iva
            descuento_maximo = margen_bruto - (rentabilidad_minima / 100)
            return margen_bruto, max(descuento_maximo, 0)  # Asegurar que no sea negativo

    def sync_products_and_stock(self, products):

        rentabilidad_minima = 50
        productos_procesados = []
        
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
                    "linkProducto": product_data.get("linkProducto", "NO_DISPONIBLE"),
                    "descontinuado": producto_info.get("descontinuado", "0"),
                    "inactivo": producto_info.get("inactivo", ""),
                    "TreeType": producto_info.get("TreeType", ""),
                },
            )

            # Si el producto es una receta, calcular stock y costo de receta
            if producto_info.get("TreeType") == "iSalesTree":

                try:                    
                    # Calcular stock y costo de la receta
                    stock_receta, costo_receta = self.calcular_stock_y_costo_receta(producto_info["codigo"])
                    
                    # Asignar stock y costo al producto
                    producto.stockTotal = stock_receta
                    producto.costo = costo_receta
                    
                    
                    margen_bruto, descuento_maximo = self.calculate_margen_descuentos(precio_venta, costo_receta, rentabilidad_minima)
                    
                    StockBodegasRepository().calcular_stock_real_bodegas(producto_info["codigo"])

                    
                    producto.dsctoMaxTienda = descuento_maximo
                    producto.dctoMaxProyectos = descuento_maximo
                    producto.save()
                    
                except Exception as e:
                    print(f"Error al calcular stock y costo de receta: {e}")
            else:
                if "Bodegas" in product_data:
                    self.sync_stock(producto, product_data["Bodegas"])
                    self.update_stock_total(producto)
                    StockBodegasRepository().calcular_stock_real_bodegas(producto_info["codigo"])

            productos_procesados.append(producto.codigo)

        return True, productos_procesados
    

    def calcular_stock_y_costo_receta(self, item_code):
        """Calcula el stock total de la receta y el costo total."""
        # Obtenemos los componentes de la receta desde la API
        
        ApiClientSL = APIClient()
        componentes = ApiClientSL.productTreesComponents(item_code).get("ProductTreeLines", [])

        # Definimos las bodegas específicas
        bodegas = list(self.get_bodegas_permitidas())

        # Inicializamos el stock total por bodega con infinito
        stock_por_bodega = {bodega: float('inf') for bodega in bodegas}
        stock_total_receta = float('inf')
        costo_total = 0.0

        # Iteramos sobre los componentes de la receta
        # y calculamos el stock y costo total
        for componente in componentes:
            item_code_componente = componente["ItemCode"]
            cantidad_necesaria = componente["Quantity"]
            
            stock_componente = self.obtener_stock_componentes_db_receta(item_code_componente)        
            costo_componente = self.obtener_costo_componente_db(item_code_componente)

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
                
                # Actualizar el stock por bodega (mínimo entre todos los componentes)
                stock_por_bodega[bodega] = min(stock_por_bodega[bodega], stock_disponible)

                print(f"Componente {item_code_componente} Bodega {bodega} Stock Componente: {stock_bodega} Cantidad Necesaria: {cantidad_necesaria} Stock Disponible Receta en Bodega: {stock_disponible}")

            # Sumar el costo total de la receta
            costo_total += costo_componente * cantidad_necesaria

            # **Sincronizar stock del componente en las bodegas**
            producto = ProductoDB.objects.get(codigo=item_code)  # Obtener la instancia del producto
            bodegas_datos = [{"nombre": bodega, "stock_disponible": stock_por_bodega[bodega], "stock_comprometido": 0} for bodega in bodegas]

            #print(f"datos de producto antes de sincronizar el stocl {producto.codigo} bodegas {bodegas_datos}")
            self.sync_stock(producto, bodegas_datos)


        stock_total_receta = stock_total_receta if stock_total_receta != float('inf') else 0

        self.update_stock_total(producto)

        return stock_total_receta, costo_total
    

    def get_bodegas_permitidas(self):
        return {p.nombre for p in BodegaDB.objects.filter(estado=True)}



    def obtener_stock_componente(self, item_code):

        ApiClientSL = APIClient()
        stock_data = ApiClientSL.urlPrueba(item_code)

        # Extraer correctamente la lista de almacenes
        warehouses = stock_data.get("ItemWarehouseInfoCollection", [])

        # Lista de bodegas permitidas
        bodegas_permitidas = self.get_bodegas_permitidas()

        # Filtrar y devolver un diccionario con el stock disponible (InStock - Committed)
        return {
            bodega["WarehouseCode"]: bodega["InStock"] - bodega.get("Committed", 0)
            for bodega in warehouses
            if bodega["WarehouseCode"] in bodegas_permitidas
        }
    
    
    def obtener_stock_componentes_db_receta(self, item_code):
        # Lista de bodegas permitidas (usando los nombres como están en la BD)
        bodegas_permitidas = self.get_bodegas_permitidas()
        
        # Obtener los registros de stock para el producto
        stocks = StockBodegasDB.objects.filter(
            idProducto__codigo=item_code,
            idBodega__nombre__in=bodegas_permitidas
        ).values("idBodega__nombre", "stock_disponible_real")
        
        # Crear el diccionario en el mismo formato que el otro método
        return {
            stock["idBodega__nombre"]: stock["stock_disponible_real"]
            for stock in stocks
        }

    def obtener_costo_componente(self, item_code):

        ApiClientSL = APIClient()
        item_data = ApiClientSL.urlPrueba(item_code)
        return item_data.get("AvgStdPrice", 0.0)

    def obtener_costo_componente_db(self, item_code):
        try:
            producto = ProductoDB.objects.get(codigo=item_code)
            return producto.costo
        except ProductoDB.DoesNotExist:
            return 0.0

    def sync_stock(self, producto, bodegas):

        for bodega_data in bodegas:

            # Validar que la bodega tenga el nombre requerido
            if "nombre" not in bodega_data:
                print(f"Advertencia: Bodega sin nombre. Datos: {bodega_data}")
                continue  # Saltar esta bodega

            # Obtener la instancia de la bodega asegurando que el nombre no tenga espacios extras
            try:
                bodega = BodegaDB.objects.get(nombre=bodega_data["nombre"].strip())
            except BodegaDB.DoesNotExist:
                print(f"Error: No se encontró la bodega con nombre '{bodega_data['nombre']}'")
                continue  # Saltar esta bodega si no existe

            # Corregir el cálculo de stockVenta (asegurarnos de obtener un entero)
            stockVenta = bodega_data.get("stock_disponible", -1) - bodega_data.get("stock_comprometido", -1)

            """
            
            if stockVenta < 0:
                stockVenta = 0  # Asegurarse de que el stock no sea negativo
            """


            # Buscar el registro de stock correctamente
            try:
                stock_bodega = StockBodegasDB.objects.get(idProducto=producto, idBodega=bodega)
                # Si existe, actualizamos los valores
                stock_bodega.stock_disponible = stockVenta
                stock_bodega.stock_fisico = bodega_data.get("stock_disponible", -1)
                stock_bodega.stock_comprometido = bodega_data.get("stock_comprometido", -1)

                #pendiente stock disponible real
                
                # Guardar los cambios
                stock_bodega.save()
            except StockBodegasDB.DoesNotExist:
                # Si no existe, creamos un nuevo registro
                StockBodegasDB.objects.create(
                    idProducto=producto,
                    idBodega=bodega,
                    stock_disponible=stockVenta,
                    stock_fisico=bodega_data.get("stock_disponible", -1),
                    stock_comprometido=bodega_data.get("stock_comprometido", -1)
                )


    def update_stock_total(self, producto):

        stock_total = StockBodegasDB.objects.filter(idProducto=producto).aggregate(
            total_stock=Sum('stock_disponible')
        )['total_stock'] or 0

        # Actualizar el campo stockTotal en el producto
        producto.stockTotal = stock_total
        producto.save()


    def descuentoMax(sku):

        producto = ProductoDB.objects.get(codigo=sku)
        
        return producto.dsctoMaxTienda
    
    def obtenerPrecioLista(sku):

        producto = ProductoDB.objects.get(codigo=sku)
        return producto.precioLista
    
    def obtenerPrecioVenta(sku):
        
        producto = ProductoDB.objects.get(codigo=sku)
        return producto.precioVenta

    def obtenerImagenProducto(codigo):
        
        producto = ProductoDB.objects.get(codigo=codigo)
        return producto.imagen
    
    def obtenerMarcaProducto(codigo):
        
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
            producto_query = producto_query.filter(codigo__icontains=filtro_codigo)
        
        producto_query = producto_query[offset:offset + limite]

        producto_lista = list(producto_query)

        for producto in producto_lista:
            bodegas = StockBodegasDB.objects.filter(idProducto__codigo=producto['codigo']).values(
                producto_codigo=F('idProducto__codigo'),
                id_Bodega=F('idBodega'),
                stock_V=F('stock_disponible_real')
            )

            #limitar descuentos
            producto_obj = ProductoDB.objects.get(codigo=producto['codigo'])
            dsctoMaxTienda, dctoMaxProyectos = ProductoRepository().limitar_descuento(producto_obj)
            producto['dsctoMaxTienda'] = dsctoMaxTienda
            producto['dctoMaxProyectos'] = dctoMaxProyectos

            producto['bodegas'] = list(bodegas)

        return producto_lista
    

    def limitar_descuento(self, producto):
        """
        Calcula los límites de descuento para un producto en tienda y en proyectos.

        :param producto: objeto con atributos marca, dsctoMaxTienda y dctoMaxProyectos
        :return: (dsctoMaxTienda, dsctoMaxProyectos)
        """

        from infrastructure.models.confiDescuentosDB import ConfiDescuentosDB

        # Mapear códigos según vendedor y marca
        mapping = {
            ("T", "LST"): "1",
            ("T", "OTHER"): "3",
            ("P", "LST"): "2",
            ("P", "OTHER"): "4",
        }

        marca_key = "LST" if producto.marca == "LST" else "OTHER"

        # Obtener límites desde DB (si no existe, usar 0)
        try:
            confi_t = ConfiDescuentosDB.objects.get(codigo=mapping[("T", marca_key)])
            limite_t = (confi_t.limiteDescuentoMaximo or 0) / 100
        except ConfiDescuentosDB.DoesNotExist:
            limite_t = 0

        try:
            confi_p = ConfiDescuentosDB.objects.get(codigo=mapping[("P", marca_key)])
            limite_p = (confi_p.limiteDescuentoMaximo or 0) / 100
        except ConfiDescuentosDB.DoesNotExist:
            limite_p = 0

        # Descuentos del producto (si no existen, 0.0)
        descuento_max_tienda = producto.dsctoMaxTienda or 0.0
        descuento_max_proy = producto.dctoMaxProyectos or 0.0

        # Aplicar límites en escala 0–1
        dscto_max_tienda = min(descuento_max_tienda, limite_t)
        dscto_max_proyectos = min(descuento_max_proy, limite_p)

        return dscto_max_tienda, dscto_max_proyectos

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
        
    def obtener_precio_unitario_neto(self, sku):

        producto = ProductoDB.objects.get(codigo=sku)
        precioventaunitario = producto.precioVenta
        return round(precioventaunitario / 1.19, 4)
        #return precioventaunitario

    def obtener_precio_unitario_bruto(self, sku):

        producto = ProductoDB.objects.get(codigo=sku)
        precioventaunitario = producto.precioVenta
        return precioventaunitario

    def es_receta(self, item_code):

        try:
            producto = ProductoDB.objects.get(codigo=item_code)
            return producto.TreeType == "iSalesTree"
        
        except ProductoDB.DoesNotExist:
            return False