from datosLsApp.repositories.socionegociorepository import SocioNegocioRepository
from datosLsApp.repositories.gruporepository import GrupoRepository
from django.db import transaction
from django.core.exceptions import ValidationError

class SocioNegocioService:

    @staticmethod
    def crear_o_actualizar_cliente(request):
        gruposn = request.POST.get('grupoSN')
        rut = request.POST['rutSN']
        giro = request.POST['giroSN']
        telefono = request.POST['telefonoSN']
        email = request.POST['emailSN']

        if not all([gruposn, rut, email]):
            raise ValidationError("Faltan datos obligatorios")

        # Eliminar guion del RUT
        rut_sn = rut.split("-")[0] if "-" in rut else rut

        # Crear código de socio de negocio
        codigosn = rut_sn.replace(".", "") + 'c'

        gruposn1 = GrupoRepository.obtener_grupo_por_codigo(gruposn)
        tipocliente = GrupoRepository.obtener_tipo_cliente_por_codigo('N')
        
        if not gruposn1 or not tipocliente:
            raise ValidationError("GrupoSN o TipoCliente no encontrados")
        
        cliente_existente = SocioNegocioRepository.obtener_por_rut(rut)
        if cliente_existente:
            raise ValidationError("Ya existe un cliente con el mismo RUT")

        tiposn = GrupoRepository.obtener_tipo_sn_por_codigo('C' if gruposn == '100' else 'I')

        with transaction.atomic():
            if gruposn == '100':
                nombre = request.POST['nombreSN']
                apellido = request.POST['apellidoSN']
                cliente = SocioNegocioRepository.crear_cliente(
                    codigoSN=codigosn,
                    nombre=nombre,
                    apellido=apellido,
                    rut=rut,
                    giro=giro,
                    telefono=telefono,
                    email=email,
                    grupoSN=gruposn1,
                    tipoSN=tiposn,
                    tipoCliente=tipocliente
                )
            elif gruposn == '105':
                razonsocial = request.POST['nombre']
                cliente = SocioNegocioRepository.crear_cliente(
                    codigoSN=codigosn,
                    razonSocial=razonsocial,
                    rut=rut,
                    giro=giro,
                    telefono=telefono,
                    email=email,
                    grupoSN=gruposn1,
                    tipoSN=tiposn,
                    tipoCliente=tipocliente
                )

            # Importar dinámicamente dentro del bloque que usa estas funciones
            if 'nombreDireccion' in request.POST:
                from showromVentasApp.views import agregarDireccion
                agregarDireccion(request, cliente)
            else:
                raise ValidationError("Debe agregar al menos una dirección")

            if 'nombreCompleto' in request.POST:
                from showromVentasApp.views import agregarContacto
                agregarContacto(request, cliente)
            else:
                raise ValidationError("Debe agregar al menos un contacto")
