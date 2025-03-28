from adapters.serializador import Serializador
from adapters.sl_client import APIClient
from datosLsApp.repositories.productorepository import ProductoRepository
from taskApp.models import SyncState
from django.db import transaction
import math
import pika


class Producto:

    def sync(self, tipo):
        # Obtener el valor de `skip` desde la base de datos
        state, created = SyncState.objects.get_or_create(
            key=f'product_sync_skip_{tipo}', 
            defaults={'value': 0}
        )
        
        # Inicializar el valor de `skip` si es la primera vez
        skip = state.value
        total_synced = 0

        # Inicializar el contador de intentos vacíos
        empty_count = 0

        sync_method = {
            "nacional": {
                "count": lambda cliente, tipo: cliente.contarProductos(tipo=tipo),
                "sync": lambda cliente, skip, tipo: cliente.obtenerProductosSL(skip=skip, tipo=tipo)
            },
            "receta": {
                "count": lambda cliente, tipo: cliente.contarProductos(tipo=tipo),
                "sync": lambda cliente, skip, tipo: cliente.obtenerProductosSL(skip=skip, tipo=tipo)
            },
            "importado": {
                "count": lambda cliente, tipo: cliente.contarProductos(tipo=tipo),
                "sync": lambda cliente, skip, tipo: cliente.obtenerProductosSL(skip=skip, tipo=tipo)
            }
        }

        # Crear instancia de APIClient
        cliente = APIClient()

        # Contar productos
        conteo = sync_method[tipo]["count"](cliente, tipo)

        # Verificar si el conteo es válido
        if not isinstance(conteo, dict) or 'value' not in conteo or not conteo['value']:
            raise ValueError(f"El conteo de productos no es válido en {tipo}")

        total_items = conteo['value'][0].get('ItemsCount', 0)

        # Verificar si `skip` ha alcanzado el total y reiniciar si es necesario
        if skip >= total_items:
            skip = 0
            state.value = 0
            state.save()

        # Obtener los productos
        productos = sync_method[tipo]["sync"](cliente, skip, tipo)

        # Verificar si no hay productos para sincronizar
        if not productos:
            empty_count += 1
            if empty_count >= 3:
                state.value = 0
                state.save()
                empty_count = 0
            return f"No hay productos para sincronizar en {tipo}"
    
        # Serializar los productos
        serialcer = Serializador('json')
        jsonserializado = serialcer.formatearDatos(productos)
        
        # Sincronizar los productos y su stock
        repo = ProductoRepository()
        creacion, listadoProductos = repo.sync_products_and_stock(jsonserializado)


        # Incrementar el valor de `skip` si la sincronización fue exitosa
        if creacion and listadoProductos:
            #synced_count = len(jsonserializado)
            synced_count = len(listadoProductos)
            total_synced += synced_count
            
            # Actualizar el valor de `skip` para la próxima llamada
            state.value += synced_count
            state.save()

            empty_count = 0  # Resetear el contador de intentos vacíos

        # Retornar el mensaje con la cantidad de productos sincronizados
        return f"{total_synced} productos sincronizados exitosamente{listadoProductos} para el tipo {tipo}"

    
    def obtenerReceta(self, codigo):
        cliente = APIClient()
        receta = cliente.productTree(codigo)

        item_codes = []  # Lista para almacenar los ItemCodes y sus cantidades
        datos_receta = []  # Lista para almacenar los datos serializados de cada item

        # Recorremos las líneas del árbol de productos
        for item in receta.get("ProductTreeLines", []):
            item_code = item.get("ItemCode")
            item_name = item.get("ItemName")
            quantity = item.get("Quantity")


            if item_code:  # Si ItemCode existe, lo agregamos a la lista
                item_codes.append((item_code, quantity))  # Guardamos ItemCode y Quantity como tupla

        # Ahora, llamamos a elementosRecetas para cada ItemCode en item_codes
        for item_code, quantity in item_codes:
            # Llamamos al método elementosReceta para cada ItemCode
            detalles_item = cliente.elementosReceta(item_code)

            # Serializamos los detalles del item
            serializador = Serializador('json')
            json_serializado = serializador.formatearDatosReceta(detalles_item)

            # Armamos los datos para cada item
            data = {
                "name": item_name,
                "codigo": codigo,
                "ItemCode": item_code,
                "Quantity": quantity,
                "detalles": json_serializado,
            }

            datos_receta.append(data)  # Agregamos los datos del item a la lista

            # Imprimimos los datos del producto obtenido

        return datos_receta  # Devolvemos la lista con todos los datos serializados


    @staticmethod
    def calcularStockReceta(data):
        # Diccionario para almacenar la receta unificada
        receta_unificada = {}

        for item in data:
            # Extraemos la información del ítem
            item_code = item["ItemCode"]
            cantidad = item["Quantity"]
            bodegas = item["detalles"][0]["Bodegas"]
            producto_nombre = item["detalles"][0]["Producto"]["Producto"]["nombre"]
            codigo_receta = item["codigo"]

            # Inicializamos el campo si no existe
            if codigo_receta not in receta_unificada:
                receta_unificada[codigo_receta] = {
                    "codigo": codigo_receta,
                    "name": producto_nombre,
                    "Stock Total Receta": float('inf'),  # Lo inicializamos con un valor muy alto
                    "Bodegas": []  # Inicializamos la lista de bodegas vacía
                }

            # Definimos las bodegas relevantes
            bodegas_relevantes = ["ME", "LC", "PH"]
            stock_por_bodega = {
                "ME": {"stock_disponible": 0, "stock_comprometido": 0},
                "LC": {"stock_disponible": 0, "stock_comprometido": 0},
                "PH": {"stock_disponible": 0, "stock_comprometido": 0}
            }
            stocks_totales = []

            # Calcular el stock por cada bodega relevante
            for bodega in bodegas:
                nombre_bodega = bodega["nombre"]
                stock_disponible = bodega["stock_disponible"]
                stock_comprometido = bodega["stock_comprometido"]

                if nombre_bodega in bodegas_relevantes:
                    # Calculamos el stock disponible dividido por la cantidad y redondeamos hacia abajo
                    stock_total = math.floor(stock_disponible / cantidad)
                    stock_por_bodega[nombre_bodega]["stock_disponible"] = stock_total
                    stock_por_bodega[nombre_bodega]["stock_comprometido"] = stock_comprometido
                    stocks_totales.append(stock_total)

            # El stock total de la receta es el valor mínimo de los stocks calculados
            stock_total_receta = min(stocks_totales) if stocks_totales else 0

            # Actualizamos el stock total de la receta
            receta_unificada[codigo_receta]["Stock Total Receta"] = min(
                receta_unificada[codigo_receta]["Stock Total Receta"], stock_total_receta)

            # Agregamos las bodegas con sus respectivos valores
            for bodega in bodegas_relevantes:
                receta_unificada[codigo_receta]["Bodegas"].append({
                    "nombre": bodega,
                    "stock_disponible": stock_por_bodega[bodega]["stock_disponible"],
                    "stock_comprometido": stock_por_bodega[bodega]["stock_comprometido"]
                })

        # Devolvemos la receta unificada
        return list(receta_unificada.values())


    def reporteProductos(data):

        """
        Construye los filtros para la consulta de cotizaciones basados en los datos proporcionados.

        Args:
            data (dict): Datos de la consulta.

        Returns:
            dict: Filtros para la consulta de cotizaciones.
        """

        filters = {}

        if data.get('fecha_doc'):
            filters['Quotations/DocDate ge'] = str(f"'{data.get('fecha_doc')}'")
            filters['Quotations/DocDate le'] = str(f"'{data.get('fecha_doc')}'")
        if data.get('fecha_inicio'):
            filters['Quotations/DocDate ge'] = str(f"'{data.get('fecha_inicio')}'")
        if data.get('fecha_fin'):
            filters['Quotations/DocDate le'] = str(f"'{data.get('fecha_fin')}'")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Quotations/DocNum,'] = f"{docum})"

        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(Quotations/CardCode,'] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['contains(Quotations/CardName,'] = f"'{car_data}')"

        if data.get('salesEmployeeName'):
            numecode = int(data.get('salesEmployeeName'))
            filters['contains(SalesPersons/SalesEmployeeCode,'] = f"{numecode})" 
        
        #if data.get('DocumentStatus'):
        #   filters['Quotations/DocumentStatus eq'] = f"'{data.get('DocumentStatus')}'"

        #if data.get('cancelled'):
        #    filters['Quotations/Cancelled eq'] = f"'{data.get('cancelled')}'"

        if data.get('DocumentStatus'):
            document_status = data.get('DocumentStatus')

            if document_status == 'O':
                filters['Quotations/DocumentStatus eq'] = "'O'"
            elif document_status == 'C':
                filters['Quotations/DocumentStatus eq'] = "'C'"
                filters['Quotations/Cancelled eq'] = "'N'"
                
            else:
                filters['Quotations/Cancelled eq'] = "'Y'"

        if data.get('docTotal'):
            docTotal = float(data.get('docTotal'))
            filters['Quotations/DocTotal eq'] = f"{docTotal}"


        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters
