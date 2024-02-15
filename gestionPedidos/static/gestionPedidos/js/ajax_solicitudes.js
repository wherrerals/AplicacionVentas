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
                            $('#resultados').append(`<p class="agregar_productos" 
                            data-codigo="${resultado.codigo}" 
                            data-nombre="${resultado.nombre}"
                            data-imagen="${resultado.imagen}"
                            data-precio="${resultado.precioVenta}" 
                            data-stockTotal="${resultado.stockTotal}" 
                            data-precioActual="${resultado.precioVenta}" 
                            data-precioAnterior="${resultado.precioLista}" 
                            data-maxDescuento="${resultado.linkProducto}">ID: ${resultado.codigo}, Nombre: ${resultado.nombre}, Stock: ${resultado.stockTotal}</p>`); 
                            console.log('#resultados')
                        });
                    } else {
                        $('#resultados').text('No se encontraron resultados');
                    }
                }
            });
        } else {
            $('#resultados').empty();
        }
    });

    // Delegación de eventos para el clic en los elementos con clase 'agregar_productos'
    $('#resultados').on('click', '.agregar_productos', function() {
        // Obtener los datos del producto seleccionado
        var codigo = $(this).data('codigo');
        var nombre = $(this).data('nombre');
        var imagen = $(this).data('imagen');
        var precioVenta = $(this).data('precio');
        var stockTotal = $(this).data('stockTotal');
        var precioVenta = $(this).data('precioActual');
        var precioLista = $(this).data('precioAnterior');
        var linkProducto = $(this).data('maxDescuento');
        // Llamar a la función agregarProducto() con los valores obtenidos
        agregarProducto(codigo, nombre, imagen);
    });
});
