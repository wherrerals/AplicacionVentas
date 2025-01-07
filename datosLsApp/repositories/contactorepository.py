from django.shortcuts import get_object_or_404
from datosLsApp.models import ContactoDB
from datosLsApp.models.socionegociodb import SocioNegocioDB

class ContactoRepository:
    """
    Repositorio de Contactos

    Metodos disponibles:

    - obtenerContactosPorCliente(cliente)
    - obtenerContacto(contacto_id)
    - actualizarContacto(contacto_obj, nombre_contacto, apellido_contacto, telefono_contacto, celular_contacto,  email_contacto)
    - crearContacto(socio, nombre_contacto, apellido_contacto, telefono_contacto, email_contacto, celular_contacto)
    """

    def obtenerContactosPorCliente(self, cliente):
        """
        Obtiene las direcciones de un cliente

        params:
            cliente: SocioNegocioDB

            - Cliente al que pertenecen las direcciones

        return:
            QuerySet
        """
        return ContactoDB.objects.filter(SocioNegocio=cliente)

    def obtenerContacto(contacto_id):
        """
        Obtiene un Contacto por su id

        params:
            contacto_id: int

            - Id del contacto

        return:
            ContactoDB

            - Contacto encontrado
        """
        return ContactoDB.objects.filter(id=contacto_id).first()
    
    def actualizarContacto(contacto_obj, nombre_contacto, apellido_contacto, telefono_contacto, celular_contacto,  email_contacto):
        """
        Actualiza los datos de un contacto

        params:
            contacto_obj: ContactoDB - Contacto a actualizar
            nombre_contacto: str - Nombre del contacto
            apellido_contacto: str - Apellido del contacto
            telefono_contacto: str - Telefono del contacto
            celular_contacto: str - Celular del contacto
            email_contacto: str - Email del contacto

        """
        try:
            contacto_obj.nombreCompleto = nombre_contacto + " " + apellido_contacto
            contacto_obj.nombre = nombre_contacto
            contacto_obj.apellido = apellido_contacto
            contacto_obj.telefono = telefono_contacto
            contacto_obj.celular = celular_contacto
            contacto_obj.email = email_contacto
            contacto_obj.save()

        except Exception as e:
            print("Error en actualizarContacto", e)


    def crearContacto(socio, codigo_interno_sap, nombre_contacto, apellido_contacto, telefono_contacto, email_contacto, celular_contacto):
        """
        Crea un nuevo contacto

        params:
            socio: int - Id del socio al que pertenece el contacto
            nombre_contacto: str - Nombre del contacto
            apellido_contacto: str - Apellido del contacto
            telefono_contacto: str - Telefono del contacto
            celular_contacto: str - Celular del contacto
            email_contacto: str - Email del contacto

        """
        print("creando contacto")
        print(f"toda la data: {socio}, {codigo_interno_sap}, {nombre_contacto}, {apellido_contacto}, {telefono_contacto}, {email_contacto}, {celular_contacto}")
        try:

            socio_obj = get_object_or_404(SocioNegocioDB, codigoSN=socio)

            nuevo_contacto = ContactoDB.objects.create(
                SocioNegocio=socio_obj,
                codigoInternoSap = codigo_interno_sap,
                nombreCompleto = nombre_contacto + " " + apellido_contacto,
                nombre=nombre_contacto,
                apellido=apellido_contacto,
                telefono=telefono_contacto,
                email=email_contacto,
                celular=celular_contacto
            )
            print("nuevo_contacto", nuevo_contacto)
        except Exception as e:
            print("Error en crearContacto", e)

        
    #eliminar todos los contactos de un socio

    def eliminarContactosPorSocio(socio):
        try:
            print(f"Intentando eliminar contactos para el socio: {socio}")
            ContactoDB.objects.filter(SocioNegocio__codigoSN=socio).delete()
            print("Contactos eliminados con éxito.")
        except Exception as e:
            print(f"Error al eliminar contactos: {e}")
            raise
