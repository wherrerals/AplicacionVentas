// Función para rellenar los campos del modal con la información del cliente seleccionado
function cargarInformacionClienteEnModal(cliente) {
    // Agregar logs para verificar si los datos están llegando correctamente
    console.log("Cargando información del cliente en el modal:", cliente);
    console.log("grupoSN:", cliente.grupoSN);

    if (cliente.grupoSN === '105') {
        $('#nombreSN').val(cliente.nombre);
        $('#apellidoSN').val(cliente.apellido);
        console.log("Cliente pertenece al grupo 105");
    } else {
        console.log("Cliente pertenece al grupo 100");
        $('#nombreSN').val(cliente.razonSocial); 
    }
    

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
    if (cliente.grupoSN === '105') {
        console.log("Cliente pertenece al grupo 105");
        $('#formCheck-5').prop('checked', true);  // Persona
        //console.log("Tipo de cliente: Persona");
        const razonSocialRadioName = 'grupoSN';
        const nombreLabelId = 'nombreSN';
        const apellidoInputId = 'apellidoSN';
        const apellidolabelId = 'apellidorow';
        cambiarLabel(razonSocialRadioName, nombreLabelId, apellidoInputId, apellidolabelId)
    } else {
        console.log("Cliente pertenece al grupo 100");
        $('#formCheck-6').prop('checked', true);  // Empresa
        const razonSocialRadioName = 'grupoSN';
        const nombreLabelId = 'nombreSN';
        const apellidoInputId = 'apellidoSN';
        const apellidolabelId = 'apellidorow';
        cambiarLabel(razonSocialRadioName, nombreLabelId, apellidoInputId, apellidolabelId)
        //console.log("Tipo de cliente: Empresa");
    }

    $('#svgdircont').hide();
    //console.log("Div svgdircont ocultado");

}

// ─── Precarga por RUT en el formulario de cliente ───
// Si el usuario escribe el RUT de un cliente ya registrado (en vez de
// seleccionarlo desde la búsqueda), se cargan sus datos y el guardado pasa a
// ser una actualización: evita el error al intentar "crear" un RUT existente
// y que un formulario a medio llenar pise la data ya registrada.

// El endpoint informacion_cliente arma el cardCode como cuerpo + "C", por lo
// que hay que consultar solo con el cuerpo del RUT (sin puntos ni dígito verificador)
function extraerCuerpoRut(rutTexto) {
    const limpio = (rutTexto || '').replace(/\./g, '').replace(/\s/g, '').toUpperCase();
    if (limpio.includes('-')) {
        return limpio.split('-')[0];
    }
    // Sin guion: asumir que el último carácter es el dígito verificador
    return limpio.length > 7 ? limpio.slice(0, -1) : limpio;
}

function quitarAvisoClienteExistente() {
    $('#avisoClienteExistente').remove();
}

function mostrarAvisoClienteExistente() {
    quitarAvisoClienteExistente();

    const aviso = $(`
        <div id="avisoClienteExistente" class="alert alert-warning" role="alert" style="font-size: 12px; margin-top: 8px; margin-bottom: 8px;">
            Este cliente ya está registrado: se cargaron sus datos y al guardar se <strong>actualizará</strong>.
        </div>
    `);

    const filaRut = $('#rutSN').closest('.row');
    if (filaRut.length) {
        filaRut.after(aviso);
    } else {
        $('#rutSN').after(aviso);
    }
}

let ultimoRutPrecargado = null;

$(document).on('blur', '#rutSN', function () {
    const input = $(this);
    const cuerpoRut = extraerCuerpoRut(input.val());

    // No consultar si ya está en modo edición, el RUT es muy corto
    // o es el mismo que ya se precargó
    if (input.prop('readonly') || cuerpoRut.length < 7 || cuerpoRut === ultimoRutPrecargado) {
        return;
    }

    $.ajax({
        url: '/ventas/informacion_cliente/',
        type: 'GET',
        data: { rut: cuerpoRut },
        dataType: 'json',
        success: function (data) {
            if (!Array.isArray(data) || data.length === 0) {
                return;
            }

            // Preferir la coincidencia exacta de RUT; si no, el primer resultado
            const cliente = data.find(c => extraerCuerpoRut(c.rut) === cuerpoRut) || data[0];

            console.log("Cliente ya registrado, precargando datos:", cliente);
            ultimoRutPrecargado = cuerpoRut;

            cargarInformacionClienteEnModal(cliente);

            // Dejarlo como cliente seleccionado para que el guardado envíe su
            // cardCode y el backend actualice en vez de intentar crear
            $('#inputCliente')
                .attr('data-rut', extraerCuerpoRut(cliente.rut))
                .attr('data-codigoSN', cliente.codigoSN || '');

            mostrarAvisoClienteExistente();
        },
        error: function () {
            // RUT no registrado: sigue el flujo normal de creación
        }
    });
});

// Si el usuario vuelve a editar el RUT, retirar el aviso
$(document).on('input', '#rutSN', function () {
    quitarAvisoClienteExistente();
    ultimoRutPrecargado = null;
});

// Al cerrar el modal, volver al modo creación
$(document).on('hidden.bs.modal', '#clienteModal', function () {
    quitarAvisoClienteExistente();
    $('#rutSN').prop('readonly', false);
    ultimoRutPrecargado = null;
});

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
