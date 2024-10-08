import json
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

    def __init__(self, request):

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
        """
        print("Validando datos obligatorios...")
        self.validarGrupoSN()
        self.validarRut()
        self.validarEmail()

    def crearOActualizarCliente(self):

        try:
            self.validarDatosObligatorios()


            # Eliminar guion del RUT y crear código SN
            codigosn = SocioNegocio.generarCodigoSN(self.rut)
            print(f"Código SN generado: {codigosn}")

            # Obtener grupo
            grupoSN = GrupoSNRepository.obtenerGrupoSNPorCodigo(self.gruposn)

            if not grupoSN:
                raise ValidationError(f"Grupo de socio de negocio no encontrado para el código: {self.gruposn}")
            print(f"Grupo de socio de negocio: {grupoSN}")

            # Obtener tipo de cliente
            tipoCliente = TipoClienteRepository.obtenerTipoClientePorCodigo('N')
            if not tipoCliente:
                raise ValidationError("Tipo de cliente no encontrado")
            print(f"Tipo de cliente: {tipoCliente}")

            # Verificar si el cliente ya existe
            cliente_existente = SocioNegocioRepository.obtenerPorRut(self.rut)
            if cliente_existente:
                raise ValidationError("Ya existe un cliente con el mismo RUT")

            # Determinar tipo de socio de negocio
            tiposn = TipoSNRepository.obtenerTipoSnPorCodigo('C' if self.gruposn == '100' else 'I')
            if not tiposn:
                raise ValidationError(f"Tipo de socio de negocio no encontrado para el código: {'C' if self.gruposn == '100' else 'I'}")
            print(f"Tipo de socio de negocio: {tiposn}")

            # Crear o actualizar cliente dentro de una transacción
            print("Creando cliente...")
            with transaction.atomic():
                if self.gruposn == '100':
                    cliente = self.crearClientePersona(self, codigosn, self.rut, tiposn, tipoCliente, self.email, grupoSN)
                elif self.gruposn == '105':
                    cliente = self.crearClienteEmpresa(self, codigosn, tiposn, grupoSN, tipoCliente)
                else:
                    raise ValidationError(f"Grupo de cliente no válido: {self.gruposn}")

                SocioNegocio.agregarDireccionYContacto(self.request, cliente)

            return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})

        except ValidationError as e:
            print(f"ValidationError: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Error al crear el cliente'}, status=500)

    @staticmethod
    def crearClientePersona(self, codigosn, rut, tiposn, tipocliente, email, grupoSN):
        print(f"Creando cliente persona - Nombre: {self.nombre}, Apellido: {self.apellido}, RUT: {self.rut}, Email: {self.email}")

        return SocioNegocioRepository.crearCliente(
            codigoSN=codigosn, nombre=self.nombre, apellido=self.apellido, rut=rut, giro=self.giro,
            telefono=self.telefono, email=email, grupoSN=grupoSN, tipoSN=tiposn,
            tipoCliente=tipocliente
        )

    @staticmethod
    def crearClienteEmpresa(self, codigosn, tiposn, grupoSN, tipoCliente):
        print(f"Creando cliente empresa - Razón Social: {self.razon_social}, RUT: {self.rut}, Email: {self.email}")
        return SocioNegocioRepository.crearCliente(
            codigoSN=codigosn, razonSocial=self.razon_social, rut=self.rut, giro=self.giro,
            telefono=self.telefono, email=self.email, grupoSN=grupoSN, tipoSN=tiposn,
            tipoCliente=tipoCliente
        )


    @staticmethod
    def validardatosObligatorios(self):
        gruposn = self.request.POST.get('grupoSN')
        rut = self.request.POST.get('rutSN')
        email = self.request.POST.get('emailSN')

        if not all([gruposn, rut, email]):
            print("Datos obligatorios faltantes")
            raise ValidationError("Faltan datos obligatorios")
        return gruposn, rut, email

    @staticmethod
    def generarCodigoSN(rut):
        rut_sn = rut.split("-")[0] if "-" in rut else rut
        return rut_sn.replace(".", "") + 'C'

    @staticmethod
    def agregarDireccionYContacto(request, cliente):
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

    
    @staticmethod
    def buscarSocioNegocio(numero):
        resultados_clientes = SocioNegocioRepository.buscarClientesPorRut(numero)
        resultados_formateados = []

        for socio in resultados_clientes:
            direcciones = DireccionDB.objects.filter(SocioNegocio=socio)
            direcciones_formateadas = [{
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

            contactos = ContactoDB.objects.filter(SocioNegocio=socio)
            contactos_formateados = [{
                'codigoInternoSap': contacto.codigoInternoSap,
                'nombreCompleto': contacto.nombreCompleto,
                'nombre': contacto.nombre,
                'apellido': contacto.apellido,
                'email': contacto.email,
                'telefono': contacto.telefono,
                'celular': contacto.celular
            } for contacto in contactos]

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

    
    def validarGrupoSN(self):
        if not self.gruposn:
            raise ValidationError("Grupo de socio de negocio no encontrado")
    
    def validarRut(self):
        if not self.rut:
            raise ValidationError("RUT no encontrado")
        
    def validarEmail(self):
        if not self.email:
            raise ValidationError("Email no encontrado")
        
        
    def verificarSocioNegocioSap(self, cardCode):
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
        cardCode = jsonData.get('rut')
        print(f"CardCode: {cardCode}")

        nombre = jsonData.get('nombre')
        apellido = jsonData.get('apellido')

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
            'Phone1': jsonData.get('telefono'),
            'Phone2': jsonData.get('telefono'),
            'Notes': "Persona",
            'PayTermsGrpCode': -1,
            'FederalTaxID': jsonData.get('rut'),
            'SalesPersonCode': -1,  # Cambiar por el código de vendedor
            'Cellular': jsonData.get('telefono'),
            'EmailAddress': jsonData.get('email'),
            'CardForeignName': nombreCompleto,
            'ShipToDefault': "DESPACHO",
            'BilltoDefault': "FACTURACION",
            'DunningTerm': "ESTANDAR",
            'CompanyPrivate': "cPrivate",
            'AliasName': jsonData.get('nombre'),
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
        client = APIClient()
        
        try:
            print("Creando socio de negocio en SAP...")

            # Preparar JSON
            json_data = self.prepararJsonCliente(data)
            print(f"JSON preparado para enviar: {json_data}")

            # Enviar solicitud a SAP
            response = client.crearCliente(json_data)
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

