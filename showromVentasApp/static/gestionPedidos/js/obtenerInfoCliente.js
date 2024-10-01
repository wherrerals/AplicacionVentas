$(document).ready(function(){
    // Delegamos el evento click al contenedor, para que funcione con elementos creados dinámicamente
    $('#resultadosClientes').on('click', '.suggestion-item', function(){
        
        let nombre = $(this).attr('data-nombre');
        let apellido = $(this).attr('data-apellido');
        let clienteId = $(this).attr('data-rut');
        let codigoSN = $(this).attr('data-codigoSN');

        // Rellenar el campo de entrada con el nombre y apellido del cliente seleccionado
        $('#inputCliente').val(codigoSN + " - " + nombre + ' ' + apellido);

        // Asignar el rut como atributo data-rut del input
        $('#inputCliente').attr('data-rut', clienteId);

        // Asignar el rut como atributo data-rut del input
        console.log("rut del cliente seleccionado: ",clienteId)
        
        // Limpiar la lista de sugerencias
        $('#resultadosClientes').empty();
 
        traerInformacionCliente(clienteId);
    });
});

// Función para traer información completa del cliente (modularizada)
function traerInformacionCliente(clienteId) {

    let buscarClientesUrl = '/ventas/buscar_clientes/'; // URL para buscar clientes
    $.ajax({

        url: buscarClientesUrl, // URL de la solicitud
        data: {
            'numero': clienteId  // numero es el rut del cliente
        },
        dataType: 'json',
        
        success: function(data) {
            if (data.resultadosClientes && data.resultadosClientes.length > 0) {

                // Toma el primer cliente de los resultados (si estás esperando un solo cliente)
                const cliente = data.resultadosClientes[0];
                console.log("informacion del cliente: ",cliente)
                console.log('contacto de Cliente encontrado:', cliente.contactos);
                console.log('direcciones de Cliente encontrado:', cliente.direcciones);
                // Llamar a las funciones para actualizar contactos y direcciones
                
                actualizarContactos(cliente.contactos);
                actualizarDirecciones(cliente.direcciones, '#direcciones_despacho', "12");
                actualizarDirecciones(cliente.direcciones, '#direcciones_facturacion', "13");
            } else {
                console.log('No se encontraron clientes con el número proporcionado.');
            }
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
function actualizarDirecciones(direcciones, selectId, tipoDireccion) {
    let select = $(selectId); 
    select.empty();
    // Filtrar las direcciones según el tipoDireccion
    const direccionesFiltradas = direcciones.filter(function(direccion) {
        console.log("tipo direccion de contacto", direccion.tipoDireccion)
        return direccion.tipoDireccion === tipoDireccion;
    });

    console.log(direccionesFiltradas);
    if (direccionesFiltradas.length > 0) {
        direccionesFiltradas.forEach(function(direccion) {
            let option = $('<option></option>');
            option.val(direccion.id); //Ver este valor que se quiere usar como id unico
            option.text(direccion.nombreDireccion + ' - ' + direccion.ciudad + ', ' + direccion.comuna);
            select.append(option); 
        });
    } else {
        // Si no hay direcciones disponibles después del filtro, agregar una opción indicando esto
        let option = $('<option></option>');
        option.text('No hay direcciones disponibles');
        select.append(option);
    }
}