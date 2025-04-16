

from adapters.sl_client import APIClient
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.productorepository import ProductoRepository
from logicaVentasApp.services.direccion import Direccion
from logicaVentasApp.services.typeofsale import TypeOfSale
from logicaVentasApp.services.vendedor import Seller


class SerializerDocument:

    @staticmethod
    def document_serializer(doc_data):

        if doc_data.get('DocEntry'):
            actualizar = True
            client = APIClient()
        else:
            actualizar = False
        
        type_sales = Seller.tipoVentaTipoVendedor(doc_data.get('SalesPersonCode'))
        
        if type_sales == 'NA':
            type_sales = TypeOfSale.Sale_type_line_type(doc_data.get('DocumentLines', []))
        
        type_sales = TypeOfSale.sale_type(type_sales, doc_data.get('TransportationCode'))
                    
        addres_bill, address_ship = Direccion.assign_bill_ship_addres(doc_data.get('Address'), doc_data.get('Address2'))
        
        cabecera = SerializerDocument.create_header(doc_data, doc_data.get('DocEntry'), type_sales)

        repo_producto = ProductoRepository()
        lineas_json = []

        for linea in doc_data.get('DocumentLines', []):
            item_code = linea.get('ItemCode')
            receta_line_num = linea.get('LineNum')  # Este es el LineNum base de la receta

            
            if repo_producto.es_receta(item_code):
                treeType = 'iSalesTree'
            else:
                treeType = 'iNotATree'
            
            warehouseCode = linea.get('WarehouseCode')

            nueva_linea = {
                'lineNum': receta_line_num,
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
            
            if actualizar and linea.get('DocEntry_line') != 'null':
                if repo_producto.es_receta(item_code):
                    componentes = client.productTreesComponents(item_code)
                    componente_line_num = int(receta_line_num) + 1


                    for componente in componentes.get('ProductTreeLines', [{}]):
                        lineas_json.append({
                            'lineNum': componente_line_num, # +1 
                            'ItemCode': componente['ItemCode'],
                            'TreeType': 'iIngredient'
                        })

                        componente_line_num += 1  # Incrementamos para el siguiente componente


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

        dic = {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }

        print(f"Json: {dic}")

        return {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }
    
    @staticmethod
    def create_header(doc_data, docentry, type_sales):

        print(f"DocEntry: {docentry}")

        if docentry is not None and docentry != '':
            cabecera = {
                'DocDate': doc_data.get('DocDate'),
                'DocDueDate': doc_data.get('DocDueDate'),
                'TaxDate': doc_data.get('TaxDate'),
                'DocTotal': doc_data.get('DocTotal'),
                'NumAtCard': doc_data.get('NumAtCard'),
                'Comments': doc_data.get('Comments'),
                'PaymentGroupCode': doc_data.get('PaymentGroupCode'),
                'SalesPersonCode': doc_data.get('SalesPersonCode'),
                'TransportationCode': doc_data.get('TransportationCode'),
                'U_LED_TIPVTA': type_sales,
                'U_LED_TIPDOC': doc_data.get('U_LED_TIPDOC'),
                'U_LED_FORENV': doc_data.get('TransportationCode'),
            }
        else:
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

        return cabecera