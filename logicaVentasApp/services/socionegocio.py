from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError
from datosLsApp.repositories.socionegociorepository import SocioNegocioRepository
from datosLsApp.repositories.gruposnrepository import GrupoSNRepository
from datosLsApp.repositories.tipoclienterepository import TipoClienteRepository
from datosLsApp.repositories.tiposnrepository import TipoSNRepository
from datosLsApp.models import DireccionDB, ContactoDB

class SocioNegocio:

    @staticmethod
    def crearOActualizarCliente(request):
        try:
            # Validar datos obligatorios
            gruposn, rut, email = SocioNegocio.validardatosObligatorios(request)
            print(f"Datos obligatorios - GrupoSN: {gruposn}, RUT: {rut}, Email: {email}")

            # Eliminar guion del RUT y crear código SN
            codigosn = SocioNegocio.generarCodigoSN(rut)
            print(f"Código SN generado: {codigosn}")

            # Obtener grupo
            grupoSN = GrupoSNRepository.obtenerGrupoSNPorCodigo(gruposn)
            if not grupoSN:
                raise ValidationError(f"Grupo de socio de negocio no encontrado para el código: {gruposn}")
            print(f"Grupo de socio de negocio: {grupoSN}")

            # Obtener tipo de cliente
            tipoCliente = TipoClienteRepository.obtenerTipoClientePorCodigo('N')
            if not tipoCliente:
                raise ValidationError("Tipo de cliente no encontrado")
            print(f"Tipo de cliente: {tipoCliente}")

            # Verificar si el cliente ya existe
            cliente_existente = SocioNegocioRepository.obtenerPorRut(rut)
            if cliente_existente:
                raise ValidationError("Ya existe un cliente con el mismo RUT")

            # Determinar tipo de socio de negocio
            tiposn = TipoSNRepository.obtenerTipoSnPorCodigo('C' if gruposn == '100' else 'I')
            if not tiposn:
                raise ValidationError(f"Tipo de socio de negocio no encontrado para el código: {'C' if gruposn == '100' else 'I'}")
            print(f"Tipo de socio de negocio: {tiposn}")

            # Crear o actualizar cliente dentro de una transacción
            print("Creando cliente...")
            with transaction.atomic():
                if gruposn == '100':
                    cliente = SocioNegocio.crearClientePersona(request, codigosn, rut, tiposn, tipoCliente, email, grupoSN)
                elif gruposn == '105':
                    cliente = SocioNegocio.crearClienteEmpresa(request, codigosn, rut, tiposn, grupoSN, tipoCliente, email)
                else:
                    raise ValidationError(f"Grupo de cliente no válido: {gruposn}")

                print(f"Cliente creado/actualizado: {cliente}")
                SocioNegocio.agregarDireccionYContacto(request, cliente)

            return JsonResponse({'success': True, 'message': 'Cliente creado exitosamente'})

        except ValidationError as e:
            print(f"ValidationError: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Error al crear el cliente'}, status=500)

    @staticmethod
    def crearClientePersona(request, codigosn, rut, tiposn, tipocliente, email, grupoSN):
        nombre = request.POST.get('nombreSN')
        apellido = request.POST.get('apellidoSN')
        giro = request.POST.get('giroSN')
        telefono = request.POST.get('telefonoSN')

        print(f"Creando cliente persona - Nombre: {nombre}, Apellido: {apellido}, RUT: {rut}, Email: {email}")
        return SocioNegocioRepository.crearCliente(
            codigoSN=codigosn, nombre=nombre, apellido=apellido, rut=rut, giro=giro,
            telefono=telefono, email=email, grupoSN=grupoSN, tipoSN=tiposn,
            tipoCliente=tipocliente
        )

    @staticmethod
    def crearClienteEmpresa(request, codigosn, rut, tiposn, grupoSN, tipocliente, email):
        razon_social = request.POST.get('nombre')
        giro = request.POST.get('giroSN')
        telefono = request.POST.get('telefonoSN')

        print(f"Creando cliente empresa - Razón Social: {razon_social}, RUT: {rut}, Email: {email}")
        return SocioNegocioRepository.crearCliente(
            codigoSN=codigosn, razonSocial=razon_social, rut=rut, giro=giro,
            telefono=telefono, email=email, grupoSN=grupoSN, tipoSN=tiposn,
            tipoCliente=tipocliente
        )


    @staticmethod
    def validardatosObligatorios(request):
        gruposn = request.POST.get('grupoSN')
        rut = request.POST.get('rutSN')
        email = request.POST.get('emailSN')

        if not all([gruposn, rut, email]):
            print("Datos obligatorios faltantes")
            raise ValidationError("Faltan datos obligatorios")
        return gruposn, rut, email

    @staticmethod
    def generarCodigoSN(rut):
        rut_sn = rut.split("-")[0] if "-" in rut else rut
        return rut_sn.replace(".", "") + 'c'

    @staticmethod
    def agregarDireccionYContacto(request, cliente):
        from showromVentasApp.views.view import agregarDireccion, agregarContacto

        if 'nombreDireccion' not in request.POST:
            print("Dirección faltante")
            raise ValidationError("Debe agregar al menos una dirección")
        agregarDireccion(request, cliente)

        if 'nombres' not in request.POST:
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
