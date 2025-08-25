import json
import math
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
from infrastructure.models.stockbodegasdb import StockBodegasDB
from infrastructure.repositories.contactorepository import ContactoRepository
from infrastructure.repositories.direccionrepository import DireccionRepository
from infrastructure.repositories.productorepository import ProductoRepository
from infrastructure.repositories.stockbodegasrepository import StockBodegasRepository
from infrastructure.repositories.vendedorRepository import VendedorRepository
from infrastructure.serializer.documentSerializer import SerializerDocument
from domain.services.documento import Documento
import logging

from domain.services.stcokService import StockService
from logs.services.documentlog import DocumentsLogs
from taskApp.tasks import update_components_task
logger = logging.getLogger(__name__)

class OrdenVenta(Documento):


    def construirFiltrosODV(data):

        """
        Construye los filtros para la consulta de cotizaciones basados en los datos proporcionados.

        Args:
            data (dict): Datos de la consulta.

        Returns:
            dict: Filtros para la consulta de cotizaciones.
        """


        filters = {}

        name = data.get('carData')
        name_mayus = name.upper() if name else None
        name_minus = name.lower() if name else None
        name_title = name.title() if name else None

        if data.get('fecha_doc'):
            filters['Orders/DocDate ge'] = str(f"'{data.get('fecha_doc')}'")
            filters['Orders/DocDate le'] = str(f"'{data.get('fecha_doc')}'")
        if data.get('fecha_inicio'):
            filters['Orders/DocDate ge'] = str(f"'{data.get('fecha_inicio')}'")
        if data.get('fecha_fin'):
            filters['Orders/DocDate le'] = str(f"'{data.get('fecha_fin')}'")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Orders/DocNum,'] = f"{docum})"

        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(Orders/CardCode,'] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['(contains(Orders/CardName,'] = f"'{name_mayus}') or contains(Orders/CardName, '{name_minus}') or contains(Orders/CardName, '{name_title}'))"

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
                filters['Orders/DocumentStatus eq'] = "'O'"
            elif document_status == 'C':
                filters['Orders/DocumentStatus eq'] = "'C'"
                filters['Orders/Cancelled eq'] = "'N'"
                
            else:
                filters['Orders/Cancelled eq'] = "'Y'"

        if data.get('docTotal'):
            docTotal = float(data.get('docTotal'))
            filters['Orders/DocTotal eq'] = f"{docTotal}"


        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters

    def formatearDatos(self, json_data):
        # Extraer y limpiar la información del cliente  

        client_info = json_data["Client"]["value"][0]
        quotations = client_info.get("Orders", {})
        salesperson = client_info.get("SalesPersons", {})
        contact_employee = client_info.get("BusinessPartners/ContactEmployees", {})
        vendedor_repo = VendedorRepository()
        tipo_vendedor = vendedor_repo.obtenerTipoVendedor(salesperson.get("SalesEmployeeCode"))

        # Formatear los datos de cliente
        cliente = {
            "Orders": {
                "DocEntry": quotations.get("DocEntry"),
                "DocNum": quotations.get("DocNum"),
                "CardCode": quotations.get("CardCode"),
                "CardName": quotations.get("CardName"),
                "TransportationCode": quotations.get("TransportationCode"),
                "Address": quotations.get("Address"),
                "Address2": quotations.get("Address2"),
                "DocDate": quotations.get("DocDate"),
                "DocDueDate": quotations.get("DocDueDate"),
                "Comments": quotations.get("Comments") if quotations.get("Comments") else "",
                "DocumentStatus": quotations.get("DocumentStatus"),
                "Cancelled": quotations.get("Cancelled"),
                "U_LED_COD_CUPON": quotations.get("U_LED_COD_CUPON"),
                "U_LED_TIPVTA": quotations.get("U_LED_TIPVTA"),
                "U_LED_TIPDOC": quotations.get("U_LED_TIPDOC"),
                "U_LED_NROPSH": quotations.get("U_LED_NROPSH"),
                "NumAtCard": quotations.get("NumAtCard"),
                "VatSum": quotations.get("VatSum"),
                "DocTotal": quotations.get("DocTotal"),
                "DocTotalNeto": quotations.get("DocTotalNeto"),
            },
            "SalesPersons": {
                "SalesEmployeeCode": salesperson.get("SalesEmployeeCode"),
                "SalesEmployeeName": salesperson.get("SalesEmployeeName"),
                "U_LED_SUCURS": salesperson.get("U_LED_SUCURS"),
            },
            "ContactEmployee": {
                "InternalCode": contact_employee.get("InternalCode"),
                "FirstName": contact_employee.get("FirstName"),
            }
        }

        # Extraer y limpiar la información de líneas de documento
        document_lines = []
        for line_info in json_data["DocumentLine"]["value"]:
            line = line_info.get("Orders/DocumentLines", {})
            warehouse_info = line_info.get("Items/ItemWarehouseInfoCollection", {})
            
            sku = line.get("ItemCode")
            
            imagen = ProductoRepository.obtenerImagenProducto(sku)
            bodega = line.get("WarehouseCode")

            imagen = ProductoRepository.obtenerImagenProducto(sku)
            marca = ProductoRepository.obtenerMarcaProducto(sku)
            descuentoMax = ProductoRepository.descuentoMax(sku)
            priceList = ProductoRepository.obtenerPrecioLista(sku)

            stock_bodega = StockBodegasRepository.consultarStockPorBodega(sku, bodega)

            if tipo_vendedor == 'P':
                if marca == "LST":
                    descuentoMax =  math.floor(min(descuentoMax * 100, 25))
                else:
                    descuentoMax = math.floor(min(descuentoMax * 100, 15))
            else:
                if marca == "LST":
                    descuentoMax = math.floor(min(descuentoMax * 100, 15))
                else:
                    descuentoMax = math.floor(min(descuentoMax * 100, 10))

            data_cupon = line.get("U_LED_DCTO_CUPON")
            if data_cupon:
                if data_cupon == None:
                    data_cupon = 0
                elif data_cupon != "":
                    data_cupon = data_cupon.replace("%", "")
                    data_cupon = int(data_cupon)

            document_line = {
                "DocEntry": line.get("DocEntry"),
                "LineNum": line.get("LineNum"),
                "imagen": imagen,
                "ItemCode": line.get("ItemCode"),
                "ItemDescription": line.get("ItemDescription"),
                "WarehouseCode": line.get("WarehouseCode"),
                "Quantity": line.get("Quantity"),
                "UnitPrice": line.get("UnitPrice"),
                "GrossPrice": line.get("GrossPrice"),
                "DiscountPercent": line.get("DiscountPercent"),
                "Price": line.get("Price"),
                "PriceAfterVAT": line.get("PriceAfterVAT"),
                "LineTotal": line.get("LineTotal"),
                "GrossTotal": line.get("GrossTotal"),
                "ShipDate": str(line.get("ShipDate")),
                "Address": line.get("Address"),
                "ShippingMethod": line.get("ShippingMethod"),
                "FreeText": line.get("FreeText"),
                "U_LED_DCTO_CUPON": data_cupon,
                "BaseType": line.get("BaseType"),
                "GrossBuyPrice": line.get("GrossBuyPrice"),
                "BaseEntry": line.get("BaseEntry"),
                "BaseLine": line.get("BaseLine"),
                "LineStatus": line.get("LineStatus"),
                "DescuentoMax": descuentoMax,
                "PriceList": priceList,
                "StockBodega": stock_bodega,
                "WarehouseInfo": {
                    "WarehouseCode": warehouse_info.get("WarehouseCode"),
                    "InStock": warehouse_info.get("InStock"),
                    "Committed": warehouse_info.get("Committed"),
                    "SalesStock": warehouse_info.get("SalesStock"),
                }
            }

            if document_line["Price"] and document_line["Price"] > 0:
                document_lines.append(document_line)
        
        # Formar el diccionario final
        resultado = {
            "Cliente": cliente,
            "DocumentLines": document_lines
        }

        return resultado

    # En odv.py - Método actualizado para manejar múltiples líneas del mismo SKU/bodega
    def actualizarDocumento(self, docnum, docentry, data):

        try:


            errores = self.validarDatosODV(data)
            
            if errores:
                return {'error': errores}

            stock_service = StockService()
            apiClient = APIClient()

            # Obtener líneas del documento antes de actualizar stock
            documents_lines = apiClient.detallesOrdenVentaLineas(docentry) 

            # Almacenar el stock inicial por SKU y bodega, sumando todas las cantidades
            stock_anterior = {}
            # Almacenar cada línea individual para identificar líneas eliminadas específicas
            lineas_anteriores = []

            # Capturar el stock inicial de cada producto antes de hacer cambios
            for item in documents_lines.get('value', []):  
                document_line = item.get('Orders/DocumentLines', {})  
                if document_line:
                    sku = document_line.get('ItemCode')
                    bodega_id = document_line.get('WarehouseCode')
                    cantidad_anterior = document_line.get('Quantity')
                    linea_id = document_line.get('LineNum')  # Identificador único de línea

                    # Guardar cada línea individual para comparación posterior
                    lineas_anteriores.append({
                        'sku': sku,
                        'bodega_id': bodega_id,
                        'cantidad': cantidad_anterior,
                        'linea_id': linea_id
                    })

                    # Sumar cantidades para el mismo par (sku, bodega_id)
                    key = (sku, bodega_id)
                    if key in stock_anterior:
                        stock_anterior[key] += cantidad_anterior
                    else:
                        stock_anterior[key] = cantidad_anterior

            # Obtener el stock actual de cada bodega
            for (sku, bodega_id), cantidad_total in stock_anterior.items():
                stock_actual = StockBodegasDB.objects.filter(
                    idProducto__codigo=sku, idBodega=bodega_id
                ).values_list('stock', flat=True).first() or 0
                
                # Capturar el stock actual en memoria para referencia
                stock_service.capture_initial_stock(sku, bodega_id, stock_actual)

            # Procesar las nuevas líneas y calcular diferencias
            stock_nuevo = {}
            lineas_nuevas = []

            # Primero, agrupar las nuevas líneas por (sku, bodega_id) y sumar cantidades
            for idx, item in enumerate(data['DocumentLines']):
                sku = item['ItemCode']
                bodega_id = item['WarehouseCode']
                nueva_cantidad = item['Quantity']
                linea_id = item.get('LineNum', idx)  # Usar LineNum si existe, si no, usar el índice

                # Guardar cada línea individual
                lineas_nuevas.append({
                    'sku': sku,
                    'bodega_id': bodega_id,
                    'cantidad': nueva_cantidad,
                    'linea_id': linea_id
                })

                # Sumar cantidades para el mismo par (sku, bodega_id)
                key = (sku, bodega_id)
                if key in stock_nuevo:
                    stock_nuevo[key] += nueva_cantidad
                else:
                    stock_nuevo[key] = nueva_cantidad

            # Ahora procesar las diferencias por par (sku, bodega_id)
            for (sku, bodega_id), nueva_cantidad_total in stock_nuevo.items():
                # Obtener la cantidad anterior total (si existía)
                cantidad_anterior_total = stock_anterior.get((sku, bodega_id), 0)
                
                # Calcular la diferencia neta entre totales
                diferencia = nueva_cantidad_total - cantidad_anterior_total
                
                # Si es una línea nueva (no existía antes), verificamos si es negativa
                if (sku, bodega_id) not in stock_anterior and nueva_cantidad_total > 0:
                    # Es una línea nueva con valor positivo
                    stock_actual = stock_service.get_initial_stock(sku, bodega_id)
                    if stock_actual == 0:  # Si no teníamos registro previo, buscar en la DB
                        stock_actual = StockBodegasDB.objects.filter(
                            idProducto__codigo=sku, idBodega=bodega_id
                        ).values_list('stock', flat=True).first() or 0
                        stock_service.capture_initial_stock(sku, bodega_id, stock_actual)
                    
                    # Restar del stock disponible (es una nueva venta)
                    stock_service.actualizar_stock_por_diferencia(sku, bodega_id, -nueva_cantidad_total, stock_actual)
                elif diferencia != 0:  # Si hay un cambio en la cantidad total
                    stock_actual = stock_service.get_initial_stock(sku, bodega_id)
                    # Si diferencia es positiva: se está pidiendo más, debemos restar al stock
                    # Si diferencia es negativa: se está pidiendo menos, debemos sumar al stock
                    stock_service.actualizar_stock_por_diferencia(sku, bodega_id, -diferencia, stock_actual)

            # Verificar líneas eliminadas: devolver el stock a las bodegas
            for (sku, bodega_id), cantidad_anterior_total in stock_anterior.items():
                if (sku, bodega_id) not in stock_nuevo:
                    stock_actual = stock_service.get_initial_stock(sku, bodega_id)
                    
                    # Como el producto fue eliminado, devolvemos la cantidad al stock (sumamos)
                    stock_service.actualizar_stock_por_diferencia(sku, bodega_id, cantidad_anterior_total, stock_actual)

            # Preparar JSON y actualizar documento en SAP
            jsonData = SerializerDocument.document_serializer(data)
            client = APIClient()

            #hay_receta = any(item.get('TreeType') == 'iSalesTree' for item in jsonData.get('DocumentLines', []))

            #if hay_receta:
            json_data = SerializerDocument.document_serializer(data)
            json_sin_linea_uno = json_data

            if json_sin_linea_uno['DocumentLines']:
                json_sin_linea_uno['DocumentLines'].clear()
                json_sin_linea_uno['DocumentLines'] = [{
                
                        "ItemCode": "LM",
                        "Quantity": 1,
                        "UnitPrice": 0,
                        "TreeType": "iNotATree"
                }]

                response = client.actualizarODVSL(docentry, json_sin_linea_uno)

            response = client.actualizarODVSL(int(docentry), jsonData)

            # Verificar respuesta de la API
            if response.get('success'):
                doc_num = docnum
                doc_entry = docentry
                # Guardar el log de la cotización
                rise = self.update_components(jsonData, doc_entry, type_document='Orders')
                DocumentsLogs.register_logs(docNum=doc_num, docEntry=doc_entry, tipoDoc='ODV', url="", json=jsonData, response=response, estate='Update')

                return {
                    'success': 'Orden Venta actualizada exitosamente',
                    'docNum': docnum,
                    'docEntry': docentry
                }

        except Exception as e:
            DocumentsLogs.register_logs(docNum=docnum, docEntry=docentry, tipoDoc='ODV', url="", json=jsonData, response=response, estate='UpdateError')
            logger.error(f"Error al actualizar la cotización: {str(e)}")
            return {'error': str(e)}



    def crearDocumento(self, data):

        try:
            
            errores = self.validarDatosODV(data)
            
            if errores:
                return {'error': errores}

            stock_service = StockService()
            sl = APIClient()
            stock_inicial = [] 

            for item in data['DocumentLines']:
                sku = item['ItemCode']
                bodega_id = item['WarehouseCode']
                cantidad = item['Quantity']

                stock_actual = StockBodegasDB.objects.filter(idProducto__codigo=sku, idBodega=bodega_id).values_list('stock', flat=True).first() or 0 # Capturar el stock inicial antes de descontarl
                stock_inicial.append((sku, bodega_id, stock_actual))  # Guardar para rollback
                stock_service.actualizar_stock(sku, bodega_id, -cantidad, stock_actual) # Descontar stock

            jsonData = SerializerDocument.document_serializer(data) # Preparar el JSON para la cotización
            response = sl.crearODV(jsonData)

            descento_porcentaje = response.get('DiscountPercent', 0)
            print ("descento_porcentaje", descento_porcentaje)

            # validar si el descuento es un porcentaje válido

            if descento_porcentaje < 0 or descento_porcentaje > 100:
                print("Descuento no válido")
            
            if isinstance(response, dict):

                if 'DocEntry' in response:
                    doc_num = response.get('DocNum')
                    doc_entry = response.get('DocEntry')
                    salesPersonCode = response.get('SalesPersonCode')
                    name_vendedor = VendedorRepository.obtenerNombreVendedor(salesPersonCode)

                    self.update_components(response, doc_entry, type_document='Orders')
                    DocumentsLogs.register_logs(docNum=doc_num, docEntry=doc_entry, tipoDoc='ODV', url="", json=jsonData, response=response, estate='Creado')

                    return {
                        'success': 'Orden Venta creada exitosamente',
                        'docNum': doc_num,
                        'docEntry': doc_entry,
                        'salesPersonCode': salesPersonCode,
                        'salesPersonName': name_vendedor
                    }
                
                elif 'error' in response:
                    DocumentsLogs.register_logs(docNum=None, docEntry=None, tipoDoc='ODV', url="", json=jsonData, response=response, estate='Error')
                    return {'error': f"Error: {response.get('error', 'Error desconocido')}"}
                else:
                    return {'error': 'Respuesta inesperada de la API.'}
            else:
                return {'error': 'La respuesta de la API no es válida.'}

        except Exception as e:
            logger.error(f"Error al crear la cotización: {str(e)}")
            # Rollback del stock si algo falla
            for sku, bodega_id, stock_original in stock_inicial:
                StockBodegasDB.objects.filter(idProducto__codigo=sku, idBodega=bodega_id).update(stock=stock_original)

            return {'error': str(e)}

    def update_components(self, data, doc_entry, type_document):
        document_line = data.get('DocumentLines')

        if 'TreeType' in document_line[0]:
            print("Enviando tarea para actualizar componentes...")
            try:
                return update_components_task.delay(doc_entry, type_document)
            except Exception as e:
                logger.error(f"Error al encolar la tarea de actualización de componentes: {str(e)}")
            

    def validarDatosODV(self, data):
        errores = []

        # Verificar que el cardcode esté presente
        if not data.get('CardCode'):
            errores.append("No se a ingresado cliente para la Cotizacion.")

        if not data.get('DocumentLines'):
            errores.append("La cotización debe tener al menos una línea de documento.")

        # Verificar que la cantidad sea válida (mayor que cero)
        for item in data.get('DocumentLines', []):
            cantidad = item.get('Quantity', 0)
            if cantidad <= 0:
                errores.append(f"La cantidad del artículo {item.get('ItemCode')} debe ser mayor a cero.")

        # Verificar que otros campos importantes estén presentes (esto depende de los campos requeridos)
        if not data.get('DocDate'):
            errores.append("La fecha del documento es obligatoria.")

        if not data.get('DocDueDate'):
            errores.append("La fecha de vencimiento es obligatoria.")
    
        if not errores:
            resultado_stock = self.validar_stock_total_por_bodega(data)
            if isinstance(resultado_stock, list):  # Si hay errores de stock
                errores.extend(resultado_stock)

        # Si hay errores, retornarlos como una cadena
        return ' '.join(errores)

    @staticmethod
    def validar_stock_total_por_bodega(data):

        doc_entry = data.get("DocEntry")

        stock_validado = {}  # Almacena el stock disponible en bodega
        suma_por_clave = {}  # Almacena la suma total de cada (SKU, Bodega)
        errores = []

        # Primera pasada: sumar las cantidades por (SKU, Bodega)
        for linea in data.get("DocumentLines", []):
            
            item_code = linea["ItemCode"]
            if item_code.startswith("SV") or item_code.startswith("L"):
                continue  # Salta a la siguiente iteración sin procesar este producto


            warehouse_code = linea["WarehouseCode"]
            quantity = linea["Quantity"]

            cantidad_inicial_sap = int(linea.get("CantidadInicialSAP", 0))  # Obtener CantidadInicialSAP, si no existe, es 0
            clave = (item_code, warehouse_code)

            # Acumular la cantidad de productos solicitados por (SKU, Bodega)
            suma_por_clave[clave] = suma_por_clave.get(clave, 0) + quantity

        # Segunda pasada: validar stock
        for (item_code, warehouse_code), total_quantity in suma_por_clave.items():
            # Obtener stock disponible en bodega si no está en el diccionario de stock_validado
            if (item_code, warehouse_code) not in stock_validado:
                stock_en_bodega = StockBodegasDB.objects.filter(
                    idProducto__codigo=item_code, idBodega=warehouse_code
                ).values_list("stock", flat=True).first() or 0

                # Ajustar stock disponible si DocEntry tiene un valor
                if doc_entry:  
                    stock_en_bodega += cantidad_inicial_sap

                stock_validado[(item_code, warehouse_code)] = stock_en_bodega

            # Validar si la cantidad total supera el stock disponible (ajustado)
            if total_quantity > stock_validado[(item_code, warehouse_code)]:
                errores.append(
                    f"El total solicitado del producto {item_code} en la bodega {warehouse_code} supera el stock disponible ({stock_validado[(item_code, warehouse_code)]} unidades)."
                )

        return errores if errores else "Stock validado correctamente."

    
    @staticmethod
    def tipoVentaTipoVendedor(codigo_vendedor):
        
        repo = VendedorRepository()
        tipo_vendedor = repo.obtenerTipoVendedor(codigo_vendedor)

        if tipo_vendedor == 'PR':
            return 'PROY'
        elif tipo_vendedor == 'CD':
            return 'ECCO'
        else:
            return 'NA'
    

    @staticmethod
    def Sale_type_line_type(lineas):
        
        shipping_methods = set(linea.get('ShippingMethod') for linea in lineas)
        warehouses = set(linea.get('WarehouseCode') for linea in lineas)
        
        if len(shipping_methods) and len(warehouses) == 1:
            return 'TIEN'
        else:
            return 'RESE'