import json
import logging
import re
from venv import logger
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from adapters.serializador import Serializador
from datosLsApp.models.gruposndb import GrupoSNDB
from datosLsApp.models.socionegociodb import SocioNegocioDB
from datosLsApp.models.tipoclientedb import TipoClienteDB
from datosLsApp.models.tiposndb import TipoSNDB
from datosLsApp.repositories.comunarepository import ComunaRepository
from datosLsApp.repositories.socionegociorepository import SocioNegocioRepository
from datosLsApp.repositories.gruposnrepository import GrupoSNRepository
from datosLsApp.repositories.tipoclienterepository import TipoClienteRepository
from datosLsApp.repositories.tiposnrepository import TipoSNRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.models import DireccionDB, ContactoDB
from adapters.sl_client import APIClient
from datosLsApp.serializer.businessPartnerSerializer import BusinessPartnerSerializer
from logicaVentasApp.services.direccion import Direccion
from taskApp.models import SyncState


class SocioNegocio:
    
    def __init__(self, request):
        
        try:
            dataSN = json.loads(request.body)
        except (json.JSONDecodeError, AttributeError):
            dataSN = None

        self.logger = logging.getLogger(__name__)
        self.request = dataSN
        
        if dataSN:
            self.gruposn = dataSN.get('tipoSN')
            self.rut = dataSN.get('rutSN')
            self.email = dataSN.get('emailSN')
            self.nombre = dataSN.get('nombreSN')
            self.apellido = dataSN.get('apellidoSN')
            self.razon_social = dataSN.get('nombreSN')
            self.giro = dataSN.get('giroSN')
            self.telefono = dataSN.get('telefonoSN')
        else:
            self.gruposn = None
            self.rut = None
            self.email = None
            self.nombre = None
            self.apellido = None
            self.razon_social = None
            self.giro = None
            self.telefono = None
        
        
    def validate_madatary_data_bp(self):
        """
        this method is used to validate the mandatory data of the business partner.
        """
        self.validarGrupoSN()
        self.validarRut()
        self.validarEmail()
        self.validarNombre()
        self.validarApellido()
        self.validarTelefono()
        self.tamañotelefono()        
        self.validarDirecciones()
        self.validarContactos()

    def process_existing_bp(self, cardcode, datosCliente, newData):
        
        verificacionSap = self.verify_sap_bp(cardcode)

        if verificacionSap:

            updata_bp = self.actualizarSocioNegocio(cardcode, newData)
            
            if updata_bp.get('error'): 
                return JsonResponse({'error': True, 'message': updata_bp['message']}, status=400)
            
            return JsonResponse({'success': True, 'message': 'Cliente actualizado exitosamente'})
        
        else:
            # Si no existe en SAP, se crea un nuevo socio de negocio
            print("no existe en sap")
            SocioNegocioDB.objects.filter(rut=datosCliente.rut).delete()
            self.process_new_bp(cardcode, newData)
            return JsonResponse({'success': True, 'message': 'Cliente actualizado exitosamente'})
        
        

    def actualizarSocioNegocio(self, cardcode, datos):

        repo = SocioNegocioRepository()
        conexionSL = APIClient()
        serializer = Serializador(formato='json')

        # Verificar grupo de cliente
        grupo_sn = datos.get('tipoSN')

        datosSerializados = serializer.serializar(datos, cardcode)
        response = conexionSL.actualizarSocioNegocioSL(cardcode, datosSerializados)

        if response.get('error'):
            return ({'error': True, 'message': response['message']})
        
        else:
            if grupo_sn == '105':            
                return repo.actualizarCliente(cardcode, datos)
            else:
                return repo.actualizarClienteEmpresa(cardcode, datos)


    def obtenerGrupoSN(self):

        grupoSN = GrupoSNRepository.obtenerGrupoSNPorCodigo(self.gruposn)
        if not grupoSN:
            raise ValidationError(f"Grupo de socio de negocio no encontrado para el código: {self.gruposn}")
        return grupoSN

    def obtenerTipoCliente(self):

        tipoCliente = TipoClienteRepository.obtenerTipoClientePorCodigo('N')
        if not tipoCliente:
            raise ValidationError("Tipo de cliente no encontrado")
        return tipoCliente

    def obtenerTipoSN(self):
        tiposn = TipoSNRepository.obtenerTipoSnPorCodigo('C' if self.gruposn == '100' else 'I')
        if not tiposn:
            raise ValidationError(f"Tipo de socio de negocio no encontrado para el código: {'C' if self.gruposn == '100' else 'I'}")
        return tiposn


    @staticmethod
    def generate_bp_code(rut):

        rut_sn = rut.split("-")[0] if "-" in rut else rut
        return rut_sn.replace(".", "") + 'C'


    @staticmethod
    def agregarDireccionYContacto(request, cliente):

        from showromVentasApp.views.view import agregarDireccion, agregarContacto

        # Capturar datos de dirección y contacto desde el request
        direccion = request.POST.get('nombre_direccion[]')
        nombre_contacto = request.POST.get('nombre[]') or cliente.nombre
        apellido_contacto = request.POST.get('apellido[]') or cliente.apellido
        telefono_contacto = request.POST.get('telefono[]') or cliente.telefono
        email_contacto = request.POST.get('email[]') or cliente.email

        # Validar que al menos un contacto esté completo
        if not direccion:
            raise ValidationError("Debe agregar al menos una dirección")

        if not (nombre_contacto and apellido_contacto and telefono_contacto and email_contacto):
            raise ValidationError("Debe proporcionar datos suficientes para un contacto válido.")

        # Preparar datos mínimos para contacto y dirección
        contacto_data = {
            'nombre': nombre_contacto,
            'apellido': apellido_contacto,
            'telefono': telefono_contacto,
            'celular': telefono_contacto,
            'email': email_contacto,
        }

        # Agregar dirección y contacto
        agregarDireccion(request, cliente)
        agregarContacto(request, cliente, **contacto_data)  # Asegúrate de que `agregarContacto` acepte estos datos.

        return JsonResponse({"mensaje": "Dirección y contacto agregados exitosamente."})

    def buscarSocioNegocio(identificador, buscar_por_nombre=False):

        try:
            if buscar_por_nombre:
                # Si se busca por nombre, usa el repositorio que busca por nombre
                resultados_clientes = SocioNegocioRepository.buscarClientesPorNombre(identificador)
                print("resultados_clientesXXX", resultados_clientes)
            else:
                # Si no, se busca por rut (número)
                
                resultados_clientes = SocioNegocioRepository.buscarClientesPorRut(identificador)
                print("resultados_clientes", resultados_clientes)

            if not resultados_clientes:
                logging.info(f"No se encontraron resultados para el identificador: {identificador}")
                return []

            resultados_formateados = []

            for socio in resultados_clientes:
                # Prefetch de direcciones y contactos para evitar consultas N+1
                direcciones = DireccionDB.objects.filter(SocioNegocio=socio).select_related('comuna', 'region')
                contactos = ContactoDB.objects.filter(SocioNegocio=socio)

                # Función para formatear las direcciones
                direcciones_formateadas = SocioNegocio.formatear_direcciones(direcciones)

                # Función para formatear los contactos
                contactos_formateados = SocioNegocio.formatear_contactos(contactos)

                #quitar el - y el digito verificador del rut
                rut = socio.rut.split("-")[0] if "-" in socio.rut else socio.rut

                # Agregar el socio formateado al resultado
                resultados_formateados.append({
                    
                    
                    'id' : rut,
                    'nombre': socio.nombre,
                    'apellido': socio.apellido,
                    'razonSocial': socio.razonSocial,
                    'codigoSN': socio.codigoSN,
                    'rut': socio.rut,
                    'email': socio.email,
                    'telefono': socio.telefono,
                    'giro': socio.giro,
                    'condicionPago': socio.condicionPago,
                    'plazoReclamaciones': socio.plazoReclamaciones,
                    'clienteExportacion': socio.clienteExportacion,
                    'vendedor': socio.vendedor,
                    'direcciones': direcciones_formateadas,
                    'contactos': contactos_formateados
                })

            print("resultados_formateados", resultados_formateados)

            return resultados_formateados
        
        except Exception as e:
            logging.error(f"Error al buscar socio negocio: {e}")
            return {'error': 'Ocurrió un error al realizar la búsqueda'}

    @staticmethod
    def formatear_direcciones(direcciones):

        nombres_direcciones_no_validos = ["TIENDA LC", "TIENDA GR", "TIENDA PH"]
        direcciones_formateadas = []

        for direccion in direcciones:
            if direccion.nombreDireccion not in nombres_direcciones_no_validos:
                direcciones_formateadas.append({
                    "id": direccion.id,
                    'rowNum': direccion.rowNum,
                    'nombreDireccion': direccion.nombreDireccion,
                    'ciudad': direccion.ciudad,
                    'calleNumero': direccion.calleNumero,
                    'codigoImpuesto': direccion.codigoImpuesto,
                    'tipoDireccion': direccion.tipoDireccion,
                    'pais': direccion.pais,
                    'comuna': direccion.comuna.nombre,
                    'region': direccion.region.nombre,
                    'comuna_codigo': direccion.comuna.codigo,
                    'region_numero': direccion.region.numero,
                })

        return direcciones_formateadas

    @staticmethod
    def formatear_contactos(contactos):

        return [{
            'id': contacto.id,
            'codigoInternoSap': contacto.codigoInternoSap,
            'nombreCompleto': contacto.nombreCompleto,
            'nombre': contacto.nombre,
            'apellido': contacto.apellido,
            'email': contacto.email,
            'telefono': contacto.telefono,
            'celular': contacto.celular
        } for contacto in contactos]


    def validarDirecciones(self):
        for direcciones in self.request.get("direcciones", []):
            # Verificar si la dirección tiene los campos obligatorios
            if any(not direcciones.get(campo) for campo in ['tipoDireccion', 'nombreDireccion', 'pais', 'region', 'comuna', 'ciudad', 'direccion']):
                raise ValidationError("Faltan datos obligatorios en la dirección")

    def validarContactos(self):
        for contacto in self.request.get("contactos", []):
            # Verificar si el contacto tiene los campos obligatorios
            if any(not contacto.get(campo) for campo in ['nombreContacto', 'apellidoContacto', 'telefonoContacto', 'puestoContacto', 'emailContacto']):
                raise ValidationError("Faltan datos obligatorios en el contacto")

    def validarGrupoSN(self):
        if not self.gruposn:
            raise ValidationError("Grupo de socio de negocio no encontrado")
        
    def validarNombre(self):
        if not self.nombre:
            raise ValidationError("Nombre no encontrado")
        
    def validarApellido(self):

        if self.gruposn == '105':
            if not self.apellido :
                raise ValidationError("Apellido no encontrado") 
        else:
            self.apellido = None
        
    def validarTelefono(self):

        if not self.telefono:
            raise ValidationError("Teléfono no encontrado")
    
    def tamañotelefono(self):

        if len(self.telefono) < 12:
            raise ValidationError("El teléfono debe tener al menos 12 dígitos")
    
    def validarRut(self):

        if not self.rut:
            raise ValidationError("RUT no encontrado")
        
    def validarEmail(self):

        if not self.email:
            raise ValidationError("Email no encontrado")
        
    def verificarSocioDB(self, rut):

        repo = SocioNegocioRepository()
        socio = repo.obtenerPorCodigoSN(rut)
        
        return True if socio else False
                    
    def verify_sap_bp(self, cardCode):
        client = APIClient()
        response = client.verificarCliente(endpoint="BusinessPartners", cardCode=cardCode)

        if not response:
            print(f"respondiendo ando: {response}")

        return True if response else False

    
    def obtenerDatosCliente(self, cardCode):
        
        cliente = SocioNegocioDB.objects.get(rut=cardCode)
        direcciones = DireccionRepository().obtenerDireccionesPorCliente(cliente)
        contactos = ContactoRepository().obtenerContactosPorCliente(cliente)
        return cliente, direcciones, contactos



    def create_sap_bp(self, json_data_bp):
        print("create sap bp")
        
        api_conection = APIClient()
        
        response = api_conection.create_bp_sl(json_data_bp)
        
        if isinstance(response, dict):
            if 'CardCode' in response:

                return response
            
            elif 'error' in response:
                return {'error': response.text}
            else:
                return {'error': 'Respuesta inesperada de la API.'}
        
        else:
            return {'error': 'La respuesta de la API no es válida.'}




    def verify_valid_rut(self, rut):
        """
        Método para verificar si un RUT es válido.

        Args:
            rut (str): RUT a verificar. Debe tener el formato "XXXXXXXX-X".

        Returns:
            bool: True si el RUT es válido, False si no.
        """
        try:

            # RUT sin puntos y guion
            if '.' in rut:
                return False, "El RUT no debe contener puntos."


            if "-" not in rut:
                return False, "El RUT debe contener un guion antes del dígito verificador."
            
            partes = rut.split("-")
            if len(partes) != 2:
                return False, "Tiene que tener el formato correcto: 'XXXXXXXX-X'."
            
            # Separar el dígito verificador del número base
            numero, digito_verificador = partes
            #numero base en entero
            numero = numero.replace(".", "")  # Quitar puntos
            digito_verificador = digito_verificador.upper()  # Convertir a mayúsculas
            
            # Invertir los dígitos del número base para el cálculo
            numero_invertido = str(numero)[::-1]

            # Lista de multiplicadores cíclicos 2, 3, 4, 5, 6, 7
            multiplicadores = [2, 3, 4, 5, 6, 7]

            # Sumar los productos de los dígitos por los multiplicadores
            suma = 0
            for i, digito in enumerate(numero_invertido):
                suma += int(digito) * multiplicadores[i % len(multiplicadores)]

            # Calcular el residuo
            residuo = suma % 11

            # Calcular el dígito verificador según el módulo 11
            digito_calculado = 11 - residuo

            if digito_calculado == 11:
                digito_calculado = '0'
            elif digito_calculado == 10:
                digito_calculado = 'K'
            else:
                digito_calculado = str(digito_calculado)

            # Retornar si el dígito verificador coincide con el calculado
            return (digito_calculado == digito_verificador, "El RUT es válido." if digito_calculado == digito_verificador else "El RUT es inválido.")

        except Exception as e:
            print(f"Error al verificar RUT: {str(e)}")
            return False

        
    
    def actualizaroCrearDireccionSL(rut, cardCode, data):
        """
        Método para actualizar o crear una dirección en SAP.

        Args:
            cardCode (str): Código del socio de negocio.
            data (dict): Datos de la dirección.

        Returns:
            dict: Mensaje de éxito o error.
        """

        # Obtener la lista de direcciones del request
        direcciones_json = data.getlist('direcciones')
            
        # Deserializar el JSON de direcciones
        direcciones = json.loads(direcciones_json[0])

        serializar = Serializador('json')
        datosSerializados = serializar.mapearDirecciones(direcciones, cardCode, rut)

        client = APIClient()

        try:
            response = client.actualizarDireccionSL(cardCode, datosSerializados)

            if isinstance(response, dict):
                if 'error' in response:
                    return {'success': False, 'message': response.get('error', 'Error desconocido')}
                else:
                    return {'success': True, 'message': 'Dirección actualizada exitosamente'}
            else:
                return {'success': False, 'message': 'Respuesta inesperada de la API'}
        except ConnectionError as e:
            return {'success': False, 'message': 'Error de conexión con SAP'}
        except Exception as e:
            return {'success': False, 'message': f'Error inesperado: {str(e)}'}
        
    def actualizaroCrearContactosSL(cardCode, data):
        """
        Método para actualizar o crear una dirección en SAP.

        Args:
            cardCode (str): Código del socio de negocio.
            data (dict): Datos de la dirección.

        Returns:
            dict: Mensaje de éxito o error.
        """

        contactos_json = data.getlist('contactos')
            
        # Deserializar el JSON
        contactos = json.loads(contactos_json[0])

        serializar = Serializador('json')

        datosSerializados = serializar.mapearContactos(contactos, cardCode)

        client = APIClient()

        try:
            response = client.actualizarContactosSL(cardCode, datosSerializados)

            if isinstance(response, dict):
                if 'error' in response:
                    return {'success': False, 'message': response.get('error', 'Error desconocido')}
                else:
                    return {'success': True, 'message': 'Contacto actualizado exitosamente'}
            else:
                return {'success': False, 'message': 'Respuesta inesperada de la API'}
        except ConnectionError as e:
            return {'success': False, 'message': 'Error de conexión con SAP'}
        except Exception as e:
            return {'success': False, 'message': f'Error inesperado: {str(e)}'}
        
        
    def procesarContactos(data, socio):
            try:
                contactos_json = data.get('contactos')

                if not contactos_json:
                    return JsonResponse({'success': False, 'message': 'No se encontraron contactos en el request.'}, status=400)

                contactos = json.loads(contactos_json[0])
                
                ContactoRepository.eliminarContactosPorSocio(socio)

                for contacto in contactos:
                    nombre = contacto.get('nombre', '')
                    apellido = contacto.get('apellido', '')
                    telefono = contacto.get('telefono', '')
                    celular = contacto.get('celular', '')
                    email = contacto.get('email', '')
                    codigo_interno_sap = int(contacto.get('contacto_id', ''))

                    if nombre:
                        try:
                            ContactoRepository.crearContacto(socio, codigo_interno_sap, nombre, apellido, telefono, email, celular)
                        except Exception as e:
                            return JsonResponse({'success': False, 'message': f'Error al crear el contacto: {str(e)}'}, status=500)
                    else:
                        print("Nombre vacío. No se procesó este contacto.")

                return {'data': {'success': True, 'message': 'Contactos procesados y reemplazados con éxito.'}, 'status': 200}

            except KeyError as e:
                return {'data': {'success': False, 'message': f'Falta el campo: {str(e)}'}, 'status': 400}
            
            except json.JSONDecodeError as e:
                return {'data': {'success': False, 'message': f'Error al decodificar JSON: {str(e)}'}, 'status': 400}


    def infoCliente(self, identificador, buscar_por_nombre=False):

        try:
            if not identificador or not identificador.strip():
                return {'error': 'El identificador está vacío'}

            # Realizar la búsqueda según el tipo
            if buscar_por_nombre:
                resultados_clientes = SocioNegocioRepository.buscarClientesPorNombre(identificador)
            else:
                resultados_clientes = SocioNegocioRepository.buscarClientesPorRut(identificador)

            # Si no hay resultados, retornar lista vacía
            if not resultados_clientes:
                return []

            # Lista para almacenar los resultados formateados
            resultados_formateados = []

            # Procesar cada socio encontrado
            for socio in resultados_clientes:
                try:
                    # Obtener direcciones y contactos del socio
                    direcciones = DireccionDB.objects.filter(
                        SocioNegocio=socio # Filtrar por el socio actual
                    ).select_related('comuna', 'region') # 
                    
                    contactos = ContactoDB.objects.filter(
                        SocioNegocio=socio
                    )

                    # Formatear datos
                    direcciones_formateadas = self.formatear_direcciones(direcciones)
                    contactos_formateados = self.formatear_contactos(contactos)

                    # Crear diccionario con datos del socio
                    socio_formateado = {
                        'nombre': socio.nombre or '',
                        'apellido': socio.apellido or '',
                        'razonSocial': socio.razonSocial or '',
                        'codigoSN': socio.codigoSN or '',
                        'rut': socio.rut or '',
                        'email': socio.email or '',
                        'telefono': socio.telefono or '',
                        'giro': socio.giro or '',
                        'condicionPago': socio.condicionPago or '',
                        'plazoReclamaciones': socio.plazoReclamaciones or '',
                        'clienteExportacion': socio.clienteExportacion or False,
                        'vendedor': socio.vendedor or '',
                        'direcciones': direcciones_formateadas,
                        'contactos': contactos_formateados,
                        'grupoSN': socio.grupoSN.codigo
                    }
                    
                    resultados_formateados.append(socio_formateado)
                    
                except Exception as e:
                    logger.error(f"Error al formatear socio {socio.rut}: {str(e)}")
                    continue

            return resultados_formateados

        except Exception as e:
            logger.error(f"Error al buscar socio negocio: {str(e)}")
            return {'error': f'Error al realizar la búsqueda: {str(e)}'}
        

    def convertirJsonObjeto(self, json_data):
        """
        Metodo para convertir un JSON a un objeto Python.

        args:
            json_data (str): Cadena JSON a convertir.

        Returns:
            dict: Objeto Python convertido.
        """

        # Verificar si `json_data` es una cadena JSON y convertirla si es necesario
        if isinstance(json_data, str):
            return json.loads(json_data)
        
        return json_data  # Si ya es un dict, lo retorna directamente


    def normalize_bp_data(self, data):
        """
        Procesa los datos de un socio de negocio para ser guardados en la base de datos.

        Args:
            data (dict): Datos del socio de negocio.

        Returns:
            dict: Datos del socio de negocio procesados.
        """

        # Obtener 'CardName' con un valor predeterminado
        card_name = data.get('CardName', '')

        # Validar si 'card_name' tiene un espacio
        if card_name and isinstance(card_name, str): 
            name, lastname = card_name.split(' ', 1) if ' ' in card_name else (card_name, None)
        else:
            name, lastname = "Null", "None"

        razonsocial = card_name or "Null"

        # Datos principales del socio de negocio
        socio_negocio = {
            "codigoSN": data.get("CardCode", ""),
            "nombreCompleto": card_name,
            "razonSocial": razonsocial,
            "nombre": name,
            "apellido": lastname,
            "email": data.get("EmailAddress", "") or "sinemali@gmail.com",
            "telefono": data.get("Phone1", "") or "+56000000000",
            "celular": data.get("Phone1", "") or "+56000000000",
            "giro": data.get("Notes", "") or "Null",
            "rut": data.get("FederalTaxID", "") or "Null",
            "grupoSN": data.get("GroupCode", "") or "Null",
            "tipoSN": "I",  # Valor fijo según lo especificado
            "tipoCliente": "N"  # Valor fijo según lo especificado
        }

        # Direcciones del socio de negocio
        direcciones = []
        for direccion in data.get("BPAddresses", []) or []:  # Asegurar que sea iterable
            address_type = direccion.get("AddressType", "")
            # Asignar valores según AddressType
            tipo_direccion = 13 if address_type == "bo_BillTo" else 12 if address_type == "bo_ShipTo" else None

            direcciones.append({
                "rowNum": direccion.get("RowNum", ""),
                "nombreDireccion": direccion.get("AddressName", ""),
                "calleNumero": direccion.get("Street", ""),
                "ciudad": direccion.get("City", ""),
                "codigoImpuesto": direccion.get("TaxCode", ""),
                "SocioNegocio": direccion.get("BPCode", ""),
                "region": direccion.get("State", ""),
                "comuna": direccion.get("County", ""),
                "tipoDireccion": tipo_direccion,  # Nuevo campo
            })

        # Empleados de contacto del socio de negocio
        empleados_contacto = []
        for contacto in data.get("ContactEmployees", []) or []:  # Asegurar que sea iterable

            empleados_contacto.append({
                "codigoInternoSap": contacto.get("InternalCode", ""),
                "nombreCompleto": contacto.get("FirstName", ""),
                "nombre": contacto.get("FirstName", ""),
                "apellido": contacto.get("LastName", ""),
                "telefono": contacto.get("Phone1", ""),
                "celular": contacto.get("Phone1", ""),
                "email": contacto.get("E_Mail", ""),
                "SocioNegocio": contacto.get("CardCode", "")
            })

        # Estructura final de salida
        resultado = {
            "SocioNegocio": socio_negocio,
            "Direcciones": direcciones,
            "Contactos": empleados_contacto
        }
        return resultado



    def guardarClienteCompleto(self, data):
        

        socio_negocio = data["SocioNegocio"]
    
        # Obtener la instancia de GrupoSNDB
        try:
            grupo = GrupoSNDB.objects.get(codigo=socio_negocio["grupoSN"]) # Cambiado de id a codigo
            tipo = TipoSNDB.objects.get(codigo=socio_negocio["tipoSN"])
            tipo_cliente = TipoClienteDB.objects.get(codigo=socio_negocio["tipoCliente"])

        except ObjectDoesNotExist:
            raise ValueError("No se encontró el grupo, tipo de socio de negocio o tipo de cliente")
            # Maneja el error según sea necesario, como lanzar una excepción o crear un nuevo grupo
        
        if socio_negocio["grupoSN"] == 105:
            cliente = SocioNegocioRepository.crearCliente(
                codigoSN=socio_negocio["codigoSN"],
                nombre=socio_negocio["nombre"],
                apellido=socio_negocio["apellido"],
                email=socio_negocio["email"],
                telefono=socio_negocio["telefono"],
                giro = socio_negocio["giro"],
                rut=socio_negocio["rut"],
                grupoSN=grupo, 
                tipoSN=tipo,
                tipoCliente=tipo_cliente
            )

        else:
            cliente = SocioNegocioRepository.crearClienteEmpresa(
                codigoSN=socio_negocio["codigoSN"],
                nombre=socio_negocio["razonSocial"],
                razonSocial=socio_negocio["razonSocial"],
                email=socio_negocio["email"],
                telefono=socio_negocio["telefono"],
                giro = socio_negocio["giro"],
                rut=socio_negocio["rut"],
                grupoSN=grupo, 
                tipoSN=tipo,
                tipoCliente=tipo_cliente
            )
            

        # Crear las direcciones asociadas al cliente usando el método del repositorio
        for direccion in data.get("Direcciones", []):
            datoComuna = direccion.get('comuna')
            # Quitar el guion y limpiar el string
            id_comuna = datoComuna.strip().split("-")[0].strip()
                        
            # Obtener la comuna del repositorio
            comuna = ComunaRepository().obtenerComunaPorId(id_comuna)
            
            if not comuna:
                comuna2 = ComunaRepository.obtenerComunaPorNombre(id_comuna)
                
            if comuna2 != 0:
                comuna_id = comuna2.codigo
            elif comuna != 0:
                comuna_id = comuna.codigo
            else:
                comuna_id = direccion["region"]

            #comuna_id = comuna.codigo if comuna != 0 else direccion["region"]            
            
            # Crear la dirección asociada
            DireccionRepository.crearDireccion(
                socio=socio_negocio["codigoSN"],
                rownum=direccion["rowNum"],
                nombre_direccion=direccion["nombreDireccion"],
                ciudad=direccion["ciudad"],
                calle_numero=direccion["calleNumero"],
                ## obtener el id de la comuna de que retona la funcion obtenerComunaPorId Comuna: ('13126', 'Quinta Normal')
                comuna_id= comuna_id,
                region_id=direccion["region"],
                tipo_direccion=direccion["tipoDireccion"],
                pais=direccion.get("pais", "Chile")  # Valor por defecto
            )

        # Crear los contactos asociados al cliente usando el método del repositorio
        for contacto in data.get("Contactos", []):
            ContactoRepository.crearContacto(
                socio=socio_negocio["codigoSN"],
                codigo_interno_sap=contacto["codigoInternoSap"],
                nombre_contacto=contacto["nombre"],
                apellido_contacto=contacto["apellido"],
                telefono_contacto=contacto["telefono"],
                email_contacto=contacto["email"],
                celular_contacto=contacto["celular"]
            )

        return cliente


    def generarCardCode(self, rut):
        """
        Método para generar el 'CardCode' de un socio de negocio.

        Args:
            rut (str): RUT del socio de negocio.

        Returns:
            str: 'CardCode' generado.
        """
        return f"{rut}C"

    def responderInfoCliente(self, rut):
        """
        Obtine y reposnde la información de un cliente existente en la base de datos.

        Args:
            socio_negocio (dict): Datos del socio de negocio.
            rut (str): RUT del cliente.

        Returns:
            JsonResponse: Respuesta con los datos del cliente si se encontró, o un mensaje de error.
        """
        data_client = self.infoCliente(rut)

        if data_client:
            return JsonResponse(data_client, status=200, safe=False)
        return JsonResponse({'success': False, 'message': 'No se encontraron resultados'}, status=404)

    def crearYresponderCliente(self, carCode, rut):
        try:
            client = APIClient()
            data = client.getInfoSN(carCode)

            if data.get('error'):
                return JsonResponse({'success': False, 'message': 'No se encontraron resultados'}, status=404)

            data_creacion = self.normalize_bp_data(self.convertirJsonObjeto(data))

            if self.guardarClienteCompleto(data_creacion):
                return self.responderInfoCliente(rut)
            else:
                return JsonResponse({'success': False, 'message': 'Error al guardar el cliente'}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear el cliente: {str(e)}'}, status=500)


    def construirFiltrosSociosNegocio(data):
        """
        Construye los filtros para la consulta de socios de negocio basados en los datos proporcionados.

        Args:
            data (dict): Datos de la consulta.

        Returns:
            dict: Filtros para la consulta de socios de negocio.
        """
        filters = {}

        filter_data = data.get('filters', {})

        name = filter_data.get('nombre')
        name_mayus = name.upper() if name else None
        name_minus = name.lower() if name else None
        name_title = name.title() if name else None

        if filter_data.get('codigo'):
            filters['contains(CardCode'] = f"'{filter_data['codigo']}')"
        if filter_data.get('nombre'):
            filters['(contains(CardName'] = f"'{name_mayus}') or contains(CardName, '{name_minus}') or contains(CardName, '{name_title}'))"
        if filter_data.get('tipo'):
            groupCode = int(filter_data['tipo'])
            filters['GroupCode eq '] = f"{groupCode} "
        if filter_data.get('telefono'):
            filters['contains(Phone1'] = f"'{filter_data['telefono']}')"
        if filter_data.get('email'):
            filters['contains(EmailAddress'] = f"'{filter_data['email']}')"

        # Limpiar filtros vacíos o inválidos
        filters = {k: v for k, v in filters.items() if v and v != "''"}

        return filters


    #Creacion Socio Negocio
    def create_or_update_bp(self):
        bp_data = self.request

        is_valid, message = self.verify_valid_rut(self.rut)
        
        if not is_valid:
            return JsonResponse({'success': False, 'message': message}, status=400)
        
        try:
            self.validate_madatary_data_bp()
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        
        rut_sap = self.rut.split("-")[0] + "C"

        exiting_bp = SocioNegocioRepository.get_by_rut(self.rut)
        exiting_bp_sap = self.verify_sap_bp(rut_sap)

        if exiting_bp_sap:
            if exiting_bp is not None:
                return self.process_existing_bp(bp_data.get('cardCodeSN'), exiting_bp, newData=bp_data)
            
            self.crearYresponderCliente(rut_sap, rut_sap)
            return JsonResponse({'success': True, 'message': 'Cliente Creado desde SAP exitosamente'})

        self.process_new_bp(SocioNegocio.generate_bp_code(self.rut), bp_data)

        return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})
        

    def process_new_bp(self, card_code, data_bp):
        # get branch from data_bp, if not found, generate a new one for default
        sales_branch = data_bp.get('sucursal', None)

        if not data_bp.get('direcciones'):
                data_bp['direcciones'] = Direccion.generate_store_address(sales_branch)
                print(f"Direcciones: {data_bp['direcciones']}")

                # convert data to json, and create the business partner in SAP
        json_data_bp = BusinessPartnerSerializer.serializer_bp(data_bp, card_code)

        response_json_bp = self.create_sap_bp(json_data_bp)

        if not response_json_bp.get('CardCode'):
            raise ValueError("Error al crear el socio de negocio en SAP")

        # process the data to save in the database
        normalize_data_bp = self.normalize_bp_data(self.convertirJsonObjeto(response_json_bp))
        business_partner = self.guardarClienteCompleto(normalize_data_bp)

        return business_partner



    def procesarDirecciones(data, socio):
        
        try:
            direcciones_json = data.get("direcciones")

            if not direcciones_json:
                return JsonResponse({"success": False, "message": "No se encontraron direcciones en el request.", }, status=400)

            direcciones = json.loads(direcciones_json[0])
            
            DireccionRepository.eliminarDireccionesPorSocio(socio)

            for direccion in direcciones:

                tipoDire = direccion.get("tipoDireccion")

                if tipoDire == "bo_BillTo":
                    
                    tipoDireccion = "13"
                    
                else:
                    tipoDireccion = "12"


                datoComuna = direccion.get('comuna')
                                
                # quitar el guion y limpiar el string
                id_comuna = datoComuna.strip().split("-")[0].strip()
                comunas = ComunaRepository().obtenerComunaPorId(id_comuna)

                rownum = direccion.get("row_id")
                nombre_direccion = direccion.get("nombreDireccion")
                ciudad = direccion.get("ciudad")
                pais = direccion.get("pais")
                region = direccion.get("region")
                comuna = comunas.codigo
                direccion = direccion.get("direccion")
                tipo = tipoDireccion
                
                if nombre_direccion:
                    
                    try:
                        DireccionRepository.crearDireccion(socio, rownum, nombre_direccion, ciudad, direccion, comuna, region, tipo, pais)
                    except Exception as e:
                        print(f"Ocurrió un error al crear la dirección: {str(e)}")
                else:
                    print(f"No se procesó la dirección el nombre está vacío.")

            return {"data": {"success": True, "message": "Direcciones procesadas con éxito.",}, "status": 200}
        
        except KeyError as e:
            return {"data": {"success": False, "message": f"Falta el campo: {str(e)}",}, "status": 400}
        
        except json.JSONDecodeError as e:
            return {"data": {"success": False, "message": f"Error al decodificar JSON: {str(e)}",}, "status": 400}



    def syncBusinessPartners(self):
        state, created = SyncState.objects.get_or_create(
            key="syncPartnersBusiness",
            defaults={"value": 0}
        )

        skip = state.value
        totalSynced = 0

        apiClientSL = APIClient()
        
        count = apiClientSL.getQuantityBusinessPartners()

        if not isinstance(count, dict) or 'value' not in count or not count['value']:
            return {"success": False, "message": "No se encontraron socios de negocio en SAP."}

        totalBP = count['value'][0].get('BusinessPartners', 0)
        
        if skip >= totalBP:
            skip = 0
            state.value = 0
            state.save()

        try:
            # Obtener los socios de negocio desde SAP
            bp = apiClientSL.getBusinessPartners(skip=skip)
            
            if not bp or 'value' not in bp:
                return {"success": False, "message": "No se encontraron socios de negocio en SAP."}
            
            # Ajuste para procesar cada elemento dentro de 'value'
            for partner_data in bp['value']:
                # Convertir cada objeto JSON de la lista en un objeto manejable
                partner_object = self.convertirJsonObjeto(partner_data)

                # Procesar y guardar cada socio de negocio
                processed_data = self.normalize_bp_data(partner_object)

                try:
                    client = self.guardarClienteCompleto(processed_data)
                    if client:
                        totalSynced += 1
                except Exception as e:
                    logging.error(f"Error al sincronizar socio {partner_object.get('CardCode')}: {str(e)}")
                    continue  # Evita que un error detenga la sincronización

            if totalSynced > 0:
                state.value = skip + totalSynced
                state.save()
                logging.info(f"{totalSynced} socios de negocio sincronizados con éxito.")

            return {"success": True, "message": f"{totalSynced} socios de negocio sincronizados con éxito."}

        except Exception as e:
            logging.error(f"Error general en la sincronización: {str(e)}")
            return {"success": False, "message": "Ocurrió un error en la sincronización."}

    @staticmethod
    def get_clen_carCode(identificado_bp):

        cardCode = identificado_bp.strip()
        cardCode = cardCode.replace(" ", "").replace(".", "").rstrip("Cc")
        cardCode = re.sub(r'-\d+$', '', cardCode)
        cardCode = re.sub(r'-\w+$', '', cardCode)
        
        return cardCode





