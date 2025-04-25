from logicaVentasApp.services.socionegocio import SocioNegocio


class SalesConsultation:

    @staticmethod
    def build_query_filters(data, type):

        filters = {}

        carCode = SocioNegocio.get_clen_carCode(data.get('cardCode'))

        if data.get('cardCode'):
            filters[f'{type}/SalesPersonCode eq SalesPersons/SalesEmployeeCode and ({type}/CardCode eq'] = f"'{carCode}' or {type}/CardCode eq '{data.get('docNum')}' or contains({type}/CardCode, '{data.get('docNum')}'))"
        if data.get('docNum'):
            filters[f'{type}/DocNum eq'] = f"{data.get('docNum')}"
        if data.get('folioNumber'):
            filters[f'{type}/FolioNumber eq'] = f"{data.get('folioNumber')}"

        filters = {k: v for k, v in filters.items() if v and v != "''"}
        
        if filters:
            for key, value in filters.items():
                filter_condition += f" and {key} {value}"

        return filter_condition