import json
import logging
from venv import logger
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.exceptions import ValidationError
from adapters.serializador import Serializador
from datosLsApp.models.gruposndb import GrupoSNDB
from datosLsApp.models.socionegociodb import SocioNegocioDB
from datosLsApp.models.tipoclientedb import TipoClienteDB
from datosLsApp.models.tiposndb import TipoSNDB
from datosLsApp.repositories.socionegociorepository import SocioNegocioRepository
from datosLsApp.repositories.gruposnrepository import GrupoSNRepository
from datosLsApp.repositories.tipoclienterepository import TipoClienteRepository
from datosLsApp.repositories.tiposnrepository import TipoSNRepository
from datosLsApp.repositories.direccionrepository import DireccionRepository
from datosLsApp.repositories.contactorepository import ContactoRepository
from datosLsApp.models import DireccionDB, ContactoDB
from adapters.sl_client import APIClient


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
            # Atributos inicializados como None por defecto
            self.gruposn = None
            self.rut = None
            self.email = None
            self.nombre = None
            self.apellido = None
            self.razon_social = None
            self.giro = None
            self.telefono = None
        
        
    def validarDatosObligatorios(self):
        """
        Metodo para validar los datos obligatorios

        Raises:
            ValidationError: Si algún dato obligatorio no se encuentra.
        """

        self.validarGrupoSN()
        self.validarRut()
        self.validarEmail()
        self.validarNombre()
        self.validarApellido()
        self.validarTelefono()
        self.tamañotelefono()        

    def procesarClienteExistente(self, codigosn, datosCliente, datosNuevos):

        print("Procesando cliente existente...")

        try:
            verificacionSap = self.verificarSocioNegocioSap(codigosn)
            logger.info(f"Resultado de verificación en SAP: {verificacionSap}")

            if verificacionSap:
                # Actualizar cliente en la base de datos
                if not self.actualizarSocioNegocio(codigosn, datosNuevos):
                    raise ValueError("Error al actualizar el cliente en la base de datos")
                
                return JsonResponse({'success': True, 'message': 'Cliente actualizado exitosamente'})

            json_data = self.prepararJsonCliente(datosCliente)
            self.creacionSocioSAP(json_data)
            return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})
            
        except ConnectionError as e:
            return JsonResponse({'success': False, 'message': 'Error de conexión con SAP'}, status=500)
        except ValueError as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Ocurrio un erro inesperado'}, status=500)

    def actualizarSocioNegocio(self, cardcode, datos):

        print("Actualizando socio de negocio...")
        print(f"Datos recibidos: {datos}")

        repo = SocioNegocioRepository()

        try:
            # Verificar grupo de cliente
            grupo_sn = datos.get('tipoSN')

            if not grupo_sn:
                raise ValueError("El atributo 'gruposn' no está definido o es inválido.")

            print(f"Grupo de cliente: {grupo_sn}")
            # Determinar tipo de cliente
            if grupo_sn == '105':

                logger.info("Actualizando cliente persona...")
                
                conexionSL = APIClient()

                serializer = Serializador(formato='json')

                datosSerializados = serializer.serializar(datos, cardcode)

                print(f"Datos serializados para la API: {datosSerializados}")

                logger.info(f"Datos serializados para la API: {datosSerializados}")
                
                response = conexionSL.actualizarSocioNegocioSL(cardcode, datosSerializados)

                return repo.actualizarCliente(cardcode, datos)
            else:
                logger.info("Actualizando cliente empresa...")
                return repo.actualizarClienteEmpresa(cardcode, datos)

        except ValueError as ve:
            logger.error(f"Error de validación: {str(ve)}")
            return {'success': False, 'message': f"Error de validación: {str(ve)}"}

        except Exception as e:
            logger.error(f"Error inesperado al actualizar socio de negocio: {str(e)}")
            return {'success': False, 'message': f"Error inesperado: {str(e)}"}



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

    def obtenerTipoSN(self):
        tiposn = TipoSNRepository.obtenerTipoSnPorCodigo('C' if self.gruposn == '100' else 'I')
        if not tiposn:
            raise ValidationError(f"Tipo de socio de negocio no encontrado para el código: {'C' if self.gruposn == '100' else 'I'}")
        return tiposn

    def crearNuevoCliente(self, codigosn, tiposn, grupoSN, tipoCliente):
        print("Creando nuevo cliente...")
        print(f"Grupo de cliente: {grupoSN}")
        
        with transaction.atomic():

            if self.gruposn == '105':
                print("creando cliente persona")
                cliente = self.crearClientePersona(codigosn, self.rut, tiposn, tipoCliente, self.email, grupoSN)
                
            elif self.gruposn == '100':
                print("creando cliente empresa")
                cliente = self.crearClienteEmpresa(codigosn, tiposn, grupoSN, tipoCliente)
            else:
                raise ValidationError(f"Grupo de cliente no válido: {self.gruposn}")
            SocioNegocio.agregarDireccionYContacto(self.request, cliente)
            print("Cliente creado exitosamente.")
            print(f"Cliente creado: {cliente}")

        return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})

    def manejarErrorValidacion(self, e):
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def manejarErrorGeneral(self, e):
        return JsonResponse({'success': False, 'message': 'Error al crear el cliente'}, status=500)

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


    def crearClienteEmpresa(self, codigosn, tiposn, grupoSN, tipoCliente):
        """
        Método para crear un cliente empresa.

        Args:
            codigosn (str): Código del socio de negocio.
            tiposn (TipoSNDB): Tipo de socio de negocio.
            grupoSN (GrupoSNDB): Grupo de socio de negocio.
            tipoCliente (TipoClienteDB): Tipo de cliente.

        Returns:
            JsonResponse: Mensaje de éxito o error según el resultado.
        """
        return SocioNegocioRepository.crearClienteEmpresa(
            codigoSN=codigosn, nombre=self.nombre, razonSocial=self.razon_social, rut=self.rut, giro=self.giro,
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
        print("Generando código de socio de negocio...")
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
            JsonResponse: Si la dirección y el contacto se agregaron exitosamente, retorna un mensaje de éxito.
                        Si hubo un error, retorna un mensaje de error y un código de estado 400.
        """
        print("Agregando dirección y contacto...")
        print(f"Cliente: {cliente}")
        print(f"Request: {request.POST}")
        from showromVentasApp.views.view import agregarDireccion, agregarContacto

        # Capturar datos de dirección y contacto desde el request
        direccion = request.POST.get('nombre_direccion[]')
        nombre_contacto = request.POST.get('nombre[]') or cliente.nombre
        apellido_contacto = request.POST.get('apellido[]') or cliente.apellido
        telefono_contacto = request.POST.get('telefono[]') or cliente.telefono
        email_contacto = request.POST.get('email[]') or cliente.email

        # Validar que al menos un contacto esté completo
        if not direccion:
            print("Dirección faltante")
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
        print(f"Datos de contacto generados: {contacto_data}")

        # Agregar dirección y contacto
        agregarDireccion(request, cliente)
        agregarContacto(request, cliente, **contacto_data)  # Asegúrate de que `agregarContacto` acepte estos datos.

        return JsonResponse({"mensaje": "Dirección y contacto agregados exitosamente."})




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
            'region': direccion.region.nombre,
            'comuna_codigo': direccion.comuna.codigo,
            'region_numero': direccion.region.numero,
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
        
    def validarNombre(self):
        """
        Método para validar el nombre del cliente.

        Raises:
            ValidationError: Si el nombre no se encuentra.
        """

        if not self.nombre:
            raise ValidationError("Nombre no encontrado")
        
    def validarApellido(self):
        """
        Método para validar el apellido del cliente.

        Raises:
            ValidationError: Si el apellido no se encuentra.
        """

        if not self.apellido:
            raise ValidationError("Apellido no encontrado")
    
    def validarTelefono(self):
        """
        Método para validar el teléfono del cliente.

        Raises:
            ValidationError: Si el teléfono no se encuentra.
        """

        if not self.telefono:
            raise ValidationError("Teléfono no encontrado")
    
    def tamañotelefono(self):
        """
        Método para validar el tamaño del teléfono del cliente.
        """

        if len(self.telefono) < 12:
            raise ValidationError("El teléfono debe tener al menos 12 dígitos")
    
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
        
    def verificarSocioDB(self, rut):
        """
        Metodo que verifica si un socio de negocio existe en la base de datos.

        Args:
            rut (str): rut del socio de negocio.

        Returns:
            bool: True si el socio de negocio existe, False si no.
        """
        try:
            repo = SocioNegocioRepository()
            socio = repo.obtenerPorCodigoSN(rut)
            if socio:
                return True
            
            else:
                return False
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error al verificar el socio de negocio'}, status=500)
            


        
    def verificarSocioNegocioSap(self, cardCode):
        """
        
        Método para verificar si un socio de negocio existe en SAP.
        
        Args:
            cardCode (str): Código del socio de negocio.
            
        Returns:
            bool: True si el socio de negocio existe, False si no.            
        """
        print("Verificando socio de negocio en SAP...")

        client = APIClient()

        try:
            
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
    
    def obtenerDatosCliente(self, cardCode):
        
        try:
            cliente = SocioNegocioDB.objects.get(rut=cardCode)
            direcciones = DireccionRepository().obtenerDireccionesPorCliente(cliente)
            contactos = ContactoRepository().obtenerContactosPorCliente(cliente)
            return cliente, direcciones, contactos
        except SocioNegocioDB.DoesNotExist:
            raise ValueError(f"No se encontró el cliente con RUT: {cardCode}")


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
            response = client.crearCliente(data)
            
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


                    return response
                
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
            #autoincementar row num por cada direccion agg
            rownum = 1
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
                            DireccionRepository.crearDireccion(socio,rownum, nombredire, ciudad[i], direccion[i], comuna[i], region[i], tipo[i], pais[i])
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
        print(f"Datos recibidos: {data}")
        print(f"Datos recibidos: {data.getlist('contactos')}")

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
            codigosInternoSap = 1
            

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
                            ContactoRepository.crearContacto(socio, codigosInternoSap, nombre, apellidos[i], telefonos[i], emails[i], celulares[i])
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
        

    def convertirJsonObjeto(self, json_data):
        """
        Metodo para convertir un JSON a un objeto Python.

        args:
            json_data (str): Cadena JSON a convertir.

        Returns:
            dict: Objeto Python convertido.
        """
        print("Convirtiendo JSON a objeto Python...")
        print(f"Datos JSON: {json_data}")

        # Verificar si `json_data` es una cadena JSON y convertirla si es necesario
        if isinstance(json_data, str):
            return json.loads(json_data)
        
        return json_data  # Si ya es un dict, lo retorna directamente


    def procesarDatosSocionegocio(self, data):
        """
        Procesa los datos de un socio de negocio para ser guardados en la base de datos.

        Args:
            data (dict): Datos del socio de negocio.

        Returns:
            dict: Datos del socio de negocio procesados.
        """

        print("Procesando datos del socio de negocio...")
        print(f"Datos recibidos para crear en MYSQL: {data}")

        name, lastname = data.get('CardName').split(' ', 1)
        razonsocial = data.get('CardName')

        # Datos principales del socio de negocio
        socio_negocio = {
            "codigoSN": data.get("CardCode", ""),
            "nombreCompleto": data.get("CardName", ""),
            "razonSocial": razonsocial or "Null",
            "nombre": name or "Null",  # Asumiendo que 'CardName' contiene nombre completo
            "apellido": lastname or "None",  # Si solo hay un campo de nombre, apellido se mantiene igual
            "email": data.get("EmailAddress", "") or "Null",
            "telefono": data.get("Phone1", "") or "Null",
            "celular": data.get("Phone1", "") or "Null",
            "giro": data.get("Notes", "") or "Null",
            "rut": data.get("FederalTaxID", "") or "Null",
            "grupoSN": data.get("GroupCode", "") or "Null",
            "tipoSN": "I",  # Valor fijo según lo especificado
            "tipoCliente": "N"  # Valor fijo según lo especificado
        }

        # Direcciones del socio de negocio
        direcciones = []
        for direccion in data.get("BPAddresses", []):
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
                "tipoDireccion": tipo_direccion,  # Nuevo campo
            })

        # Empleados de contacto del socio de negocio
        empleados_contacto = []
        for contacto in data.get("ContactEmployees", []):
            fullName = contacto.get("Name", "")
            nombre, apellido = (fullName.split(' ', 1) + [""])[:2]

            empleados_contacto.append({
                "codigoInternoSap": contacto.get("InternalCode", ""),
                "nombreCompleto": contacto.get("Name", ""),
                "nombre": nombre,  # Asumiendo que 'Name' contiene nombre completo
                "apellido": apellido or "None",  # Si no hay apellido, se mantiene vacío
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
        print(f"Nombre: " + socio_negocio["nombre"])
        print(f"Apellido: " + socio_negocio["apellido"])

        # Obtener la instancia de GrupoSNDB
        try:
            grupo = GrupoSNDB.objects.get(codigo=socio_negocio["grupoSN"]) # Cambiado de id a codigo
            tipo = TipoSNDB.objects.get(codigo=socio_negocio["tipoSN"])
            tipo_cliente = TipoClienteDB.objects.get(codigo=socio_negocio["tipoCliente"])

        except ObjectDoesNotExist:
            raise ValueError("No se encontró el grupo, tipo de socio de negocio o tipo de cliente")
            # Maneja el error según sea necesario, como lanzar una excepción o crear un nuevo grupo
        
        if socio_negocio["grupoSN"] == 105:
            print("Creando cliente persona...")
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
            print("Creando cliente empresa...")
            cliente = SocioNegocioRepository.crearClienteEmpresa(
                codigoSN=socio_negocio["codigoSN"],
                nombre=socio_negocio["nombre"],
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
            DireccionRepository.crearDireccion(
                socio=socio_negocio["codigoSN"],
                rownum=direccion["rowNum"],
                nombre_direccion=direccion["nombreDireccion"],
                ciudad=direccion["ciudad"],
                calle_numero=direccion["calleNumero"],
                comuna_id=666,
                region_id=13,  # Valor por defecto
                tipo_direccion=direccion["tipoDireccion"],
                pais=direccion.get("pais", "Chile")  # Valor por defecto
            )
            print (f"Data Direccion: {direccion}")

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
        print("Generando CardCode...")
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
        print("Creando y respondiendo cliente...")  
        try:
            client = APIClient()
            data = client.getInfoSN(carCode)
            
            print(f"Data: {data}")
            
            data_creacion = self.procesarDatosSocionegocio(self.convertirJsonObjeto(data))

            print (f"Data Creacion: {data_creacion}")

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

        if filter_data.get('codigo'):
            filters['contains(CardCode'] = f"'{filter_data['codigo']}')"
        if filter_data.get('nombre'):
            filters['contains(CardName'] = f"'{filter_data['nombre']}')"
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


    
    """
    filter=CardType eq 'cCustomer' and contains(CardCode, '10') 
    and contains(CardName, 'Leonardo') and GroupCode eq 105 and contains(Phone1, '+569') and contains(EmailAddress, '@gmail')
    """
    
    def plp(cls):
        """
        clear
        """

        ab = 1 + 2
        pass


#Creacion Socio Negocio

    def crearOActualizarCliente(self):

        dataSN = self.request
        print("creando o actualizando cliente...")

        if not self.verificarRutValido(self.rut):
            return JsonResponse({'success': False, 'message': 'RUT inválido'}, status=400)
        
        try:
            self.validarDatosObligatorios()

            rut = self.rut            
            codigoSN = SocioNegocio.generarCodigoSN(rut)
            clienteExistente = SocioNegocioRepository.obtenerPorRut(self.rut)

            print(f"Cliente existente: {clienteExistente}")

            print(f"Grupo datos actualizar: {dataSN}")
                        
            if clienteExistente is not None:
                return self.procesarClienteExistente(codigoSN, clienteExistente, datosNuevos=dataSN)
            
            self.procesarNuevoCliente(dataSN)
            
            return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})
        except ValidationError as e:
            return self.manejarErrorValidacion(e)
        except Exception as e:
            return self.manejarErrorGeneral(e)

    def procesarNuevoCliente(self, dataSN):
        try:
            print("Procesando nuevo cliente...")

            print (f"DataSN: {dataSN}")

            codigoSN = SocioNegocio.generarCodigoSN(self.rut)

            if not codigoSN:
                raise ValueError("No se pudo generar el código del cliente.")
            
            print(f"Código de cliente generado: {codigoSN}")

            jsonData = self.serializarSN(dataSN)
            
            data = self.creacionSocioSAP(jsonData)

            data_creacion = self.procesarDatosSocionegocio(self.convertirJsonObjeto(data))

            print (f"Data Creacion: {data_creacion}")

            cliente = self.guardarClienteCompleto(data_creacion)

            return cliente
        
        except Exception as e: 
            return JsonResponse({'success': False, 'message': 'Error al procesar el cliente'}, status=500)
        
    def crearNuevoCliente(self, codigosn, tiposn, grupoSN, tipoCliente):
        print("Creando nuevo cliente...")
        print(f"Grupo de cliente: {grupoSN}")
        
        with transaction.atomic():

            if self.gruposn == '105':
                print("creando cliente persona")
                cliente = self.crearClientePersona(codigosn, self.rut, tiposn, tipoCliente, self.email, grupoSN)
                
            elif self.gruposn == '100':
                print("creando cliente empresa")
                cliente = self.crearClienteEmpresa(codigosn, tiposn, grupoSN, tipoCliente)
            else:
                raise ValidationError(f"Grupo de cliente no válido: {self.gruposn}")
            SocioNegocio.agregarDireccionYContacto(self.request, cliente)
            print("Cliente creado exitosamente.")
            print(f"Cliente creado: {cliente}")

        return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})

    def serializarSN(self, data):
        # Decodifica el JSON de entrada
        print("Serializando datos del cliente...")

        rut = data.get("rutSN", "")
        cardcode = self.generarCodigoSN(rut)

        print(f"RUT: {rut}")
        print(f"Código de cliente: {cardcode}")
        
        client_data = data
        
        # Serializa los datos principales del cliente
        serialized_data = {
            "CardCode": cardcode,
            "CardName": f"{client_data.get('nombreSN', '')} {client_data.get('apellidoSN', '')}".strip(),
            "CardType": "cCustomer",
            "GroupCode": int(client_data.get("tipoSN", "")),
            "Phone1": client_data.get("telefonoSN", ""),
            "Phone2": client_data.get("telefonoSN", ""),
            "Notes": client_data.get("giroSN", ""),
            "PayTermsGrpCode": -1,
            "FederalTaxID": client_data.get("rutSN", ""),
            "SalesPersonCode": -1,
            "Cellular": client_data.get("telefonoSN", ""),
            "EmailAddress": client_data.get("emailSN", ""),
            "CardForeignName": f"{client_data.get('nombreSN', '')} {client_data.get('apellidoSN', '')}".strip(),
            #"ShipToDefault": "DESPACHO",
            #"BilltoDefault": "FACTURACION",
            "DunningTerm": "ESTANDAR",
            "CompanyPrivate": "cPrivate",
            "AliasName": client_data.get("nombreSN", ""),
            "U_Tipo": "N",
            "U_FE_Export": "N",
            "BPAddresses": [],
            "ContactEmployees": []
        }
        
        # Serializa las direcciones
        direcciones = client_data.get("direcciones", [])
        tipos_direccion = {"13": None, "12": None}

        for address in direcciones:
            tipo_direccion = address.get("tipoDireccion", "")
            serialized_address = {
                "AddressName": address.get("nombreDireccion", ""),
                "Street": address.get("direccion", ""),
                "City": address.get("ciudad", ""),
                "County": tipo_direccion,
                "Country": "CL",  # Abreviación del país (e.g., Chile -> CL)
                "State": int(address.get("region", "")),
                "FederalTaxID": client_data.get("rutSN", "").split("-")[0],
                "TaxCode": "IVA",
                "AddressType": "bo_ShipTo" if tipo_direccion == "13" else "bo_BillTo"
            }
            serialized_data["BPAddresses"].append(serialized_address)
            tipos_direccion[tipo_direccion] = serialized_address

        # Genera la dirección faltante si solo hay una de las dos
        if tipos_direccion["13"] and not tipos_direccion["12"]:
            direccion_facturacion = tipos_direccion["13"].copy()
            direccion_facturacion["County"] = "12"  # Cambia a tipo 12
            direccion_facturacion["AddressType"] = "bo_BillTo"
            serialized_data["BPAddresses"].append(direccion_facturacion)

        if tipos_direccion["12"] and not tipos_direccion["13"]:
            direccion_despacho = tipos_direccion["12"].copy()
            direccion_despacho["County"] = "13"  # Cambia a tipo 13
            direccion_despacho["AddressType"] = "bo_ShipTo"
            serialized_data["BPAddresses"].append(direccion_despacho)
        
        # Serializa los contactos
        contactos = client_data.get("contactos", [])
        
        if not contactos:  # Si no hay contactos, genera uno basado en el cliente principal
            print("No se proporcionaron contactos. Generando un contacto basado en los datos del cliente principal...")
            contacto_cliente_principal = {
                "Name": f"{client_data.get('nombreSN', '')} {client_data.get('apellidoSN', '')}".strip(),
                "Phone1": client_data.get("telefonoSN", ""),
                "MobilePhone": client_data.get("telefonoSN", ""),
                "E_Mail": client_data.get("emailSN", ""),
                "FirstName": client_data.get("nombreSN", ""),
                "LastName": client_data.get("apellidoSN", "")
            }
            serialized_data["ContactEmployees"].append(contacto_cliente_principal)
        else:
            for contact in contactos:
                serialized_contact = {
                    "Name": f"{contact.get('nombreContacto', '')} {contact.get('apellidoContacto', '')}".strip(),
                    "Phone1": contact.get("telefonoContacto", ""),
                    "MobilePhone": contact.get("telefonoContacto", ""),
                    "E_Mail": contact.get("emailContacto", ""),
                    "FirstName": contact.get("nombreContacto", ""),
                    "LastName": contact.get("apellidoContacto", "")
                }
                serialized_data["ContactEmployees"].append(serialized_contact)

        print(f"Datos serializados: {serialized_data}")
        return serialized_data
