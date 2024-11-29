$(document).ready(function () {
    $('#inputCliente').on('input', function () {
        let inputValue = $(this).val().trim(); // Captura el valor ingresado y elimina espacios en blanco

        // Si el campo está vacío, limpia la información del cliente
        if (inputValue === '') {
            limpiarInformacionCliente();
            return; // Salimos de la función
        }

        // Solo realizar la búsqueda si el valor tiene al menos 3 caracteres
        if (inputValue.length >= 3) {
            let buscarClientesUrl = '/ventas/buscar_clientes/';

            $.ajax({
                url: buscarClientesUrl,
                data: {
                    'numero': inputValue || '', 
                    'nombre': inputValue || ''  
                },
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

        $('#inputCliente').val(`${codigoSN} - ${nombre} ${apellido}`);
        $('#inputCliente').attr('data-rut', clienteId);
        $('#inputCliente').attr('data-codigoSN', codigoSN);

        $('#resultadosClientes').empty();

        traerInformacionCliente(clienteId);
    });
});

function limpiarInformacionCliente() {
    $('#inputCliente').val(''); // Limpia el campo de entrada
    $('#inputCliente').removeAttr('data-rut').removeAttr('data-codigoSN'); // Elimina los atributos
    $('#resultadosClientes').empty(); // Vacía el contenedor de resultados

    // Restablece el select de contactos con la opción predeterminada
    $('#clientes').html(`
        <option value="">Seleccione un contacto</option>
    `);

    // Restablece los selects de direcciones con opciones predeterminadas
    $('#direcciones_despacho').html('<option value="">Seleccione una dirección de despacho</option>');
    $('#direcciones_facturacion').html('<option value="">Seleccione una dirección de facturación</option>');

    console.log("Información del cliente limpia.");
}
