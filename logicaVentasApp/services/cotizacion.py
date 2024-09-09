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
    
    """     
def prepare_filters(self, data):
        filters = []

        # Asegurarse de que data sea un diccionario
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON string")
                return ''

        # Mapeo de campos a sus respectivos filtros
        filter_mapping = {
            'fecha_inicio': ('Quotations/DocDate ge', str),
            'fecha_fin': ('Quotations/DocDate le', str),
            'docNum': ('contains(Quotations/DocNum,', int),
            'carCode': ('contains(Quotations/CardCode,', str),
            'cardName': ('contains(Quotations/CardName,', str),
            'salesEmployeeName': ('contains(SalesPersons/SalesEmployeeName,', str),
            'DocumentStatus': ('Quotations/DocumentStatus eq', str),
            'docTotal': ('contains(Quotations/DocTotal,', float),
            'cancelled': ('Quotations/Cancelled eq', str)
        }

        for field, (filter_key, value_type) in filter_mapping.items():
            value = data.get(field)
            if value:
                try:
                    value = value_type(value)
                    # Construye el filtro para campos que usan "contains" o filtros de igualdad
                    if 'contains' in filter_key:
                        filters.append(f"{filter_key}{value})")
                    elif 'eq' in filter_key:
                        filters.append(f"{filter_key} '{value}'")
                    else:
                        filters.append(f"{filter_key} {value}")
                except (ValueError, TypeError):
                    print(f"Error: Unable to convert {field} to {value_type}")
                    continue

        # Limpieza de filtros vacíos
        return ' and '.join(filters) 
    """
        
    def obtenerCotizaciones(self, client, docEntry):
        all_quotations = []
        page = 1
        while True:
            data = client.get_quotations_items('Quotations', docEntry, top=20, skip=(page - 1) * 20)
            if 'value' not in data or not data['value']:
                break
            all_quotations.extend(data['value'])
            if 'odata.nextLink' not in data:
                break
            page += 1
        return all_quotations
    
    def prepararLineasItemas(self, document_lines):
        return [
            {
                'LineNum': line.get('LineNum'),
                'ItemCode': line.get('ItemCode'),
                'ItemDescription': line.get('ItemDescription'),
                'Quantity': line.get('Quantity'),
                'Price': line.get('Price'),
            }
            for line in document_lines
        ]
    
    def prepararJsonData(self):
        """
        Prepara los datos JSON específicos de la cotización.
        """
        data = {
            'docEntry': self.docEntry,
            'docNum': self.docNum,
            'folio': self.folio,
            'fechaDocumento': self.fechaDocumento,
            'fechaEntrega': self.fechaEntrega,
            'horarioEntrega': self.horarioEntrega,
            'referencia': self.referencia,
            'comentario': self.comentario,
            'totalAntesDelDescuento': self.totalAntesDelDescuento,
            'descuento': self.descuento,
            'totalDocumento': self.totalDocumento,
            'codigoVenta': self.codigoVenta,
            'tipo_documento': self.tipo_documento,
            'vendedor': self.vendedor,
            'condi_pago': self.condi_pago,
            'tipoentrega': self.tipoentrega,
            'tipoobjetoSap': self.tipoobjetoSap,
            'items': self.prepararLineasItemas(self.items),
        }
        return data
    
    def getdocumentlines(self):
        """
        Método abstracto para obtener las líneas del documento.
        Debe ser implementado por las subclases.
        """
        pass
