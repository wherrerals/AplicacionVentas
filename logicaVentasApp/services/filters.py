class FilterPreparer:
    @staticmethod
    def prepare_filters(data, document_type):
        filters = {}

        def add_filter(key, value):
            if value:
                filters[key] = value

        # Fechas
        if data.get('fecha_doc'):
            fecha_doc = str(data.get('fecha_doc'))
            add_filter(f'{document_type}/DocDate ge', f"'{fecha_doc}'")
            add_filter(f'{document_type}/DocDate le', f"'{fecha_doc}'")

        if data.get('fecha_inicio'):
            add_filter(f'{document_type}/DocDate ge', f"'{data.get('fecha_inicio')}'")

        if data.get('fecha_fin'):
            add_filter(f'{document_type}/DocDate le', f"'{data.get('fecha_fin')}'")

        # Número de documento
        if data.get('docNum'):
            try:
                docum = int(data.get('docNum'))
                add_filter(f'contains({document_type}/DocNum,', f"{docum})")
            except ValueError:
                pass  # O manejar el error de conversión

        # Datos de tarjeta
        if data.get('carData'):
            car_data = data.get('carData')
            if car_data.isdigit():
                add_filter(f'contains({document_type}/CardCode,', f"'{car_data}')")
            else:
                add_filter(f'contains({document_type}/CardName,', f"'{car_data}')")

        # Empleado de ventas
        if data.get('salesEmployeeName'):
            try:
                numecode = int(data.get('salesEmployeeName'))
                add_filter('contains(SalesPersons/SalesEmployeeCode,', f"{numecode})")
            except ValueError:
                pass  # O manejar el error de conversión

        # Estado del documento
        if data.get('DocumentStatus'):
            document_status = data.get('DocumentStatus')
            if document_status in ['O', 'C']:
                add_filter(f'{document_type}/DocumentStatus eq', f"'{document_status}'")
                if document_status == 'C':
                    add_filter(f'{document_type}/Cancelled eq', "'N'")
            else:
                add_filter(f'{document_type}/Cancelled eq', "'Y'")

        # Total del documento
        if data.get('docTotal'):
            try:
                docTotal = float(data.get('docTotal'))
                add_filter(f'{document_type}/DocTotal eq', f"{docTotal}")
            except ValueError:
                pass  # O manejar el error de conversión

        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters