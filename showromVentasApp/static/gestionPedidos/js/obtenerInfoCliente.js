$(document).ready(function(){
    // Delegamos el evento click al contenedor, para que funcione con elementos creados dinámicamente
    $('#resultadosClientes').on('click', '.suggestion-item', function(){
        
        let nombre = $(this).attr('data-nombre');
        let apellido = $(this).attr('data-apellido');
        let clienteId = $(this).attr('data-rut');
        console.log('Cliente seleccionado:', nombre, apellido, clienteId);

        // Rellenar el campo de entrada con el nombre y apellido del cliente seleccionado
        $('#inputCliente').val(nombre + ' ' + apellido);

        // Limpiar la lista de sugerencias
        $('#resultadosClientes').empty();

        // Llamar a la función para traer información adicional del cliente
        traerInformacionCliente(clienteId);
    });
});

// Función para traer información completa del cliente (modularizada)
function traerInformacionCliente(clienteId) {
    $.ajax({
        url: 'buscarc/', // Cambia a la URL correcta de tu backend
        data: {
            'rut': clienteId
        },
        dataType: 'json',
        success: function(data) {
            console.log('Información completa del cliente:', data); // Console log para ver el JSON completo

            // Llamar a la función para actualizar los contactos en el select
            actualizarContactos(data.contactos);
            actualizarDirecciones(data.despachos, '#direcciones_despacho');
            actualizarDirecciones(data.facturaciones, '#direcciones_facturacion');
        },
        error: function(xhr, status, error) {
            console.error('Error al obtener la información del cliente:', error);
        }
    });
}


// Función para actualizar los contactos en el select
function actualizarContactos(contactos) {
    let selectContactos = $('#clientes'); // ID del optgroup en el select

    // Limpiar el select antes de agregar nuevos contactos
    selectContactos.empty();

    if (contactos && contactos.length > 0) {
        contactos.forEach(function(contacto) {
            let option = $('<option></option>');
            option.val(contacto.id);
            option.text(contacto.nombre + ' ' + contacto.apellido);
            selectContactos.append(option);
        });
    } else {
        // Si no hay contactos, puedes agregar una opción indicando esto
        let option = $('<option></option>');
        option.text('No hay contactos disponibles');
        selectContactos.append(option);
    }
}

// Función para actualizar los select de direcciones
function actualizarDirecciones(direcciones, selectId) {
    let select = $(selectId); // El select correspondiente

    // Limpiar el select antes de agregar nuevas opciones
    select.empty();

    if (direcciones && direcciones.length > 0) {
        direcciones.forEach(function(direccion) {
            let option = $('<option></option>');
            option.val(direccion.id);
            option.text(direccion.nombreDireccion);
            select.append(option);
        });
    } else {
        // Si no hay direcciones, agregar una opción indicando esto
        let option = $('<option></option>');
        option.text('No hay direcciones disponibles');
        select.append(option);
    }
}