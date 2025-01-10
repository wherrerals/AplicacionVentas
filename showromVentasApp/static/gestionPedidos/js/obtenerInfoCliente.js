
// Función para obtener información de los clientes
$(document).ready(function(){

    // Delegar el evento click al contenedor para elementos creados dinámicamente
    $('#resultadosClientes').on('click', '.suggestion-item', function(){
        
        let nombre = $(this).attr('data-nombre');
        let apellido = $(this).attr('data-apellido');
        let clienteId = $(this).attr('data-rut');
        let codigoSN = $(this).attr('data-codigoSN');

        // Actualizar valores en el DOM (nombre y apellido del cliente seleccionado)
        $('#inputCliente').val(codigoSN + " - " + nombre + ' ' + apellido);

        // Asignar el rut como atributo data-rut del input
        $('#inputCliente').attr('data-rut', clienteId);

        // Asignar el codigoSN como atributo data-codigoSN del input
        $('#inputCliente').attr('data-codigoSN', codigoSN);

        // Asignar el rut como atributo data-rut del input
        console.log("rut del cliente seleccionado: ",clienteId)
        
        // Limpiar la lista de sugerencias
        $('#resultadosClientes').empty();
 
        // Llamar a la función para traer la información completa del cliente
        traerInformacionCliente(clienteId);
    });
});


// Función para traer la información completa del cliente
function traerInformacionCliente(clienteId) {

    // si el numero tiene un - se elimina y lo que este al lado derecho se elimina
    if(clienteId.includes("-")){
        clienteId = clienteId.split("-")[0];
    }

    // URL para buscar clientes

    let buscarClientesUrl = `/ventas/buscar_clientes/?numero=${clienteId}`;

    $.ajax({

        url: buscarClientesUrl, // URL de la solicitud
        type: 'GET', // Método de la solicitud
        dataType: 'json',
        
        success: function(data) {
            if (data.resultadosClientes && data.resultadosClientes.length > 0) {

                // Obtener el primer cliente de la lista de resultados
                const cliente = data.resultadosClientes[0];
                const nombre = cliente.nombre;
                const apellido = cliente.apellido;
                const codigoSN = cliente.codigoSN;

                // Asignar el rut como atributo data-rut del input
                $('#inputCliente').attr('data-rut', clienteId);

                // Asignar el codigoSN como atributo data-codigoSN del input
                $('#inputCliente').attr('data-codigoSN', codigoSN);        

                // Rellenar el campo de entrada con el nombre y apellido del cliente seleccionado
                $('#inputCliente').val(codigoSN + " - " + nombre + ' ' + apellido);
                
                // Actualizar los contactos y direcciones del cliente seleccionado
                actualizarContactos(cliente.contactos);
                actualizarDirecciones(cliente.direcciones, '#direcciones_despacho', "12");
                actualizarDirecciones(cliente.direcciones, '#direcciones_facturacion', "13");

                // Llamar a la función para cargar la información del cliente en el modal
                cargarInformacionClienteEnModal(cliente);

            } else { 
                console.log('No se encontraron clientes con el número proporcionado.');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error al obtener la información del cliente:', error);
        }
    });
}

// Función para cargar la información del cliente en el modal
function actualizarContactos(contactos) {
    let selectContactos = $('#clientes'); // ID del optgroup en el select

    // Limpiar el select antes de agregar nuevos contactos
    selectContactos.empty();

    // Verificar si hay contactos disponibles
    if (contactos && contactos.length > 0) {
        contactos.forEach(function(contacto) {
            let option = $('<option></option>');
            option.val(contacto.id);
            option.text(contacto.nombre + ' ' + contacto.apellido);
            selectContactos.append(option);
        });
    } else {

        // Si no hay contactos disponibles, agregar una opción indicando esto
        let option = $('<option></option>');
        option.text('No hay contactos disponibles');
        selectContactos.append(option);
    }
}

// Función para actualizar las direcciones de despacho y facturación
function actualizarDirecciones(direcciones, selectId, tipoDireccion) {
    let select = $(selectId); 
    select.empty();

    // Filtrar las direcciones según el tipoDireccion
    const direccionesFiltradas = direcciones.filter(function(direccion) {

        return direccion.tipoDireccion === tipoDireccion;
    });

    // Verificar si hay direcciones disponibles para el tipo seleccionado
    if (direccionesFiltradas.length > 0) {
        direccionesFiltradas.forEach(function(direccion) {
            let option = $('<option></option>');
            option.val(direccion.id); //Ver este valor que se quiere usar como id unico
            option.text(direccion.nombreDireccion + ' - ' + direccion.ciudad + ', ' + direccion.comuna);
            select.append(option); 
        });
    } else {

        let option = $('<option></option>');
        option.text('No hay direcciones disponibles');
        select.append(option);
    }
}