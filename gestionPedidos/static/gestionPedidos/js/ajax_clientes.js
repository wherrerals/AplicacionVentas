$(document).ready(function(){
    $('#inputCliente').on('input', function(){
        var numero = $(this).val();
        if(numero){
            $.ajax({
                url: 'buscarc/',
                data:{
                    'numero': numero
                },
                dataType: 'json',
                success: function(data){
                    console.log(data); // Agregando console.log para ver los datos recibidos
                    $('#resultadosClientes').empty(); // Limpiando el contenedor antes de agregar nuevos elementos
                    if(data.resultadosClientes && data.resultadosClientes.length > 0){
                        data.resultadosClientes.forEach(function(resultadosClientes) {
                            var clientesElemento = $('<p></p>'); // Creando un nuevo elemento <option> con jQuery
                            clientesElemento.addClass('informacion_clientes'); // Agregando la clase al elemento
                            clientesElemento.attr('data-nombre', resultadosClientes.nombre); // Agregando el atributo data-nombre
                            clientesElemento.attr('data-apellido', resultadosClientes.apellido); // Agregando el atributo data-apellido
                            clientesElemento.text(resultadosClientes.nombre + ' ' + resultadosClientes.apellido); // Agregando el texto al elemento
                            console.log(clientesElemento);

                            $('#resultadosClientes').append(clientesElemento); // Agregando el elemento al contenedor
                            console.log("Se agregó un elemento <option> al select #resultadosClientes.");
                        });
                    } else {
                        $('#resultadosClientes').text('No se encontraron resultados'); // Si no encuentra resultados muestra el mensaje
                    }
                },
                complete: function(){ // Agregando la función completa para borrar los resultados si el usuario elimina el contenido
                    if(!numero){
                        $('#resultadosClientes').empty();
                    }
                }
            });
        } else {
            $('#resultadosClientes').empty();
        }
    });
});

