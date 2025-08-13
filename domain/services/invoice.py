from domain.services.documento import Documento
from domain.services.socionegocio import SocioNegocio


class Invoice(Documento):

    @staticmethod
    def build_query_filters(data, type):

        print("data", data)
        
        filters = {}
        filter_condition = ""

        carCode = SocioNegocio.get_clen_carCode(data.get('carData'))

        if data.get('carData'):
            filters[f'{type}/SalesPersonCode eq SalesPersons/SalesEmployeeCode and ({type}/CardCode eq'] = f"'{carCode}C' or {type}/CardCode eq '{carCode}c' or contains({type}/CardCode, '{carCode}'))"
        if data.get('docNum'):
            filters[f'{type}/DocNum eq'] = f"{data.get('docNum')}"
        if data.get('folio_number'):
            filters[f'{type}/FolioNumber eq'] = f"{data.get('folio_number')}"
        if data.get('fecha_doc'):
            filters[f'{type}/DocDate ge'] = f"'{data.get('fecha_doc')}'"
        if data.get('DocumentStatus') == 'Y':
            filters[f'{type}/Cancelled eq'] = f"'{data.get('DocumentStatus')}'"
        else:
            filters[f'{type}/DocumentStatus eq'] = f"'{data.get('DocumentStatus')}'"
        if data.get('docTotal'):
            filters[f'contains({type}/DocTotal, '] = f"{int(data.get('docTotal'))})"

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