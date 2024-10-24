import json
import logging
from venv import logger
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError
from datosLsApp.models.socionegociodb import SocioNegocioDB
from datosLsApp.repositories.socionegociorepository import SocioNegocioRepository
from datosLsApp.repositories.gruposnrepository import GrupoSNRepository
from datosLsApp.repositories.tipoclienterepository import TipoClienteRepository
from datosLsApp.repositories.tiposnrepository import TipoSNRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.models import DireccionDB, ContactoDB
from adapters.sl_client import APIClient


class SocioNegocio:
    """
    Clase para la lógica de negocio de los socios de negocio.

    Metodos disponibles:

    - validarDatosObligatorios()
    - crearOActualizarCliente()
    - obtenerGrupoSN()
    - obtenerTipoCliente()
    - procesarClienteExistente(codigosn)
    - obtenerTipoSN()
    - crearNuevoCliente(codigosn, tiposn, grupoSN, tipoCliente)
    - manejarErrorValidacion(e)
    - manejarErrorGeneral(e)
    - crearClientePersona(self, codigosn, rut, tiposn, tipocliente, email, grupoSN)
    - crearClienteEmpresa(self, codigosn, tiposn, grupoSN, tipoCliente)
    - validardatosObligatorios(self)
    - generarCodigoSN(rut)
    - agregarDireccionYContacto(request, cliente)
    - buscarSocioNegocio(identificador, buscar_por_nombre=False)
    - formatear_direcciones(direcciones)
    - formatear_contactos(contactos)
    - validarGrupoSN(self)
    - validarRut(self)
    - validarEmail(self)
    - verificarSocioNegocioSap(cardCode)
    - prepararJsonCliente(jsonData)
    - creacionSocioSAP(data)
    - verificarRutValido(rut)
    - procesarDirecciones(data, socio)
    - procesarContactos(data, socio)
    """
    def __init__(self, request):
        """
        Constructor de la clase SocioNegocio

        Args:
            request (HttpRequest): Request de la vista.

        Attributes:
            request (HttpRequest): Request de la vista.
            gruposn (str): Código del grupo de socio de negocio.
            rut (str): RUT del cliente.
            email (str): Email del cliente.
            nombre (str): Nombre del cliente.
            apellido (str): Apellido del cliente.
            razon_social (str): Razón social del cliente.
            giro (str): Giro del cliente.
            telefono (str): Teléfono del cliente.
        """

        self.request = request
        self.gruposn = request.POST.get('grupoSN')
        self.rut = request.POST.get('rutSN')
        self.email = request.POST.get('emailSN')
        self.nombre = request.POST.get('nombreSN')
        self.apellido = request.POST.get('apellidoSN')
        self.razon_social = request.POST.get('grupoSN')
        self.giro = request.POST.get('giroSN')
        self.telefono = request.POST.get('telefonoSN')
        
        
    def validarDatosObligatorios(self):
        """
        Metodo para validar los datos obligatorios

        Raises:
            ValidationError: Si algún dato obligatorio no se encuentra.
        """

        self.validarGrupoSN()
        self.validarRut()
        self.validarEmail()


    def crearOActualizarCliente(self):
        """
        Método para crear o actualizar un cliente en la base de datos.

        args:
            request (HttpRequest): Request de la vista.

        Returns:
            Si el cliente se creó exitosamente, retorna un JsonResponse con un mensaje de éxito.
            Si hubo un error, retorna un JsonResponse con un mensaje de error y un código de estado 400 o 500.
        """

        rutVerificado = self.verificarRutValido(self.rut)
        
        print(f"Rut verificado: {rutVerificado}")
        if not rutVerificado:
            return JsonResponse({'success': False, 'message': 'RUT inválido'}, status=400)

        try:
            print("Creando o actualizando cliente...")
            print(f"validando datos obligatorios")
            self.validarDatosObligatorios()
            print(f"Datos obligatorios validados")
            codigosn = SocioNegocio.generarCodigoSN(self.rut)
            print(f"Código de socio de negocio: {codigosn}")
            grupoSN = self.obtenerGrupoSN()
            print(f"Grupo de socio de negocio: {grupoSN}")
            tipoCliente = self.obtenerTipoCliente()
            print(f"Tipo de cliente: {tipoCliente}")

            clienteExistente = SocioNegocioRepository.obtenerPorRut(self.rut)

            print(f"Cliente existente: {clienteExistente}")

            if clienteExistente is not None:
                print("Cliente existente encontrado")
                return self.procesarClienteExistente(codigosn)

            tiposn = self.obtenerTipoSN()

            with transaction.atomic():
                print("Creando nuevo cliente...")
                cliente = self.crearNuevoCliente(codigosn, tiposn, grupoSN, tipoCliente)

                
                print

                print(f"Cliente creado: {cliente}")

                print("Creando cliente en SAP...")
                json_data = self.prepararJsonCliente(self.request.POST)
                self.creacionSocioSAP(json_data)
                print("Cliente creado en SAP")
            
                return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})

        except ValidationError as e:
            return self.manejarErrorValidacion(e)
        except Exception as e:
            return self.manejarErrorGeneral(e)

    def obtenerGrupoSN(self):
        """
        Método para obtener el grupo de socio de negocio.

        Raises:
            ValidationError: Si el grupo de socio de negocio no se encuentra.

        Returns:
            GrupoSNDB: Grupo de socio de negocio.
        """
        grupoSN = GrupoSNRepository.obtenerGrupoSNPorCodigo(self.gruposn)
        if not grupoSN:
            raise ValidationError(f"Grupo de socio de negocio no encontrado para el código: {self.gruposn}")
        return grupoSN

    def obtenerTipoCliente(self):
        """
        Método para obtener el tipo de cliente 'Natural'.

        Raises:
            ValidationError: Si el tipo de cliente no se encuentra.

        Returns:
            TipoClienteDB: Tipo de cliente 'Natural'.

        """
        tipoCliente = TipoClienteRepository.obtenerTipoClientePorCodigo('N')
        if not tipoCliente:
            raise ValidationError("Tipo de cliente no encontrado")
        return tipoCliente

    def procesarClienteExistente(self, codigosn):

        print("Procesando cliente existente...")
        verificacionSap = self.verificarSocioNegocioSap(codigosn)
        print(f"Verificación en SAP: {verificacionSap}")
        print(f"cogidoSN: {codigosn}")

        if verificacionSap:
            print("Cliente ya existe en SAP y en la base de datos")
            return JsonResponse({'success': True, 'message': 'Cliente ya existe en SAP y en la base de datos'})
        
        else:
            print("Cliente ya existe en la base de datos, pero no en SAP")
            json_data = self.prepararJsonCliente(self.request.POST)
            self.creacionSocioSAP(json_data)
            return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})

    def obtenerTipoSN(self):
        tiposn = TipoSNRepository.obtenerTipoSnPorCodigo('C' if self.gruposn == '100' else 'I')
        if not tiposn:
            raise ValidationError(f"Tipo de socio de negocio no encontrado para el código: {'C' if self.gruposn == '100' else 'I'}")
        return tiposn

    def crearNuevoCliente(self, codigosn, tiposn, grupoSN, tipoCliente):
        with transaction.atomic():
            if self.gruposn == '100':
                cliente = self.crearClientePersona(self, codigosn, self.rut, tiposn, tipoCliente, self.email, grupoSN)
                
            elif self.gruposn == '105':
                cliente = self.crearClienteEmpresa(self, codigosn, tiposn, grupoSN, tipoCliente)
            else:
                raise ValidationError(f"Grupo de cliente no válido: {self.gruposn}")

            SocioNegocio.agregarDireccionYContacto(self.request, cliente)

        return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})

    def manejarErrorValidacion(self, e):
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def manejarErrorGeneral(self, e):
        return JsonResponse({'success': False, 'message': 'Error al crear el cliente'}, status=500)


    @staticmethod
    def crearClientePersona(self, codigosn, rut, tiposn, tipocliente, email, grupoSN):
        """
        Método para crear un cliente persona.
        
        Args:
            codigosn (str): Código del socio de negocio.
            rut (str): RUT del cliente.
            tiposn (TipoSNDB): Tipo de socio de negocio.
            tipocliente (TipoClienteDB): Tipo de cliente.
            email (str): Email del cliente.
            grupoSN (GrupoSNDB): Grupo de socio de negocio.

        Returns:
            Si el cliente se creó exitosamente, retorna un JsonResponse con un mensaje de éxito.
            Si hubo un error, retorna un JsonResponse con un mensaje de error y un código de estado 400 o 500.
        """

        return SocioNegocioRepository.crearCliente(
            codigoSN=codigosn, nombre=self.nombre, apellido=self.apellido, rut=rut, giro=self.giro,
            telefono=self.telefono, email=email, grupoSN=grupoSN, tipoSN=tiposn,
            tipoCliente=tipocliente
        )

    @staticmethod
    def crearClienteEmpresa(self, codigosn, tiposn, grupoSN, tipoCliente):
        """
        Método para crear un cliente empresa.

        Args:
            codigosn (str): Código del socio de negocio.
            tiposn (TipoSNDB): Tipo de socio de negocio.
            grupoSN (GrupoSNDB): Grupo de socio de negocio.
            tipoCliente (TipoClienteDB): Tipo de cliente.

        Returns:
            Si el cliente se creó exitosamente, retorna un JsonResponse con un mensaje de éxito.
            Si hubo un error, retorna un JsonResponse con un mensaje de error y un código de estado
        """

        print(f"Creando cliente empresa - Razón Social: {self.razon_social}, RUT: {self.rut}, Email: {self.email}")
        return SocioNegocioRepository.crearCliente(
            codigoSN=codigosn, nombre=self.nombre, razonSocial=self.nombre, rut=self.rut, giro=self.giro,
            telefono=self.telefono, email=self.email, grupoSN=grupoSN, tipoSN=tiposn,
            tipoCliente=tipoCliente
        )


    @staticmethod
    def validardatosObligatorios(self):
        """
        Método para validar los datos obligatorios.

        args:
            request (HttpRequest): Request de la vista.

        Raises:
            ValidationError: Si algún dato obligatorio no se encuentra.

        Returns:
            Tuple: Tupla con los datos obligatorios.
        """

        gruposn = self.request.POST.get('grupoSN')
        rut = self.request.POST.get('rutSN')
        email = self.request.POST.get('emailSN')

        if not all([gruposn, rut, email]):
            print("Datos obligatorios faltantes")
            raise ValidationError("Faltan datos obligatorios")
        return gruposn, rut, email

    @staticmethod
    def generarCodigoSN(rut):

        """
        Método para generar el código de socio de negocio.

        Args:
            rut (str): RUT del cliente.
        
        Returns:
            str: Código de socio de
        """

        rut_sn = rut.split("-")[0] if "-" in rut else rut
        return rut_sn.replace(".", "") + 'C'

    @staticmethod
    def agregarDireccionYContacto(request, cliente):
        """
        Método para agregar una dirección y un contacto a un cliente.

        Args:
            request (HttpRequest): Request de la vista.
            cliente (SocioNegocioDB): Cliente al que se le agregará la dirección y el contacto.
        
        Raises:
            ValidationError: Si no se encuentra la dirección o el contacto.

        Returns:
            si la dirección y el contacto se agregaron exitosamente, retorna un JsonResponse con un mensaje de éxito.
            Si hubo un error, retorna un JsonResponse con un mensaje de error y un código de estado 400 o 500.
        """

        print("Agregando dirección y contacto...")
        print(f"dirección: {request.POST.get('nombre_direccion[]')}")
        from showromVentasApp.views.view import agregarDireccion, agregarContacto

        if 'nombre_direccion[]' not in request.POST:
            print("Dirección faltante")
            raise ValidationError("Debe agregar al menos una dirección")
        agregarDireccion(request, cliente)

        if 'nombre' not in request.POST:
            agregarContacto(request, cliente)
        else:
            print("Contacto faltante")
            raise ValidationError("Debe agregar al menos un contacto")


    def buscarSocioNegocio(identificador, buscar_por_nombre=False):
        """
        Método para buscar un socio de negocio por nombre o rut.

        Args:
            identificador (str): Nombre o rut del socio de negocio.
            buscar_por_nombre (bool): Indica si se busca por nombre o por rut.

        Returns:
            Si se encontraron resultados, retorna un diccionario con los datos de los socios de negocio.
            Si no se encontraron resultados, retorna una lista vacía.
        """
        print(f"identificador: {identificador}")

        try:
            if buscar_por_nombre:
                # Si se busca por nombre, usa el repositorio que busca por nombre
                resultados_clientes = SocioNegocioRepository.buscarClientesPorNombre(identificador)
            else:
                print("Buscando por rut")
                # Si no, se busca por rut (número)
                resultados_clientes = SocioNegocioRepository.buscarClientesPorRut(identificador)

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

                # Agregar el socio formateado al resultado
                resultados_formateados.append({
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

            return resultados_formateados
        
        except Exception as e:
            logging.error(f"Error al buscar socio negocio: {e}")
            return {'error': 'Ocurrió un error al realizar la búsqueda'}

    @staticmethod
    def formatear_direcciones(direcciones):
        """
        Método para formatear las direcciones de un socio de negocio.

        Args:
            direcciones (QuerySet): Direcciones del socio de negocio.

        Returns:
            List: Lista con las direcciones formateadas.
        """

        return [{
            "id": direccion.id,
            'rowNum': direccion.rowNum,
            'nombreDireccion': direccion.nombreDireccion,
            'ciudad': direccion.ciudad,
            'calleNumero': direccion.calleNumero,
            'codigoImpuesto': direccion.codigoImpuesto,
            'tipoDireccion': direccion.tipoDireccion,
            'pais': direccion.pais,
            'comuna': direccion.comuna.nombre,
            'region': direccion.region.nombre
        } for direccion in direcciones]

    @staticmethod
    def formatear_contactos(contactos):
        """
        Método para formatear los contactos de un socio de negocio.

        Args:
            contactos (QuerySet): Contactos del socio de negocio.

        Returns:
            List: Lista con los contactos formateados.
        """

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


    
    def validarGrupoSN(self):
        """
        Método para validar el grupo de socio de negocio.

        Raises:
            ValidationError: Si el grupo de socio de negocio no se encuentra.
        """

        if not self.gruposn:
            raise ValidationError("Grupo de socio de negocio no encontrado")
    
    def validarRut(self):
        """
        Método para validar el RUT del cliente.
        
        Raises:
            ValidationError: Si el RUT no se encuentra.
        """

        if not self.rut:
            raise ValidationError("RUT no encontrado")
        
    def validarEmail(self):
        """
        Metodo para validar el email del cliente.

        Raises:
            ValidationError: Si el email no se encuentra.
        """

        if not self.email:
            raise ValidationError("Email no encontrado")
        
        
    def verificarSocioNegocioSap(self, cardCode):
        """
        
        Método para verificar si un socio de negocio existe en SAP.
        
        Args:
            cardCode (str): Código del socio de negocio.
            
        Returns:
            bool: True si el socio de negocio existe, False si no.            
        """

        client = APIClient()

        try:
            print("Verificando socio de negocio en SAP...")
            
            response = client.verificarCliente(endpoint="BusinessPartners", cardCode=cardCode)
            print(f"Response: {response}")

            # Verifica si la respuesta contiene el 'CardCode'
            if 'CardCode' in response:
                print(f"Socio de negocio encontrado: {response['CardCode']}")
                return True
            else:
                print("Socio de negocio no encontrado.")
                return False
        except Exception as e:
            print(f"Error al verificar socio de negocio en SAP: {str(e)}")
            return False
    
    def prepararJsonCliente(self, jsonData):

        """
        Prepara los datos JSON específicos de la cotización.

        Args:
            jsonData (dict): Datos de la cotización.
        
        Returns:
            dict: Datos de la cotización preparados para ser enviados a SAP.
        """
        
        # Datos de la cabecera
        print("Preparando JSON para el socio de negocio...")
        print(f"Datos recibidos: {jsonData}")
        cardCode = jsonData.get('rutSN')
        print(f"CardCode: {cardCode}")

        nombre = jsonData.get('nombreSN')
        apellido = jsonData.get('apellidoSN')

        # Obtener cliente
        try:
            cliente = SocioNegocioDB.objects.get(rut=cardCode)  # Asumiendo que 'rut' es el identificador único
            print(f"Cliente: {cliente}")
        except SocioNegocioDB.DoesNotExist:
            raise ValueError(f"No se encontró el cliente con RUT: {cardCode}")

        # Instancia del repositorio de direcciones
        direccion_repo = DireccionRepository()
        
        # Obtener direcciones y contactos
        direcciones = direccion_repo.obtenerDireccionesPorCliente(cliente)
        contactos = ContactoRepository().obtenerContactosPorCliente(cliente)

        nombreCompleto = "{nombre} {apellido}".format(nombre=nombre, apellido=apellido)
        cardCodeSinGuion = self.generarCodigoSN(cardCode)
        
        if not cardCode:
            raise ValueError("El campo 'CardCode' es obligatorio.")

        # Preparar cabecera
        cabecera = {
            'CardCode': cardCodeSinGuion,
            'CardName': nombreCompleto,
            'CardType': "C",
            'GroupCode': jsonData.get('grupoSN'),
            'Phone1': jsonData.get('telefonoSN'),
            'Phone2': jsonData.get('telefonoSN'),
            'Notes': "Persona",
            'PayTermsGrpCode': -1,
            'FederalTaxID': jsonData.get('rutSN'),
            'SalesPersonCode': -1,  # Cambiar por el código de vendedor
            'Cellular': jsonData.get('telefonoSN'),
            'EmailAddress': jsonData.get('emailSN'),
            'CardForeignName': nombreCompleto,
            'ShipToDefault': jsonData.get('nombre_direccion[]'),
            'BilltoDefault': jsonData.get('nombre_direccion[]'),
            'DunningTerm': "ESTANDAR",
            'CompanyPrivate': "cPrivate",
            'AliasName': jsonData.get('nombreSN'),
            'U_Tipo': "N",
            'U_FE_Export': "N",
        }

        # Preparar direcciones
        bp_addresses_json = []
        for direccion in direcciones:
            tipoDireccion = 'bo_BillTo' if direccion.tipoDireccion == 'F' else 'bo_ShipTo'
            
            # Crear un diccionario por cada dirección
            bp_addresses_json.append({
                'AddressName': direccion.nombreDireccion,
                'Street': direccion.calleNumero,
                'City': direccion.codigoImpuesto,
                'County': direccion.pais,
                'Country': "CL", # Cambiar por el código de país
                'State': direccion.region.numero,
                'FederalTaxID': direccion.SocioNegocio.rut,
                'TaxCode': "IVA", # Cambiar por el código de impuesto
                'AddressType': tipoDireccion,
            })

        # Preparar contactos
        contact_employees_json = [
            {
                'Name': contacto.nombreCompleto,
                'Phone1': contacto.telefono,
                'MobilePhone': contacto.celular,
                'E_Mail': contacto.email,
                'FirstName': contacto.nombre,
                'LastName': contacto.apellido,
            }
            for contacto in contactos
        ]

        # Combina cabecera y líneas en un solo diccionario
        return {
            **cabecera,
            'BPAddresses': bp_addresses_json,
            'ContactEmployees': contact_employees_json
        }

    
    def creacionSocioSAP(self, data):
        """
        Método para crear un socio de negocio en SAP.

        Args:
            data (dict): Datos del socio de negocio.

        Returns:
            si el socio de negocio se creó exitosamente, retorna un diccionario con un mensaje de éxito y el 'CardCode'.
            Si hubo un error, retorna un diccionario con un mensaje de error.
        """

        client = APIClient()
        
        try:
            print("Creando socio de negocio en SAP...")


            # Enviar solicitud a SAP
            print(f"Datos a enviar: {data}")
            response = client.crearCliente(data)
            print(f"Respuesta de la API: {response}")
            
            if isinstance(response, dict):
                # Verificar si la respuesta contiene un 'CardCode'
                if 'CardCode' in response:
                    card_code = response.get('CardCode')
                    print(f"Socio de negocio creado exitosamente con CardCode: {card_code}")
                    
                    # Extraer BPAddresses si está presente
                    bp_addresses = response.get('BPAddresses', [])
                    row_nums = [address.get('RowNum') for address in bp_addresses if 'RowNum' in address]
                    
                    # Extraer ContactEmployees si está presente
                    contact_employees = response.get('ContactEmployees', [])
                    internal_codes = [employee.get('InternalCode') for employee in contact_employees if 'InternalCode' in employee]


                    return {
                        'success': 'Socio de negocio creado exitosamente',
                        'CardCode': card_code,
                        'RowNums': row_nums,  # Lista con los RowNum extraídos
                        'InternalCodes': internal_codes  # Lista con los InternalCode extraídos

                    }
                
                # Manejar el mensaje de error si lo hay
                elif 'error' in response:
                    error_message = response.get('error', 'Error desconocido')
                    print(f"Error devuelto por la API: {error_message}")
                    return {'error': f"Error: {error_message}"}
                else:
                    print("Respuesta inesperada de la API.")
                    return {'error': 'Respuesta inesperada de la API.'}
            
            else:
                print("La respuesta de la API no es válida o no es un diccionario.")
                return {'error': 'La respuesta de la API no es válida.'}

        except json.JSONDecodeError as e:
            print(f"Error al decodificar el JSON: {str(e)}")
            return {'error': 'Error al decodificar el JSON.'}
        except ConnectionError as e:
            print(f"Error de conexión con SAP: {str(e)}")
            return {'error': 'Error de conexión con SAP.'}
        except Exception as e:
            print(f"Error general al crear socio de negocio en SAP: {str(e)}")
            return {'error': f"Error inesperado: {str(e)}"}

    def verificarRutValido(self, rut):
        """
        Método para verificar si un RUT es válido.

        Args:
            rut (str): RUT a verificar. Debe tener el formato "XXXXXXXX-X".

        Returns:
            bool: True si el RUT es válido, False si no.
        """
        try:
            # RUT sin puntos y guion
            rut = rut.replace(".", "").replace("-", "")
            
            # Separar el dígito verificador del número base
            numero, digito_verificador = rut[:-1], rut[-1].upper()

            #numero base en entero
            numero = int(numero)
            
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
            return digito_calculado == digito_verificador

        except Exception as e:
            print(f"Error al verificar RUT: {str(e)}")
            return False

    def procesarDirecciones(data, socio):

        try:
            # Obtener la lista de direcciones como JSON
            direcciones_json = data.getlist('direcciones')
            
            if not direcciones_json:
                return JsonResponse({'success': False, 'message': 'No se encontraron direcciones en el request.'}, status=400)
            
            # Deserializar el JSON
            direcciones = json.loads(direcciones_json[0])
            print(f"Direcciones deserializadas: {direcciones}")
            
            # Extraer campos relevantes
            tipo = [direccion.get('tipoDireccion') for direccion in direcciones]
            nombre_direccion = [direccion.get('nombreDireccion') for direccion in direcciones]
            ciudad = [direccion.get('ciudad') for direccion in direcciones]
            pais = [direccion.get('pais') for direccion in direcciones]
            region = [direccion.get('region') for direccion in direcciones]
            comuna = [direccion.get('comuna') for direccion in direcciones]
            direccion = [direccion.get('direccion') for direccion in direcciones]
            
            # Verificar que las listas tienen la misma longitud
            if not all(len(lst) == len(nombre_direccion) for lst in [ciudad, direccion, tipo, pais, region, comuna]):
                return {'data': {'success': False, 'message': 'Las listas deben tener la misma longitud.'}, 'status': 400}

            # Procesar cada dirección
            for i in range(len(nombre_direccion)):
                nombredire = nombre_direccion[i].strip()
                
                if nombredire:
                    direccion_id = direcciones[i].get('direccionId')

                    if direccion_id:
                        # Obtener la dirección existente
                        direccion_obj = DireccionRepository.obtenerDireccion(direccion_id)

                        # Actualizar si existe, o crear si no
                        if direccion_obj:
                            DireccionRepository.actualizarDireccion(direccion_obj, nombredire, ciudad[i], direccion[i], comuna[i], region[i], tipo[i], pais[i])
                    else:
                        # Crear la dirección
                        try:
                            DireccionRepository.crearDireccion(socio, nombredire, ciudad[i], direccion[i], comuna[i], region[i], tipo[i], pais[i])
                        except Exception as e:
                            print(f"Ocurrió un error al crear la dirección: {str(e)}")
                else:
                    print(f"No se procesó la dirección {i+1} porque el nombre está vacío.")

            return {'data': {'success': True, 'message': 'Direcciones procesadas con éxito.'}, 'status': 200}
        except KeyError as e:
            return {'data': {'success': False, 'message': f'Falta el campo: {str(e)}'}, 'status': 400}
        except json.JSONDecodeError as e:
            return {'data': {'success': False, 'message': f'Error al decodificar JSON: {str(e)}'}, 'status': 400}
        
    def procesarContactos(data, socio):

        print("Procesando contactos...")
        try:
            contactos_json = data.getlist('contactos')
            print(f"Contactos JSON: {contactos_json}")

            if not contactos_json:
                return JsonResponse({'success': False, 'message': 'No se encontraron contactos en el request.'}, status=400)

            contactos = json.loads(contactos_json[0])

            # Extraer los valores necesarios desde el JSON deserializado
            nombres = [contacto.get('nombre', '').strip() for contacto in contactos]
            apellidos = [contacto.get('apellido', '').strip() for contacto in contactos]
            telefonos = [contacto.get('telefono', '').strip() for contacto in contactos]
            celulares = [contacto.get('celular', '').strip() for contacto in contactos]
            emails = [contacto.get('email', '').strip() for contacto in contactos]

            # Verifica la longitud de todas las listas
            if not all(len(lst) == len(nombres) for lst in [apellidos, telefonos, celulares, emails]):
                print("Las listas deben tener la misma longitud.")
                return JsonResponse({'success': False, 'message': 'Las listas deben tener la misma longitud.'}, status=400)

            for i in range(len(nombres)):
                nombre = nombres[i]

                if nombre:
                    contacto_id = contactos[i].get('contacto_id')

                    if contacto_id:
                        contacto_obj = ContactoRepository.obtenerContacto(contacto_id)

                        if contacto_obj:
                            print(f"Actualizando contacto {i+1}...")
                            ContactoRepository.actualizarContacto(contacto_obj, nombre, apellidos[i], telefonos[i], celulares[i], emails[i])
                    else:
                        try:
                            ContactoRepository.crearContacto(socio, nombre, apellidos[i], telefonos[i], emails[i], celulares[i])
                        except Exception as e:
                            print(f"Error al crear el contacto: {str(e)}")
                            return JsonResponse({'success': False, 'message': f'Error al crear el contacto: {str(e)}'}, status=500)

                else:
                    print(f"No se procesó el contacto {i+1} porque el nombre o apellido está vacío.")

            return {'data': {'success': True, 'message': 'Direcciones procesadas con éxito.'}, 'status': 200}
        
        except KeyError as e:
            return {'data': {'success': False, 'message': f'Falta el campo: {str(e)}'}, 'status': 400}
        except json.JSONDecodeError as e:
            return {'data': {'success': False, 'message': f'Error al decodificar JSON: {str(e)}'}, 'status': 400}


    def infoCliente(self, identificador, buscar_por_nombre=False):
        """
        Método para buscar un socio de negocio por nombre o rut.

        Args:
            identificador (str): Nombre o rut del socio de negocio.
            buscar_por_nombre (bool): Indica si se busca por nombre o por rut.

        Returns:
            list: Lista de diccionarios con los datos de los socios de negocio.
            dict: Diccionario con error en caso de excepción.
        """
        logger.info(f"Buscando socio negocio - Identificador: {identificador}, "
                f"Buscar por nombre: {buscar_por_nombre}")

        try:
            # Validar que el identificador no esté vacío
            if not identificador or not identificador.strip():
                return {'error': 'El identificador está vacío'}

            # Realizar la búsqueda según el tipo
            if buscar_por_nombre:
                resultados_clientes = SocioNegocioRepository.buscarClientesPorNombre(identificador)
            else:
                resultados_clientes = SocioNegocioRepository.buscarClientesPorRut(identificador)

            # Si no hay resultados, retornar lista vacía
            if not resultados_clientes:
                logger.info(f"No se encontraron resultados para el identificador: {identificador}")
                return []

            resultados_formateados = []

            # Procesar cada socio encontrado
            for socio in resultados_clientes:
                try:
                    # Prefetch de direcciones y contactos
                    direcciones = DireccionDB.objects.filter(
                        SocioNegocio=socio
                    ).select_related('comuna', 'region')
                    
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
                        'contactos': contactos_formateados
                    }
                    
                    resultados_formateados.append(socio_formateado)
                    
                except Exception as e:
                    logger.error(f"Error al formatear socio {socio.rut}: {str(e)}")
                    continue

            return resultados_formateados

        except Exception as e:
            logger.error(f"Error al buscar socio negocio: {str(e)}")
            return {'error': f'Error al realizar la búsqueda: {str(e)}'}