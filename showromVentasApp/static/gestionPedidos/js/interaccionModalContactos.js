$(document).ready(function() {
    $('#btn-grabar-cont').on('click', function(e) {
        e.preventDefault(); // Evitar comportamiento por defecto del botón

        // Capturar todos los contactos en un array
        let contactos = [];

        // Recorrer cada div que contiene los contactos
        $('#listaContactos .col-sm-5').each(function() {
            // Obtener los valores de los inputs
            let nombre = $(this).find('input[name="nombre[]"]').val();
            let apellido = $(this).find('input[name="apellido[]"]').val();
            let telefono = $(this).find('input[name="telefono[]"]').val();
            let celular = $(this).find('input[name="celular[]"]').val();
            let email = $(this).find('input[name="email[]"]').val();
            let contactoid = $(this).find('input[name="contacto_id[]"]').val();
        
            
            if (nombre && apellido && telefono && celular && email) {
                contactos.push({
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono,
                    'celular': celular,
                    'email': email,
                    "contacto_id": contactoid,
                });
            } else {
                console.log('Contacto ignorado porque no tiene todos los campos completos.');
            }
        });
        

        // Mostrar en consola el array completo de contactos
        console.log('Contactos capturados:', contactos);

        // Validar que al menos un contacto tenga datos completos
        if (contactos.length === 0) {
            alert('Debes agregar al menos un contacto.');
            return;
        }

        // Mostrar el cliente que se enviará en la petición
        let clienteRut = $('#inputCliente').data('rut');
        console.log('Cliente RUT capturado:', clienteRut);

        // Enviar los contactos al backend mediante AJAX
        $.ajax({
            url: '/guardar_contactos/',  // URL del endpoint en Django
            type: 'POST',
            data: {
                'contactos': JSON.stringify(contactos),
                'cliente': clienteRut  // Asumiendo que el cliente está en un atributo `data-rut`
            },
            headers: { 
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()  // Incluir el token CSRF en los headers
            },
            success: function(response) {
                console.log('Respuesta del servidor:', response);
                if (response.success) {
                    alert('Contactos guardados correctamente');
                    $('#contactoModal').modal('hide');
                    location.reload();
                } else {
                    alert('Error al guardar contactos: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error al guardar contactos:', error);
                alert('Ha ocurrido un error al guardar los contactos.');
            }
        });
    });
});
