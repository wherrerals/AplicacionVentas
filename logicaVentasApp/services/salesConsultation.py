from logicaVentasApp.services.socionegocio import SocioNegocio


class SalesConsultation:

    @staticmethod
    def build_query_filters(data, type):
        
        filters = {}
        filter_condition = ""

        carCode = SocioNegocio.get_clen_carCode(data.get('carData'))

        if data.get('carData'):
            filters[f'{type}/SalesPersonCode eq SalesPersons/SalesEmployeeCode and ({type}/CardCode eq'] = f"'{carCode}C' or {type}/CardCode eq '{carCode}c' or contains({type}/CardCode, '{carCode}'))"
        if data.get('docNum'):
            filters[f'{type}/DocNum eq'] = f"{data.get('docNum')}"
        if data.get('folioNumber'):
            filters[f'{type}/FolioNumber eq'] = f"{data.get('folioNumber')}"

        filters = {k: v for k, v in filters.items() if v and v != "''"}
        
        if filters:
            first_filter = True
            for key, value in filters.items():
                if first_filter:
                    filter_condition += f"{key} {value}"
                    first_filter = False
                else:
                    filter_condition += f" and {key} {value}"

        return filter_condition