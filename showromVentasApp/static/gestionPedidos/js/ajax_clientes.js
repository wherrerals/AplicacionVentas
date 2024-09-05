$(document).ready(function(){
    $('#inputCliente').on('input', function(){
        let numero = $(this).val().trim(); // Trim para eliminar espacios en blanco al inicio y al final
        if(numero){ // Verificar si el número no está vacío
            // Define la URL directamente en el archivo JavaScript
            let buscarClientesUrl = '/ventas/buscar_clientes/';

            $.ajax({
                url: buscarClientesUrl,
                data:{
                    'numero': numero
                },
                dataType: 'json',
                success: function(data){
                    console.log(data);
                    $('#resultadosClientes').empty();
                    if(data.resultadosClientes && data.resultadosClientes.length > 0){
                        data.resultadosClientes.forEach(function(resultadosClientes) {
                            var clientesElemento = $('<p></p>');
                            clientesElemento.addClass('suggestion-item');
                            clientesElemento.attr('data-nombre', resultadosClientes.nombre);
                            clientesElemento.attr('data-apellido', resultadosClientes.apellido);
                            clientesElemento.attr('data-rut', resultadosClientes.rut);
                            clientesElemento.text(resultadosClientes.nombre + ' ' + resultadosClientes.apellido);
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
            $('#resultadosClientes').empty(); // Limpiar el contenedor si el número está vacío
        }
    });
});


