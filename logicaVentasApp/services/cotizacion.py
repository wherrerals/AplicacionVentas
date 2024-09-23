import json
from django.http import JsonResponse
from requests import request
from adapters.sl_client import APIClient
from logicaVentasApp.services.documento import Documento
import logging
logger = logging.getLogger(__name__)

class Cotizacion(Documento):
    def __init__(self, request=None):
        super().__init__(request)
        self.client = APIClient()
        self.cliente = None
        self.items = []
    

    def get_endpoint(self):
        """
        Obtiene el endpoint específico de la cotización.
        """
        return 'Quotations'
    
    def validarDatosObligatorios(self):
        """
        Valida los datos obligatorios de la cotización.
        """
        super().validarDatosObligatorios()
        if not self.cliente or not self.items:
            raise ValueError("Faltan datos obligatorios para la cotización.")
    
    def crearOActualizarCotizacion(self):
        """
        Crea o actualiza una cotización.
        """
        self.validarDatosObligatorios()
        if self.docEntry:
            return self.actualizarDocumento()
        else:
            return self.crearDocumento()
    
    
    def validarDatosObligatorios(self, data, required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")
    
    def construirFiltrosCotizaciones(data):
        """
        Construye los filtros para la consulta de cotizaciones basados en los datos proporcionados.
        """

        filters = {}

        if data.get('fecha_inicio'):
            filters['Quotations/DocDate ge'] = str(f"'{data.get('fecha_inicio')}'")
        if data.get('fecha_fin'):
            filters['Quotations/DocDate le'] = str(f"'{data.get('fecha_fin')}'")
        if data.get('docNum'):
            docum = int(data.get('docNum'))
            filters['contains(Quotations/DocNum,'] = f"{docum})"
        if data.get('carCode'):
            filters['contains(Quotations/CardCode,'] = f"'{data.get('carCode')}'"
        if data.get('cardNAme'):
            filters['contains(Quotations/CardName,'] = f"'{data.get('cardNAme')}')"
        if data.get('salesEmployeeName'):
            filters['contains(SalesPersons/SalesEmployeeName,'] = f"'{data.get('salesEmployeeName')}'"
        if data.get('DocumentStatus'):
            filters['Quotations/DocumentStatus eq'] = f"'{data.get('DocumentStatus')}'"
        if data.get('docTotal'):
            filters['contains(Quotations/DocTotal,'] = data.get('docTotal')
        if data.get('cancelled'):
            filters['Quotations/Cancelled eq'] = f"'{data.get('cancelled')}'"

        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters
        
    @staticmethod
    def buscarDocumentosCotizacion(doc_entry):
        try:
            print("-" * 10)
            print(f"Fetching quotation items for DocEntry: {doc_entry}")
            client = APIClient()
            data = client.obtenerCotizacionesDE('Quotations', doc_entry)
            print(f"Data received: {data}")
            print("-" * 10)

            if 'value' not in data:
                return None, 'No se encontraron datos de cotización'
            
            quotations = data['value']

            try:
                doc_entry_int = int(doc_entry)
            except ValueError:
                return None, f'El valor de DocEntry proporcionado ({doc_entry}) no es un número válido'
            
            # Filtramos las líneas de documento que coinciden con el DocEntry
            matching_lines = [
                q['Quotations/DocumentLines'] 
                for q in quotations 
                if q['Quotations/DocumentLines']['DocEntry'] == doc_entry_int
            ]

            if not matching_lines:
                return None, f'No se encontró la cotización con el DocEntry {doc_entry}'
            
            lines_data = Cotizacion.prepararLineasInternas(matching_lines)

            return lines_data, None

        except APIClient.ConnectionError as e:
            logger.error(f"Error de conexión al obtener detalles de la cotización: {str(e)}")
            return None, 'Error de conexión al servidor'
        except APIClient.TimeoutError as e:
            logger.error(f"Tiempo de espera agotado al obtener detalles de la cotización: {str(e)}")
            return None, 'Tiempo de espera agotado en la solicitud al servidor'
        except Exception as e:
            logger.error(f"Error inesperado al obtener detalles de la cotización: {str(e)}")
            return None, 'Error interno del servidor'


    @staticmethod
    def prepararLineasInternas(documentLines):
        return [
            {
                'docEntry': line.get('DocEntry'),
                'LineNum': line.get('LineNum'),
                'ItemCode': line.get('ItemCode'),
                'WarehouseCode': line.get('WarehouseCode'),
                'Quantity': line.get('Quantity'),
                'UnitPrice': line.get('UnitPrice'),
                "GrossPrice": line.get('GrossPrice'),
                "DiscountPercent": line.get('DiscountPercent'),
                "Price": line.get('Price'),
                "PriceAfterVAT": line.get('PriceAfterVAT'),
                "LineTotal": line.get('LineTotal'),
                "GrossTotal": line.get('GrossTotal'),
                "ShipDate": line.get('ShipDate'),
                "Address": line.get('Address'),
                "ShippingMethod": line.get('ShippingMethod'),
                "FreeText": line.get('FreeText'),
                "BaseType": line.get('BaseType'),
                "GrossBuyPrice": line.get('GrossBuyPrice'),
                "BaseEntry": line.get('BaseEntry'),
                "BaseLine": line.get('BaseLine'),
                "LineStatus": line.get('LineStatus'),
            }
            for line in documentLines
        ]

    def prepararJsonCotizacion(self, jsonData):
        """
        Prepara los datos JSON específicos de la cotización.
        """
        # Datos de la cabecera
        cabecera = {
            'DocDate': jsonData.get('DocDate'),
            'DocDueDate': jsonData.get('DocDueDate'),
            'TaxDate': jsonData.get('TaxDate'),
            'CardCode': jsonData.get('CardCode'),
            'PaymentGroupCode': jsonData.get('PaymentGroupCode'),
            'SalesPersonCode': jsonData.get('SalesPersonCode'),
            'TransportationCode': jsonData.get('TransportationCode'),
            'U_LED_NROPSH': jsonData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': jsonData.get('U_LED_TIPVTA'),
            'U_LED_TIPDOC': jsonData.get('U_LED_TIPDOC'),
            'U_LED_FORENV': jsonData.get('U_LED_FORENV'),
        }

        # Datos de las líneas
        lineas = jsonData.get('DocumentLines', [])
        lineas_json = [
            {
                'lineNum': linea.get('lineNum'),
                'ItemCode': linea.get('ItemCode'),
                'Quantity': linea.get('Quantity'),
                'ShipDate': linea.get('ShipDate'),
                'DiscountPercent': linea.get('DiscountPercent'),
                'WarehouseCode': linea.get('WarehouseCode'),
                'CostingCode': linea.get('CostingCode'),
                'ShippingMethod': linea.get('ShippingMethod'),
                'COGSCostingCode': linea.get('COGSCostingCode'),
                'CostingCode2': linea.get('CostingCode2'),
                'COGSCostingCode2': linea.get('COGSCostingCode2'),
                'UnitPrice': linea.get('UnitPrice'),
            }
            for linea in lineas
        ]

        # Combina cabecera y líneas en un solo diccionario
        return {
            **cabecera,
            'DocumentLines': lineas_json,
        }


    
    def crearDocumento(self, data):
        """
        Crea una nueva cotización.
        """
        try:
            jsonData = self.prepararJsonCotizacion(data)
            response = self.client.crearCotizacionSL(self.get_endpoint(), jsonData)
            return response
        except Exception as e:
            logger.error(f"Error al crear la cotización: {str(e)}")
            return {'error': str(e)}

    def eliminarDocumento(self, docEntry):
        """
        Elimina una cotización.
        """
        try:
            response = self.client.eliminarDocumentoSL(self.get_endpoint(), docEntry)
            return response
        except Exception as e:
            logger.error(f"Error al eliminar la cotización: {str(e)}")
            return {'error': str(e)}

    def actualizarEstadoDocumento(self, docNum, estado):
        """
        Actualiza el estado de una cotización.
        """
        print("Actualizando estado de la cotización...")
        try:
            response = self.client.actualizarEstadoDocumentoSL(self.get_endpoint(), docNum, estado)
            return response
        except Exception as e:
            logger.error(f"Error al actualizar el estado de la cotización: {str(e)}")
            return {'error': str(e)}