from django.shortcuts import get_object_or_404
from infrastructure.models import ContactoDB
from infrastructure.models.socionegociodb import SocioNegocioDB

class ContactoRepository:
    def obtenerContactosPorCliente(self, cliente):
        return ContactoDB.objects.filter(SocioNegocio=cliente)

    def obtenerContacto(contacto_id):
        return ContactoDB.objects.filter(id=contacto_id).first()
    
    def actualizarContacto(contacto_obj, nombre_contacto, apellido_contacto, telefono_contacto, celular_contacto,  email_contacto):
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
        try:

            socio_obj = get_object_or_404(SocioNegocioDB, codigoSN=socio)

            nuevo_contacto = ContactoDB.objects.create(
                SocioNegocio=socio_obj,
                codigoInternoSap = codigo_interno_sap,
                nombreCompleto = nombre_contacto,
                nombre=nombre_contacto,
                apellido=apellido_contacto,
                telefono=telefono_contacto,
                email=email_contacto,
                celular=celular_contacto
            )

        except Exception as e:
            print("Error en crearContacto", e)

        
    #eliminar todos los contactos de un socio

    def eliminarContactosPorSocio(socio):
        try:
            ContactoDB.objects.filter(SocioNegocio__codigoSN=socio).delete()
        except Exception as e:
            print(f"Error al eliminar contactos: {e}")
            raise
