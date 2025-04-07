

from adapters.sl_client import APIClient
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.productorepository import ProductoRepository


class SerializerDocument:

    def document_serializer(self, documentData):
        """
        Prepara los datos JSON específicos de la cotización.

        Args:
            documentData (dict): Datos de la cotización.
        
        Returns:
            dict: Datos de la cotización preparados para ser enviados a SAP.
        """
        
        codigo_vendedor = documentData.get('SalesPersonCode')
        tipo_venta = self.tipoVentaTipoVendedor(codigo_vendedor)
        
        # Si el tipo de venta por vendedor no es válido ('NA'), determinar por líneas
        if tipo_venta == 'NA':
            lineas = documentData.get('DocumentLines', [])
            tipo_venta = self.tipoVentaTipoLineas(lineas)
        
        transportationCode = documentData.get('TransportationCode')

        if tipo_venta == 'NA' and transportationCode != '1':
            tipo_venta = 'RESE'
        elif tipo_venta == 'PROY':
            tipo_venta = 'PROY'
        elif tipo_venta == 'ECCO':
            tipo_venta = 'ECCO'
                    
        adrres = documentData.get('Address')
        adrres2 = documentData.get('Address2')
        
        idContacto = documentData.get('ContactPersonCode')
        
        if idContacto == "No hay contactos disponibles":
            numerocontactoSAp = "null"
        else:
            contacto = ContactoRepository.obtenerContacto(idContacto)
            numerocontactoSAp = contacto.codigoInternoSap        #consultar en base de datos con el id capturado
        
        if adrres == "No hay direcciones disponibles":
            direccion1 = DireccionRepository.obtenerDireccion(adrres)
        else:
            direccion1 = DireccionRepository.obtenerDireccion(adrres2)

        if adrres2 == "No hay direcciones disponibles":
            direccionRepo2 = DireccionRepository.obtenerDireccion(adrres2)
        else:
            direccionRepo2 = DireccionRepository.obtenerDireccion(adrres)
        
        # Datos de la cabecera
        cabecera = {
            'DocDate': documentData.get('DocDate'),
            'DocDueDate': documentData.get('DocDueDate'),
            'TaxDate': documentData.get('TaxDate'),
            'DocTotal': documentData.get('DocTotal'),
            #'ContactPersonCode': numerocontactoSAp,
            #'Address': addresmodif,
            #'Address2': addresmodif2,
            'CardCode': documentData.get('CardCode'),
            'NumAtCard': documentData.get('NumAtCard'),
            'Comments': documentData.get('Comments'),
            'PaymentGroupCode': documentData.get('PaymentGroupCode'),
            'SalesPersonCode': documentData.get('SalesPersonCode'),
            'TransportationCode': documentData.get('TransportationCode'),
            #'U_LED_NROPSH': documentData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': tipo_venta,  # Tipo de venta calculado
            'U_LED_TIPDOC': documentData.get('U_LED_TIPDOC'),
            'U_LED_FORENV': documentData.get('TransportationCode'),
        }

        # Datos de las líneas
        lineas = documentData.get('DocumentLines', [])

        repo_producto = ProductoRepository()
        
        #maper item code
        lineas_json = []


        for linea in lineas:
            item_code = linea.get('ItemCode')
            
            if repo_producto.es_receta(item_code):
                treeType = 'iSalesTree'
            else:
                treeType = 'iNotATree'
            
            # Obtener lineNum, pero solo usarlo si es un número válido
            #line_num_str = linea.get('LineNum')
            #line_num = int(line_num_str) if line_num_str and line_num_str.isdigit() else None  # Dejarlo como None si no es válido
            line_num = 0
            warehouseCode = linea.get('WarehouseCode')

            nueva_linea = {
                #'lineNum': line_num,  # Se mantiene como None si no hay un valor válido
                'TreeType': treeType,
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
                'COGSCostingCode2': linea.get('COGSCostingCode2'),
            }

            lineas_json.append(nueva_linea)

        taxExtension = {
            "StreetS": direccion1.calleNumero,
            "CityS": direccion1.ciudad,
            "CountyS": f"{direccion1.comuna.codigo} - {direccion1.comuna.nombre}",
            "StateS": direccion1.region.numero,
            "CountryS": "CL",
            "StreetB": direccionRepo2.calleNumero,
            "CityB": direccionRepo2.ciudad,
            "CountyB": f"{direccionRepo2.comuna.codigo} - {direccionRepo2.comuna.nombre}",
            "StateB": direccionRepo2.region.numero,
            "CountryB": "CL",
        } 
    
        dic = {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }

        print(f"dic: {dic}")

        return {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }