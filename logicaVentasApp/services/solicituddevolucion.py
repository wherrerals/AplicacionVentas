from logicaVentasApp.services.documento import Documento


class SolicitudesDevolucion(Documento):

    def construirSolicitudesDevolucion(data):
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
            filters['ReturnRequest/DocDate ge'] = str(f"'{data.get('fecha_doc')}'")
            filters['ReturnRequest/DocDate le'] = str(f"'{data.get('fecha_doc')}'")
        if data.get('fecha_inicio'):
            filters['ReturnRequest/DocDate ge'] = str(f"'{data.get('fecha_inicio')}'")
        if data.get('fecha_fin'):
            filters['ReturnRequest/DocDate le'] = str(f"'{data.get('fecha_fin')}'")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(ReturnRequest/DocNum,'] = f"{docum})"

        # Modificación para el filtro de CardName con múltiples opciones de formato
        # Mantener la lógica original para carData
        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(ReturnRequest/CardCode,'] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['(contains(ReturnRequest/CardName,'] = f"'{name_mayus}') or contains(ReturnRequest/CardName, '{name_minus}') or contains(ReturnRequest/CardName, '{name_title}'))"

        if data.get('salesEmployeeName'):
            numecode = int(data.get('salesEmployeeName'))
            filters['contains(SalesPersons/SalesEmployeeCode,'] = f"{numecode})" 
        
        if data.get('DocumentStatus'):
            document_status = data.get('DocumentStatus')

            if document_status == 'O':
                filters['ReturnRequest/DocumentStatus eq'] = "'O'"
            elif document_status == 'C':
                filters['ReturnRequest/DocumentStatus eq'] = "'C'"
                filters['ReturnRequest/Cancelled eq'] = "'N'"
                
            else:
                filters['ReturnRequest/Cancelled eq'] = "'Y'"

        if data.get('docTotal'):
            docTotal = float(data.get('docTotal'))
            filters['ReturnRequest/DocTotal eq'] = f"{docTotal}"

        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters