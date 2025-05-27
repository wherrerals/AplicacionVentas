

from adapters.sl_client import APIClient
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from logicaVentasApp.services.direccion import Direccion
from logicaVentasApp.services.typeofsale import TypeOfSale
from logicaVentasApp.services.vendedor import Seller


class SerializerDocument:

    @staticmethod
    def document_serializer(doc_data):
        
        type_sales = Seller.tipoVentaTipoVendedor(doc_data.get('SalesPersonCode'))
        
        if type_sales == 'NA':
            type_sales = TypeOfSale.Sale_type_line_type(doc_data.get('DocumentLines', []))
        
        type_sales = TypeOfSale.sale_type(type_sales, doc_data.get('TransportationCode'))

        branch_code = VendedorRepository.get_sucursal(doc_data.get('SalesPersonCode'))
                    
        addres_bill, address_ship = Direccion.assign_bill_ship_addres(doc_data.get('Address'), doc_data.get('Address2'), branch_code)
        print(type(addres_bill) )
        print(type(address_ship) )

        print(f"addres_bill {addres_bill}")
        print(f"address_ship {address_ship}")

        cabecera = {
            'DocDate': doc_data.get('DocDate'),
            'DocDueDate': doc_data.get('DocDueDate'),
            'TaxDate': doc_data.get('TaxDate'),
            'DocTotal': doc_data.get('DocTotal'),
            'CardCode': doc_data.get('CardCode'),
            'NumAtCard': doc_data.get('NumAtCard'),
            'Comments': doc_data.get('Comments'),
            'PaymentGroupCode': doc_data.get('PaymentGroupCode'),
            'SalesPersonCode': doc_data.get('SalesPersonCode'),
            'TransportationCode': doc_data.get('TransportationCode'),
            'U_LED_TIPVTA': type_sales,
            'U_LED_TIPDOC': doc_data.get('U_LED_TIPDOC'),
            'U_LED_FORENV': doc_data.get('TransportationCode'),
        }

        repo_producto = ProductoRepository()
        lineas_json = []

        for linea in doc_data.get('DocumentLines', []):
            item_code = linea.get('ItemCode')
            
            if repo_producto.es_receta(item_code):
                treeType = 'iSalesTree'
            else:
                treeType = 'iNotATree'
            
            warehouseCode = linea.get('WarehouseCode')

            nueva_linea = {
                'ItemCode': item_code,
                'Quantity': linea.get('Quantity'),
                'UnitPrice': repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')),
                'ShipDate': linea.get('ShipDate'),
                'FreeText': linea.get('FreeText'),
                'DiscountPercent': linea.get('DiscountPercent'),
                'WarehouseCode': warehouseCode,
                'CostingCode': linea.get('CostingCode'),
                'ShippingMethod': linea.get('ShippingMethod'),
                'COGSCostingCode': linea.get('COGSCostingCode'),
                'CostingCode2': linea.get('CostingCode2'),
                'TreeType': treeType
            }

            lineas_json.append(nueva_linea)
        # validar si es una lista o un class el tipo de addres_bill y address_ship
        if not isinstance(addres_bill, list) and not isinstance(address_ship, list):
            taxExtension = {
                "StreetS": addres_bill.calleNumero,
                "CityS": addres_bill.ciudad,
                "CountyS": f"{addres_bill.comuna.codigo} - {addres_bill.comuna.nombre}",
                "StateS": addres_bill.region.numero,
                "CountryS": "CL",
                "StreetB": address_ship.calleNumero,
                "CityB": address_ship.ciudad,
                "CountyB": f"{address_ship.comuna.codigo} - {address_ship.comuna.nombre}",
                "StateB": address_ship.region.numero,
                "CountryB": "CL",
            } 
        else:
            taxExtension = SerializerDocument.build_tax_extension(addres_bill, address_ship)
    
        return {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }

    def build_tax_extension(address_list):
        if not address_list or len(address_list) < 2:
            raise ValueError("Se requieren al menos dos direcciones para bill y ship")

        bill = address_list[0]
        ship = address_list[1]

        taxExtension = {
            "StreetS": bill['direccion'],
            "CityS": bill['ciudad'],
            "CountyS": bill['comuna'],  # Aquí puedes añadir nombre si lo tienes
            "StateS": bill['region'],
            "CountryS": "CL",
            "StreetB": ship['direccion'],
            "CityB": ship['ciudad'],
            "CountyB": ship['comuna'],
            "StateB": ship['region'],
            "CountryB": "CL",
        }

        return taxExtension

    @staticmethod
    def build_tax_extension(addres_bill, address_ship):

            bill = addres_bill[0]
            ship = address_ship[0]

            return {
                "StreetS": bill.get('direccion', ''),
                "CityS": bill.get('ciudad', ''),
                "CountyS": bill.get('comuna', ''),
                "StateS": bill.get('region', ''),
                "CountryS": bill.get('pais', 'CL'),
                "StreetB": ship.get('direccion', ''),
                "CityB": ship.get('ciudad', ''),
                "CountyB": ship.get('comuna', ''),
                "StateB": ship.get('region', ''),
                "CountryB": ship.get('pais', 'CL'),
            }



    @staticmethod
    def serialize_recipe_ingredients(document_lines, type_document):
        lines = document_lines.get("value", [])

        print(f"lines {lines}")
        result = {"DocumentLines": []}

        # Ordenar por LineNum
        parsed_lines = [line.get(f"{type_document}/DocumentLines", {}) for line in lines]

        current_warehouse = None
        current_line_num = None

        for line in parsed_lines:
            tree_type = line.get("TreeType")
            warehouse = line.get("WarehouseCode")
            item_code = line.get("ItemCode")
            line_num = line.get("LineNum")

            if tree_type == "S":
                # Guardar la bodega actual para futuras líneas I
                current_warehouse = warehouse
                current_line_num = line_num

                result["DocumentLines"].append({
                    "LineNum": line_num,
                    "ItemCode": item_code,
                    "WarehouseCode": current_warehouse,
                    "TreeType": "iSalesTree"
                })

            elif tree_type == "I" and current_warehouse is not None:
                # Usar la bodega asociada a la última línea S
                result["DocumentLines"].append({
                    "LineNum": line_num,
                    "ItemCode": item_code,
                    "WarehouseCode": current_warehouse,
                    "TreeType": "iIngredient"
                })

            # Si es "N" o sin TreeType válido, ignorar

        return result

""" 
    @staticmethod
    def serialize_recipe_ingredients(document_lines, type_document):
        lines = document_lines.get("value", [])
        result = {"DocumentLines": []}

        # Ordenar por LineNum
        parsed_lines = [line.get(f"{type_document}/DocumentLines", {}) for line in lines]


        current_recipe = None

        for line in parsed_lines:
            tree_type = line.get("TreeType")
            warehouse = line.get("WarehouseCode")

            if tree_type == "S":
                # Nueva receta activa
                current_recipe = {
                    "LineNum": line["LineNum"],
                    "ItemCode": line["ItemCode"],
                    "WarehouseCode": warehouse,
                    "TreeType": "iSalesTree"
                }
                result["DocumentLines"].append(current_recipe)

            elif tree_type == "I" and current_recipe:
                # Ingrediente válido para la receta activa
                result["DocumentLines"].append({
                    "LineNum": line["LineNum"],
                    "ItemCode": line["ItemCode"],
                    "WarehouseCode": current_recipe["WarehouseCode"],
                    "TreeType": "iIngredient"
                })

            # TreeType == "N" o sin receta activa: ignorar

        return result """
