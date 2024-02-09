$(document).ready(function(){
    $('#inputNumero').on('input', function(){
        var numero = $(this).val();
        if(numero){
            $.ajax({
                url: 'buscar/',
                data: {
                    'numero': numero
                },
                dataType: 'json',
                success: function(data){
                    $('#resultados').empty();
                    if(data.resultados && data.resultados.length > 0){
                        data.resultados.forEach(function(resultado){
                            $('#resultados').append('<p>ID: ' + resultado.codigo + ', Nombre: ' + resultado.nombre + '</p>'); 
                        });
                    } else {
                        $('#resultados').text('No se encontraron resultados');
                    }
                }
            });
        } else {
            $('#resultados').empty();
            console.log("prueba")
        }
    });
});