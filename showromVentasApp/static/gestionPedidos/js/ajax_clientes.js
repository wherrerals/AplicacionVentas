$(document).ready(function () {
    $('#inputCliente, #rutSN').on('input', function () {
        let inputValue = $(this).val().trim(); // Captura el valor ingresado y elimina espacios en blanco

        // Si el campo está vacío, limpia la información del cliente
        if (inputValue === '') {
            limpiarInformacionCliente();
            return; // Salimos de la función
        }

        // Solo realizar la búsqueda si el valor tiene al menos 3 caracteres
        if (inputValue.length >= 3) {
            let buscarClientesUrl = '/ventas/buscar_clientes/';
            let parametros = {};

            // Detectamos si el valor contiene solo números y puntos
            if (/^[0-9.]+$/.test(inputValue)) {
                parametros = { 'numero': inputValue, 'nombre': '' }; // Buscar por número
            } else {
                parametros = { 'numero': '', 'nombre': inputValue }; // Buscar por nombre
            }

            $.ajax({
                url: buscarClientesUrl,
                data: parametros, // Enviamos los parámetros adecuados
                dataType: 'json',
                success: function (data) {
                    $('#resultadosClientes').empty();
                    if (data.resultadosClientes && data.resultadosClientes.length > 0) {
                        data.resultadosClientes.forEach(function (resultado) {
                            let clientesElemento = $('<p></p>');
                            clientesElemento.addClass('suggestion-item');
                            clientesElemento.attr('data-nombre', resultado.nombre);
                            clientesElemento.attr('data-apellido', resultado.apellido);
                            clientesElemento.attr('data-codigoSN', resultado.codigoSN);
                            clientesElemento.attr('data-rut', resultado.rut);
                            clientesElemento.text(
                                `${resultado.codigoSN} - ${resultado.nombre} ${resultado.apellido}`
                            );
                            $('#resultadosClientes').append(clientesElemento);
                        });
                    } else {
                        $('#resultadosClientes').html('No se encontraron resultados');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error en la solicitud AJAX:', error);
                }
            });
        } else {
            // Si el valor es menor a 3 caracteres, vacía los resultados
            $('#resultadosClientes').empty();
        }
    });

    // Delegamos el evento click al contenedor para elementos creados dinámicamente
    $('#resultadosClientes').on('click', '.suggestion-item', function () {
        let nombre = $(this).attr('data-nombre');
        let apellido = $(this).attr('data-apellido');
        let clienteId = $(this).attr('data-rut');
        let codigoSN = $(this).attr('data-codigoSN');

        // Actualizar valores en el DOM
        $('#inputCliente').val(`${codigoSN} - ${nombre} ${apellido}`);
        $('#inputCliente').attr('data-rut', clienteId)
        $('#rutSN').val(clienteId);
        $('#rutSN').attr('data-rut', clienteId); // Actualiza el atributo data-rut
        $('#inputCliente').attr('data-codigoSN', codigoSN);

        // Limpiar los resultados
        $('#resultadosClientes').empty();

        traerInformacionCliente(clienteId);
        const rutDisplayParagraph = document.querySelector('#rut-display p');
        const rutSinPuntos = clienteId.replace(/\./g, '')
        const modifiedText = rutSinPuntos.length > 0 ? rutSinPuntos.slice(0, -1) + 'C' : '';
        rutDisplayParagraph.textContent = modifiedText;

        // Llamar a las funciones cargarContactos y cargarDirecciones
        cargarDirecciones();
        cargarContactos();

    });
});

function limpiarInformacionCliente() {
    $('#inputCliente').val(''); // Limpia el campo de entrada
    $('#rutSN').val(''); // Limpia el campo de RUT
    $('#rutSN').removeAttr('data-rut'); // Limpia el atributo data-rut
    $('#inputCliente').removeAttr('data-rut').removeAttr('data-codigoSN'); // Elimina los atributos
    $('#resultadosClientes').empty(); // Vacía el contenedor de resultados
    $('#nombreSN').val('');
    $('#apellidoSN').val(''); 
    $('#rutSN').val('');
    $('#codigoSN').val('');
    $('#telefonoSN').val('');
    $('#emailSN').val('');
    $('#giroSN').val('');

    // Restablece el select de contactos con la opción predeterminada
    $('#clientes').html(`
        <option value="">Seleccione un contacto</option>
    `);

    // Restablece los selects de direcciones con opciones predeterminadas
    $('#direcciones_despacho').html('<option value="">Seleccione una dirección de despacho</option>');
    $('#direcciones_facturacion').html('<option value="">Seleccione una dirección de facturación</option>');

    console.log("Información del cliente limpia.");
}
