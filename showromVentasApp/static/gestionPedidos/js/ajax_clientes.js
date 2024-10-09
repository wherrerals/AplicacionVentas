$(document).ready(function(){
    $('#inputCliente').on('input', function(){
        let inputValue = $(this).val().trim(); // Captura el valor ingresado y elimina espacios en blanco

        // Solo realizar la búsqueda si el valor tiene al menos 3 caracteres
        if(inputValue.length >= 3){
            let numero = inputValue; // Puedes usar el mismo valor tanto para número como para nombre
            let nombre = inputValue; // Si ingresan nombre en lugar de número, igual capturamos el input

            // Define la URL directamente en el archivo JavaScript
            let buscarClientesUrl = '/ventas/buscar_clientes/';

            $.ajax({
                url: buscarClientesUrl,
                data: {
                    'numero': numero || '', // Enviar número si está disponible, de lo contrario enviar vacío
                    'nombre': nombre || ''  // Enviar nombre si está disponible, de lo contrario enviar vacío
                },
                dataType: 'json',
                success: function(data){
                    console.log("estos son los datos del cliente", data);
                    $('#resultadosClientes').empty();
                    if(data.resultadosClientes && data.resultadosClientes.length > 0){
                        data.resultadosClientes.forEach(function(resultadosClientes) {
                            var clientesElemento = $('<p></p>');
                            clientesElemento.addClass('suggestion-item');
                            clientesElemento.attr('data-nombre', resultadosClientes.nombre);
                            clientesElemento.attr('data-apellido', resultadosClientes.apellido);
                            clientesElemento.attr('data-codigoSN', resultadosClientes.codigoSN);
                            clientesElemento.attr('data-rut', resultadosClientes.rut);
                            clientesElemento.text(resultadosClientes.codigoSN + ' - ' + resultadosClientes.nombre + ' ' + resultadosClientes.apellido);
                            console.log(clientesElemento);

                            $('#resultadosClientes').append(clientesElemento);
                            console.log("Se agregó un elemento <option> al select #resultadosClientes: " + resultadosClientes.nombre + ' ' + resultadosClientes.apellido + ' ' + numero);
                        });
                    } else {
                        $('#resultadosClientes').html('No se encontraron resultados'); // Utilizar html() en lugar de text()
                    }
                },
                error: function(xhr, status, error) { // Maneja errores de la solicitud AJAX
                    console.error('Error en la solicitud AJAX:', error);
                }
            });
        } else {
            $('#resultadosClientes').empty(); // Limpiar el contenedor si el input tiene menos de 3 caracteres
        }
    });
});
