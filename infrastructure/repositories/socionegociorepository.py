from django.db.models import Q, Prefetch

from infrastructure.models import SocioNegocioDB
from infrastructure.models.direcciondb import DireccionDB



class SocioNegocioRepository:

    """
    Repositorio de Socios de Negocio

    Metodos disponibles:

    - get_by_rut(rut)
    - crearCliente(**kwargs)
    - buscarClientesPorRut(rut)
    - buscarClientesPorNombre(nombre)
    - obtenerPorCodigoSN(codigoSN)

    """
    
    @staticmethod
    def get_by_rut(rut):
        """
        Obtiene un socio de negocio por su rut
        
        params:
            rut: str

            - Rut del socio de negocio a buscar
        
        return:
            SocioNegocioDB | None
        """
        try:
            return SocioNegocioDB.objects.get(rut=rut)
        except SocioNegocioDB.DoesNotExist:
            return None

    @staticmethod
    def crearCliente(**kwargs):
        """
        Crea un cliente en la base de datos
        
        params:
            kwargs: dict

            - Datos del cliente a crear
        
        return:
            SocioNegocioDB
        """
        return SocioNegocioDB.objects.create(**kwargs)
    
    @staticmethod
    def crearClienteEmpresa(**kwargs):
        """
        Crea un cliente empresa en la base de datos
        
        params:
            kwargs: dict

            - Datos del cliente empresa a crear
        
        return:
            SocioNegocioDB
        """
        return SocioNegocioDB.objects.create(**kwargs)

    @staticmethod
    def buscarClientesPorRut(rut):
        """
        Busca clientes por rut
        
        params:
            rut: str - Rut del cliente a buscar
        
        return:
            QuerySet - Clientes encontrados
            """
        return SocioNegocioDB.objects.filter(rut__icontains=rut)

    @staticmethod
    def buscarClientesPorNombre(nombre):
        return SocioNegocioDB.objects.filter(nombre__icontains=nombre)
    
    def obtenerPorCodigoSN(self, codigoSN):

        codigoSN = codigoSN.replace("C", "").replace("c", "").replace("-", "").replace(".", "").replace(" ", "").strip()

        card_code = f"{codigoSN}C"
        card_code_min = card_code.lower()

        # Intentar buscar el código exacto primero
        socio = SocioNegocioDB.objects.filter(codigoSN=card_code).first()

        if socio:
            print("Socio encontrado con código exacto:", socio)
            return socio

        # Si no existe, intentar con minúsculas
        socio_min = SocioNegocioDB.objects.filter(codigoSN=card_code_min).first()

        if socio_min:
            print("Socio encontrado con código en minúsculas:", socio_min)
            return socio_min

        print("No se encontró socio de negocio con código:", codigoSN)
        return None
    
    def obtenerPorCodigoSN2(self, codigoSN):
        """
        Obtiene un socio de negocio por su código
        
        params:
            codigoSN: str

            - Código del socio de negocio a buscar
        
        return:
            SocioNegocioDB | None
        """
        
        try:
            return SocioNegocioDB.objects.get(codigoSN=codigoSN)
        except SocioNegocioDB.DoesNotExist:
            return None
    
    def data_bp_for_pdf(codigoSN, sucursal):

        from infrastructure.models.contactodb import ContactoDB
        from infrastructure.models.direcciondb import DireccionDB
        from infrastructure.models.sucursaldb import SucursalDB

        data_bp = SocioNegocioDB.objects.get(codigoSN=codigoSN)
        address = DireccionDB.objects.filter(SocioNegocio=data_bp.codigoSN, tipoDireccion="13").first()
        contact = ContactoDB.objects.filter(SocioNegocio=data_bp.codigoSN).first()
        branch_detail = SucursalDB.objects.filter(codigo=sucursal).first()

        def clean(value):
            return '' if value in (None, 'null') else value

        data = {
            "name": f"{data_bp.nombre} {data_bp.apellido}" if data_bp.tipoSN == "105" else data_bp.razonSocial,
            "email": clean(data_bp.email),
            "phone": clean(data_bp.telefono),
            "address": clean(address.comuna.nombre) if address else '',
            "contact": clean(contact.nombre) if contact else '',
            "contact_phone": clean(contact.telefono) if contact else '',
            "branch_detail": clean(branch_detail.codigo) if branch_detail else '',
        }

        return data

    @staticmethod
    def actualizarCliente(codigoSN, datosActualizados):
        try:
            cliente = SocioNegocioDB.objects.get(codigoSN=codigoSN)
            
            # Actualizar atributos comunes
            cliente.nombre = datosActualizados.get('nombreSN', cliente.nombre)
            cliente.apellido = datosActualizados.get('apellidoSN', cliente.apellido)
            cliente.razonSocial = ""
            cliente.rut = datosActualizados.get('rutSN', cliente.rut)
            cliente.telefono = datosActualizados.get('telefonoSN', cliente.telefono)
            cliente.giro = datosActualizados.get('giroSN', cliente.giro)
            cliente.email = datosActualizados.get('emailSN', cliente.email)
            cliente.grupoSN = datosActualizados.get('grupoSN', cliente.grupoSN)


            cliente.save()

            return {'success': True, 'message': 'Cliente persona actualizado correctamente', 'cliente': cliente}
        
        except SocioNegocioDB.DoesNotExist:
            return {'success': False, 'message': f'Cliente con código {codigoSN} no encontrado'}
        except Exception as e:
            return {'success': False, 'message': f'Error al actualizar cliente: {str(e)}'}

    @staticmethod
    def actualizarClienteEmpresa(codigoSN, datosActualizados):

        try:
            cliente = SocioNegocioDB.objects.get(codigoSN=codigoSN)
            
            # Actualizar atributos específicos de empresa
            cliente.nombre = datosActualizados.get('nombreSN', cliente.razonSocial)
            cliente.razonSocial = datosActualizados.get('nombreSN', cliente.razonSocial)
            cliente.rut = datosActualizados.get('rutSN', cliente.rut)
            cliente.telefono = datosActualizados.get('telefonoSN', cliente.telefono)
            cliente.giro = datosActualizados.get('giroSN', cliente.giro)
            cliente.email = datosActualizados.get('emailSN', cliente.email)
            cliente.grupoSN = datosActualizados.get('grupoSN', cliente.grupoSN)

            cliente.save()

            return {'success': True, 'message': 'Cliente empresa actualizado correctamente', 'cliente': cliente}
        
        except SocioNegocioDB.DoesNotExist:
            return {'success': False, 'message': f'Cliente con código {codigoSN} no encontrado'}
        except Exception as e:
            return {'success': False, 'message': f'Error al actualizar cliente: {str(e)}'}


    #obtener rut de cliente por codigoSN
    
    def obtenerRutCliente(self, codigoSN):
        """
        Obtiene el rut de un cliente por su código
        
        params:
            codigoSN: str

            - Código del cliente a buscar
        
        return:
            str | None
        """
        try:
            cliente = SocioNegocioDB.objects.get(codigoSN=codigoSN)
            return cliente.rut
        except SocioNegocioDB.DoesNotExist:
            return None
        
    
    @staticmethod
    def buscar_clientes(termino):

        termino = termino.strip()

        return (
            SocioNegocioDB.objects
            .filter(
                Q(nombre__icontains=termino) |
                Q(rut__icontains=termino) |
                Q(razonSocial__icontains=termino)
            )
            .prefetch_related(
                Prefetch(
                    "direcciondb_set",
                    queryset=DireccionDB.objects.select_related("comuna", "region")
                ),
                "contactodb_set"
            )
            .only(
                "codigoSN",
                "nombre",
                "apellido",
                "razonSocial",
                "rut",
                "email",
                "telefono",
                "giro",
                "condicionPago",
                "plazoReclamaciones",
                "clienteExportacion",
                "vendedor"
            )
            .order_by("nombre")[:20]
        )
