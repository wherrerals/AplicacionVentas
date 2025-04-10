class TypeOfSale:

    @staticmethod
    def Sale_type_line_type(lineas):
        """
        Asigna el tipo de venta a las líneas de la cotización.

        - Si todas las lineas son del mismo warehouse, se asigna el tipo de venta: TIEN.
        - Si las lineas son de diferentes warehouses, se asigna el tipo de venta: RESE.

        Args:
            lineas (list): Líneas de la cotización.
        """

        warehouses = set(linea.get('WarehouseCode') for linea in lineas)
        return 'TIEN' if len(warehouses) == 1 else 'RESE'
    
    @staticmethod
    def sale_type(type_sales, transportation_code):

        if type_sales == 'NA' and transportation_code != '1':
            return 'RESE'
        
        elif type_sales == 'PROY':
            return 'PROY'
        
        elif type_sales == 'ECCO':
            return 'ECCO'
        
        else:
            return type_sales