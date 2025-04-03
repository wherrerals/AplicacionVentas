from abc import ABC, abstractmethod
import logging

from adapters.sl_client import APIClient
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.productorepository import ProductoRepository

logger = logging.getLogger(__name__)

class Documento(ABC):
    
    def __init__(self, request=None):
        self.request = request
        self.docEntry = None
        self.docNum = None
        self.folio = None
        self.fechaDocumento = None
        self.fechaEntrega = None
        self.horarioEntrega = None
        self.referencia = None
        self.comentario = None
        self.totalAntesDelDescuento = None
        self.descuento = None
        self.totalDocumento = None
        self.codigoVenta = None
        self.tipo_documento = None
        self.vendedor = None
        self.condi_pago = None
        self.tipoentrega = None
        self.tipoobjetoSap = None
        # Otros atributos comunes a todos los documentos



    def get_endpoint(self):
        """
        Método abstracto para obtener el endpoint específico del documento.
        Debe ser implementado por las subclases.
        """
        pass

    def validarDatosObligatorios(self):
        """
        Método para validar los datos obligatorios del documento.
        Implementa aquí la validación común para todos los documentos.
        """
        if not self.fechaDocumento or not self.fechaEntrega or not self.codigoVenta:
            raise ValueError("Faltan datos obligatorios para el documento.")

    def crearOActualizarDocumento(self):
        """
        Método para crear o actualizar un documento.
        Utiliza `self.docEntry` para decidir si debe crear o actualizar.
        """
        self.validarDatosObligatorios()
        if self.docEntry:
            return self.actualizarDocumento()
        else:
            return self.crearDocumento()

    def crearDocumento(self):
        """
        Método para crear un nuevo documento.
        """
        try:
            json_data = self.preparar_json_data()
            endpoint = self.get_endpoint()
            headers = {"Content-Type": "application/json"}
            result = self.client.post_data(endpoint, data=json_data, headers=headers)
            return result
        except Exception as e:
            logger.error(f"Error al crear el documento: {e}")
            raise

    def actualizarDocumento(self):
        """
        Método para actualizar un documento existente.
        """
        if not self.docEntry:
            raise ValueError("No se puede actualizar un documento sin DocEntry.")
        try:
            json_data = self.preparar_json_data()
            endpoint = f"{self.get_endpoint()}/{self.docEntry}"
            headers = {"Content-Type": "application/json"}
            result = self.client.post_data(endpoint, data=json_data, headers=headers)
            return result
        except Exception as e:
            logger.error(f"Error al actualizar el documento: {e}")
            raise

    def obtenerDocumentoPorDocEntry(self):
        """
        Método para obtener un documento por su DocEntry.
        """
        try:
            endpoint = f"{self.get_endpoint()}/{self.docEntry}"
            result = self.client.getData(endpoint=endpoint)
            return result
        except Exception as e:
            logger.error(f"Error al obtener el documento: {e}")
            raise

    def obtenerDocumentoPorDocNum(self):
        """
        Método para obtener un documento por su DocNum.
        """
        try:
            endpoint = self.get_endpoint()
            filters = {"DocNum": f"eq '{self.docNum}'"}
            result = self.client.getData(endpoint=endpoint, filters=filters)
            return result
        except Exception as e:
            logger.error(f"Error al obtener el documento: {e}")
            raise

    def filtroDocumentos(self):
        """
        Método para filtrar documentos.
        """
        try:
            filters = self.prepare_filters()
            endpoint = self.get_endpoint()
            result = self.client.getData(endpoint=endpoint, filters=filters)
            return result
        except Exception as e:
            logger.error(f"Error al filtrar documentos: {e}")
            raise

    def getdocumentlines(self):
        """
        Método abstracto para obtener las líneas del documento.
        Debe ser implementado por las subclases.
        """
        pass
    

    def prepararJsonData(self, data):
        """
        Prepara los datos JSON para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass

    def get_endpoint(self):
        """
        Define el endpoint para la creación del documento.
        Debe ser implementado por las clases hijas.
        """
        pass

    def prepare_json_document(self, jsonData):
        """
        Prepara los datos JSON específicos de la cotización.

        Args:
            jsonData (dict): Datos de la cotización.
        
        Returns:
            dict: Datos de la cotización preparados para ser enviados a SAP.
        """
            
        # Determinar el tipo de venta basado en el vendedor
        print(f"jsonData: {jsonData}")

        if jsonData.get('DocEntry'):
            actualizar = True
            client = APIClient()
        else:
            actualizar = False
        
        codigo_vendedor = jsonData.get('SalesPersonCode')
        tipo_venta = self.tipoVentaTipoVendedor(codigo_vendedor)
        
        # Si el tipo de venta por vendedor no es válido ('NA'), determinar por líneas
        if tipo_venta == 'NA':
            lineas = jsonData.get('DocumentLines', [])
            tipo_venta = self.tipoVentaTipoLineas(lineas)
        
        transportationCode = jsonData.get('TransportationCode')

        if tipo_venta == 'NA' and transportationCode != '1':
            tipo_venta = 'RESE'
        elif tipo_venta == 'PROY':
            tipo_venta = 'PROY'
        elif tipo_venta == 'ECCO':
            tipo_venta = 'ECCO'
                    
        adrres = jsonData.get('Address')
        adrres2 = jsonData.get('Address2')
        
        idContacto = jsonData.get('ContactPersonCode')
        
        if idContacto == "No hay contactos disponibles":
            numerocontactoSAp = "null"
        else:
            contacto = ContactoRepository.obtenerContacto(idContacto)
            numerocontactoSAp = contacto.codigoInternoSap        #consultar en base de datos con el id capturado
        
        if adrres == "No hay direcciones disponibles":
            addresmodif = "null"
        else:
            direccion1 = DireccionRepository.obtenerDireccion(adrres)
            addresmodif = f"{direccion1.calleNumero}, {direccion1.comuna.nombre}\n{direccion1.ciudad}\n{direccion1.region.nombre}"

        if adrres2 == "No hay direcciones disponibles":
            addresmodif2 = "null"
        else:
            direccionRepo2 = DireccionRepository.obtenerDireccion(adrres2)
            addresmodif2 = f"{direccionRepo2.calleNumero}, {direccionRepo2.comuna.nombre}\n{direccionRepo2.ciudad}\n{direccionRepo2.region.nombre}"
        
        # Datos de la cabecera
        cabecera = {
            'DocDate': jsonData.get('DocDate'),
            'DocDueDate': jsonData.get('DocDueDate'),
            'TaxDate': jsonData.get('TaxDate'),
            'DocTotal': jsonData.get('DocTotal'),
            #'ContactPersonCode': numerocontactoSAp,
            #'Address': addresmodif,
            #'Address2': addresmodif2,
            'CardCode': jsonData.get('CardCode'),
            'NumAtCard': jsonData.get('NumAtCard'),
            'Comments': jsonData.get('Comments'),
            'PaymentGroupCode': jsonData.get('PaymentGroupCode'),
            'SalesPersonCode': jsonData.get('SalesPersonCode'),
            'TransportationCode': jsonData.get('TransportationCode'),
            #'U_LED_NROPSH': jsonData.get('U_LED_NROPSH'),
            'U_LED_TIPVTA': tipo_venta,  # Tipo de venta calculado
            'U_LED_TIPDOC': jsonData.get('U_LED_TIPDOC'),
            'U_LED_FORENV': jsonData.get('TransportationCode'),
        }

        # Datos de las líneas
        lineas = jsonData.get('DocumentLines', [])

        repo_producto = ProductoRepository()
        
        #maper item code
        lineas_json = []


        # Mapeo de item code
        lineas_json = []

        for linea in lineas:
            item_code = linea.get('ItemCode')
            
            if repo_producto.es_receta(item_code):
                treeType = 'iSalesTree'
            else:
                treeType = 'iNotATree'
            
            # Obtener lineNum, pero solo usarlo si es un número válido
            #line_num_str = linea.get('LineNum')
            #line_num = int(line_num_str) if line_num_str and line_num_str.isdigit() else None  # Dejarlo como None si no es válido
            line_num = 0
            warehouseCode = linea.get('WarehouseCode')

            nueva_linea = {
                #'lineNum': line_num,  # Se mantiene como None si no hay un valor válido
                'ItemCode': item_code,
                'Quantity': linea.get('Quantity'),
                'UnitPrice': repo_producto.obtener_precio_unitario_neto(linea.get('ItemCode')),
                'ShipDate': linea.get('ShipDate'),
                'FreeText': linea.get('FreeText'),
                'DiscountPercent': linea.get('DiscountPercent'),
                'WarehouseCode': warehouseCode,
                'CostingCode': linea.get('CostingCode'),
                'ShippingMethod': linea.get('ShippingMethod'),
                'COGSCostingCode': linea.get('COGSCostingCode'),
                'CostingCode2': linea.get('CostingCode2'),
                'COGSCostingCode2': linea.get('COGSCostingCode2'),
                'TreeType': treeType,
            }

            lineas_json.append(nueva_linea)

        taxExtension = {
            "StreetS": direccion1.calleNumero,
            "CityS": direccion1.ciudad,
            "CountyS": f"{direccion1.comuna.codigo} - {direccion1.comuna.nombre}",
            "StateS": direccion1.region.numero,
            "CountryS": "CL",
            "StreetB": direccionRepo2.calleNumero,
            "CityB": direccionRepo2.ciudad,
            "CountyB": f"{direccionRepo2.comuna.codigo} - {direccionRepo2.comuna.nombre}",
            "StateB": direccionRepo2.region.numero,
            "CountryB": "CL",
        } 
    
        dic = {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }

        print(f"dic: {dic}")

        return {
            **cabecera,
            'DocumentLines': lineas_json,
            'TaxExtension': taxExtension
        }