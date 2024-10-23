from django.shortcuts import get_object_or_404
from datosLsApp.models import ContactoDB
from datosLsApp.models.socionegociodb import SocioNegocioDB

class ContactoRepository:

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

    def prueba(self):
        pass

    def obtenerContacto(contacto_id):
        return ContactoDB.objects.filter(id=contacto_id).first()
    
    def actualizarContacto(contacto_obj, nombre_contacto, apellido_contacto, telefono_contacto, celular_contacto,  email_contacto):
        print("contacto_obj", contacto_obj)
        print("prueba")
        print("nombre_contacto", nombre_contacto)
        print("apellido_contacto", apellido_contacto)
        print("telefono_contacto", telefono_contacto)
        print("email_contacto", email_contacto)
        print("cargo_contacto", celular_contacto)
        
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


    def crearContacto(socio, nombre_contacto, apellido_contacto, telefono_contacto, email_contacto, celular_contacto):
        print("crearContacto")
        print("socio", socio)
        print("nombre_contacto", nombre_contacto)
        print("apellido_contacto", apellido_contacto)
        print("telefono_contacto", telefono_contacto)
        print("email_contacto", email_contacto)
        
        try:

            socio_obj = get_object_or_404(SocioNegocioDB, codigoSN=socio)

            nuevo_contacto = ContactoDB.objects.create(
                SocioNegocio=socio_obj,
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
    