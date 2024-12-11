import json
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
from datosLsApp.repositories.vendedorRepository import VendedorRepository
from logicaVentasApp.services.documento import Documento
import logging
logger = logging.getLogger(__name__)

class OrdenVenta(Documento):


    def construirFiltros(data):

        """
        Construye los filtros para la consulta de cotizaciones basados en los datos proporcionados.

        Args:
            data (dict): Datos de la consulta.

        Returns:
            dict: Filtros para la consulta de cotizaciones.
        """

        filters = {}

        if data.get('fecha_doc'):
            filters['Orders/DocDate ge'] = str(f"'{data.get('fecha_doc')}'")
            filters['Orders/DocDate le'] = str(f"'{data.get('fecha_doc')}'")
        if data.get('fecha_inicio'):
            filters['contains(Orders/DocNum, '] = str(f"{data.get('fecha_inicio')})")
        if data.get('fecha_fin'):
            filters['contains(Orders/CardCode, '] = str(f"{data.get('fecha_fin')})")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Orders/CardName, '] = f"{docum})"

        if data.get('carData'):
            car_data = data.get('carData')
            
            if car_data.isdigit():  # Si es un número
                filters['contains(SalesPersons/SalesEmployeeName, '] = f"'{car_data}')"
            else:  # Si contiene letras (nombre)
                filters['contains(Quotations/CardName,'] = f"'{car_data}')"

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
                filters['Quotations/DocumentStatus eq'] = "'O'"
            elif document_status == 'C':
                filters['Quotations/DocumentStatus eq'] = "'C'"
                filters['Quotations/Cancelled eq'] = "'N'"
                
            else:
                filters['Quotations/Cancelled eq'] = "'Y'"

        if data.get('docTotal'):
            docTotal = float(data.get('docTotal'))
            filters['Quotations/DocTotal eq'] = f"{docTotal}"


        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters

"""
and Orders/DocDate ge '2023-05-23' and Orders/DocDate le '2023-05-25' and contains(Orders/DocNum, 12) and contains(Orders/CardCode, '2') and contains(Orders/CardName, 'CA') and contains(SalesPersons/SalesEmployeeName, 'e') 
and Orders/DocumentStatus eq 'C' and contains(Orders/DocTotal, 0) and Orders/Cancelled eq 'Y'
"""