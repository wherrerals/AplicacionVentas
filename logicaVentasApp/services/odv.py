import json
import math
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
from datosLsApp.models.stockbodegasdb import StockBodegasDB
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.repositories.stockbodegasrepository import StockBodegasRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from logicaVentasApp.services.documento import Documento
import logging

from logicaVentasApp.services.stcokService import StockService
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
        print(name_mayus)
        name_minus = name.lower() if name else None
        print(name_minus)
        name_title = name.title() if name else None
        print(name_title)

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
        print(f"JSON_DATA: {json_data}")      

        client_info = json_data["Client"]["value"][0]
        quotations = client_info.get("Orders", {})
        salesperson = client_info.get("SalesPersons", {})
        contact_employee = client_info.get("BusinessPartners/ContactEmployees", {})
        vendedor_repo = VendedorRepository()
        tipo_vendedor = vendedor_repo.obtenerTipoVendedor(salesperson.get("SalesEmployeeCode"))
        print(f"TIPO VENDEDOR: {tipo_vendedor}")

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
            document_lines.append(document_line)

        # Formar el diccionario final
        resultado = {
            "Cliente": cliente,
            "DocumentLines": document_lines
        }

        print(f"RESULTADO_cotizacion: {document_lines}")
        return resultado

    # En odv.py - Método actualizado para manejar múltiples líneas del mismo SKU/bodega
    def actualizarDocumento(self, docnum, docentry, data):

        print(f"DATA: {data}")

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
                print(f"Stock inicial total para {sku} en bodega {bodega_id}: {cantidad_total} (DB: {stock_actual})")

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
                    
                    print(f"Nueva línea: SKU {sku} en bodega {bodega_id} con cantidad {nueva_cantidad_total}")
                    # Restar del stock disponible (es una nueva venta)
                    stock_service.actualizar_stock_por_diferencia(sku, bodega_id, -nueva_cantidad_total, stock_actual)
                elif diferencia != 0:  # Si hay un cambio en la cantidad total
                    stock_actual = stock_service.get_initial_stock(sku, bodega_id)
                    print(f"Cambio en línea existente: SKU {sku} en bodega {bodega_id}, diferencia {diferencia}")
                    # Si diferencia es positiva: se está pidiendo más, debemos restar al stock
                    # Si diferencia es negativa: se está pidiendo menos, debemos sumar al stock
                    stock_service.actualizar_stock_por_diferencia(sku, bodega_id, -diferencia, stock_actual)

            # Verificar líneas eliminadas: devolver el stock a las bodegas
            for (sku, bodega_id), cantidad_anterior_total in stock_anterior.items():
                if (sku, bodega_id) not in stock_nuevo:
                    print(f"SKU {sku} en bodega {bodega_id} fue eliminado, devolviendo {cantidad_anterior_total} unidades al stock.")
                    stock_actual = stock_service.get_initial_stock(sku, bodega_id)
                    
                    # Como el producto fue eliminado, devolvemos la cantidad al stock (sumamos)
                    stock_service.actualizar_stock_por_diferencia(sku, bodega_id, cantidad_anterior_total, stock_actual)

            # Preparar JSON y actualizar documento en SAP
            jsonData = self.prepararJsonODV(data)
            client = APIClient()
            response = client.actualizarODVSL(int(docentry), jsonData)

            # Verificar respuesta de la API
            if response.get('success'):
                return {
                    'success': 'Orden Venta actualizada exitosamente',
                    'docNum': docnum,
                    'docEntry': docentry
                }

        except Exception as e:
            logger.error(f"Error al actualizar la cotización: {str(e)}")
            return {'error': str(e)}



    def crearDocumento(self, data):

        try:

            print(f"DATA: {data}")
            
            errores = self.validarDatosODV(data)
            
            if errores:
                return {'error': errores}


            stock_service = StockService()
            sl = APIClient()

            
            stock_inicial = []  # Para rollback en caso de error

            for item in data['DocumentLines']:
                sku = item['ItemCode']
                bodega_id = item['WarehouseCode']
                cantidad = item['Quantity']

                # Capturar el stock inicial antes de descontarlo
                stock_actual = StockBodegasDB.objects.filter(idProducto__codigo=sku, idBodega=bodega_id).values_list('stock', flat=True).first() or 0

                stock_inicial.append((sku, bodega_id, stock_actual))  # Guardar para rollback

                # Descontar stock
                stock_service.actualizar_stock(sku, bodega_id, -cantidad, stock_actual)

            # Preparar el JSON para la cotización
            jsonData = self.prepararJsonODV(data)

            print(f"previo a la creacion de la cotizacion")

            # Realizar la solicitud a la API
            response = sl.crearODV(jsonData)

            print(f"RESPONSE: {response}")
            
            if isinstance(response, dict):
                if 'DocEntry' in response:
                    doc_num = response.get('DocNum')
                    doc_entry = response.get('DocEntry')
                    salesPersonCode = response.get('SalesPersonCode')
                    name_vendedor = VendedorRepository.obtenerNombreVendedor(salesPersonCode)
                    return {
                        'success': 'Orden Venta creada exitosamente',
                        'docNum': doc_num,
                        'docEntry': doc_entry,
                        'salesPersonCode': salesPersonCode,
                        'salesPersonName': name_vendedor
                    }
                elif 'error' in response:
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

            

    def validarDatosODV(self, data):
        """
        Verifica que los datos de la cotización sean correctos.

        Args:
            data (dict): Datos de la cotización.

        Returns:
            str: Mensajes de error si hay problemas con los datos, o vacío si son correctos.
        """
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
        """
        Verifica que el stock total del código en la cotización no supere el stock disponible en bodega.
        """
        print("Validando stock total por bodega...")

        stock_validado = {}  # Almacena el stock disponible en bodega
        suma_por_clave = {}  # Almacena la suma total de cada (SKU, Bodega)
        errores = []

        # Primera pasada: sumar las cantidades por (SKU, Bodega)
        for linea in data.get("DocumentLines", []):
            item_code = linea["ItemCode"]
            warehouse_code = linea["WarehouseCode"]
            quantity = linea["Quantity"]
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

                print(f"Stock en bodega {warehouse_code} para {item_code}: {stock_en_bodega}")
                stock_validado[(item_code, warehouse_code)] = stock_en_bodega

            # Validar si la cantidad total supera el stock disponible
            if total_quantity > stock_validado[(item_code, warehouse_code)]:
                errores.append(f"El total solicitado del producto {item_code} en la bodega {warehouse_code} supera el stock disponible ({stock_validado[(item_code, warehouse_code)]} unidades).")

        return errores if errores else "Stock validado correctamente."


            


    
    def prepararJsonODV(self, jsonData):

        codigo_vendedor = jsonData.get('SalesPersonCode')
        tipo_venta = self.tipoVentaTipoVendedor(codigo_vendedor)
        
        if tipo_venta == 'NA':
            lineas = jsonData.get('DocumentLines', [])
            tipo_venta = self.tipoVentaTipoLineas(lineas)
            
            
        adrres = jsonData.get('Address')
        adrres2 = jsonData.get('Address2')
        
        idContacto = jsonData.get('ContactPersonCode')
        
        if idContacto == "No hay contactos disponibles":
            numerocontactoSAp = "null"
        else:
            contacto = ContactoRepository.obtenerContacto(idContacto)
            numerocontactoSAp = contacto.codigoInternoSap   
        
        direccion1 = DireccionRepository.obtenerDireccion(adrres)
        direccionRepo2 = DireccionRepository.obtenerDireccion(adrres2)
        
        addresmodif = f"{direccion1.calleNumero} {direccion1.comuna.nombre}\n{direccion1.ciudad}\n{direccion1.region.nombre}"
        addresmodif2 = f"{direccionRepo2.calleNumero} {direccionRepo2.comuna.nombre}\n{direccionRepo2.ciudad}\n{direccionRepo2.region.nombre}"


        
        # Datos de la cabecera
        cabecera = {
            'DocDate': jsonData.get('DocDate'),
            'DocDueDate': jsonData.get('DocDueDate'),
            'TaxDate': jsonData.get('TaxDate'),
            'DocTotal': jsonData.get('DocTotal'),
            #'ContactPersonCode': numerocontactoSAp,
            'Address': addresmodif,
            'Address2': addresmodif2,
            'CardCode': jsonData.get('CardCode'),
            'NumAtCard': jsonData.get('NumAtCard'),
            'Comments': jsonData.get('Comments'),
            'PaymentGroupCode': jsonData.get('PaymentGroupCode'),
            'SalesPersonCode': jsonData.get('SalesPersonCode'),
            'TransportationCode': jsonData.get('TransportationCode'),
            #'U_LED_NROPSH': jsonData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': tipo_venta,
            'U_LED_TIPDOC': jsonData.get('U_LED_TIPDOC'),
            'U_LED_FORENV': jsonData.get('TransportationCode'),
        }

        # Datos de las líneas
        lineas = jsonData.get('DocumentLines', [])

        repo_producto = ProductoRepository()

        
        #lineas = self.ajustarShippingMethod(lineas)
        lineas_json = [
            {
                'lineNum': linea.get('LineNum'),
                'ItemCode': linea.get('ItemCode'),
                'Quantity': linea.get('Quantity'),
                'UnitPrice': repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')),
                'ShipDate': linea.get('ShipDate'),
                'FreeText': linea.get('FreeText'),
                'DiscountPercent': linea.get('DiscountPercent'),
                'WarehouseCode': linea.get('WarehouseCode'),
                'CostingCode': linea.get('CostingCode'),
                'ShippingMethod': linea.get('ShippingMethod'),
                'COGSCostingCode': linea.get('COGSCostingCode'),
                'CostingCode2': linea.get('CostingCode2'),
                'COGSCostingCode2': linea.get('COGSCostingCode2'),
            }
            for linea in lineas
        ]

        dic = {
            **cabecera,
            'DocumentLines': lineas_json,
        }

        print(dic)

        return {
            **cabecera,
            'DocumentLines': lineas_json,
        }

    @staticmethod
    def tipoVentaTipoVendedor(codigo_vendedor):
        """
        Asigna el tipo de venta a la cotización.

        Args:
            tipo_venta (str): Tipo de venta.
        """
        
        repo = VendedorRepository()
        tipo_vendedor = repo.obtenerTipoVendedor(codigo_vendedor)

        if tipo_vendedor == 'PR':
            return 'PROY'
        elif tipo_vendedor == 'CD':
            return 'ECCO'
        else:
            return 'NA'
    

    @staticmethod
    def tipoVentaTipoLineas(lineas):
        """
        Asigna el tipo de venta a las líneas de la cotización.

        - Si todas las lineas son del mismo warehouse, se asigna el tipo de venta: TIEN.
        - Si las lineas son de diferentes warehouses, se asigna el tipo de venta: RESE.

        Args:
            lineas (list): Líneas de la cotización.
        """
        
        shipping_methods = set(linea.get('ShippingMethod') for linea in lineas)
        warehouses = set(linea.get('WarehouseCode') for linea in lineas)
        
        if len(shipping_methods) and len(warehouses) == 1:
            return 'TIEN'
        else:
            return 'RESE'
""" 
    @staticmethod
    def ajustarShippingMethod(lineas):

        for linea in lineas:
            shipping_method = linea.get('ShippingMethod')
            warehouse_code = linea.get('WarehouseCode')

            # Regla para ShippingMethod
            if shipping_method == "2":
                if warehouse_code == "LC":
                    linea['ShippingMethod'] = "3"
                elif warehouse_code == "ME":
                    linea['ShippingMethod'] = "2"
                elif warehouse_code == "PH":
                    linea['ShippingMethod'] = "4"

        return lineas """