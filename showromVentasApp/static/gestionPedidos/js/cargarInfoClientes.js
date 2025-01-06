// Función para rellenar los campos del modal con la información del cliente seleccionado
function cargarInformacionClienteEnModal(cliente) {
    // Agregar logs para verificar si los datos están llegando correctamente
    console.log("Cargando información del cliente en el modal:", cliente);

    // Nombre y Apellido
    $('#nombreSN').val(cliente.nombre);
    $('#apellidoSN').val(cliente.apellido);
    //console.log("Nombre:", cliente.nombre, "Apellido:", cliente.apellido);

    // RUT
    $('#rutSN').val(cliente.rut);
    //console.log("RUT:", cliente.rut);
    $('#rutSN').prop('readonly', true);
    
    // Giro
    $('#giroSN').val(cliente.giro);
    //console.log("Giro:", cliente.giro);

    // Teléfono
    $('#telefonoSN').val(cliente.telefono);
    //console.log("Teléfono:", cliente.telefono);

    // Email
    $('#emailSN').val(cliente.email);
    //console.log("Email:", cliente.email);

    // Tipo de cliente (Persona o Empresa)
    if (cliente.razonSocial === '') {
        $('#formCheck-5').prop('checked', true);  // Persona
        //console.log("Tipo de cliente: Persona");
    } else {
        $('#formCheck-6').prop('checked', true);  // Empresa
        //console.log("Tipo de cliente: Empresa");
    }

    $('#svgdircont').hide();
    //console.log("Div svgdircont ocultado");

}

// Llamada para abrir el modal y cargar la información
$('#botonModal').on('click', function() {
    var clienteId = $('#inputCliente').attr('data-rut');  // Obtener el RUT del cliente seleccionado
    console.log("Cliente ID (RUT) obtenido:", clienteId);  // Verifica si el cliente ID se obtiene correctamente

    if (clienteId) {
        console.log("Cliente seleccionado, trayendo información del cliente...");

        // Traer la información completa del cliente usando la función que ya tienes implementada
        traerInformacionCliente(clienteId); 
    } else {
        console.log("No hay cliente seleccionado, abriendo modal vacío...");
        // Abre el modal sin cargar información si no hay cliente seleccionado
        var modalDefault = new bootstrap.Modal(document.getElementById('clienteModal'));
        modalDefault.show();
    }
});
