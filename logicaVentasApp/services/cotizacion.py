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
