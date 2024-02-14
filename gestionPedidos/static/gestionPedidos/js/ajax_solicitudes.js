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
                            data-precio="${resultado.precioVenta}" 
                            data-stock="${resultado.stockTotal}" 
                            data-precio-actual="${resultado.precioVenta}" 
                            data-precio-anterior="${resultado.precioLista}" 
                            data-max-descuento="${resultado.dsctoMaxTienda}">ID: ${resultado.codigo}, Nombre: ${resultado.nombre}, Stock: ${resultado.stock}</p>`); 
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
        var precioVenta = $(this).data('precio');
        var stockTotal = $(this).data('stock');
        var precioVenta = $(this).data('precio-actual');
        var precioLista = $(this).data('precio-anterior');
        var dsctoMaxTienda = $(this).data('max-descuento');
        // Llamar a la función agregarProducto() con los valores obtenidos
        agregarProducto(codigo, stockTotal, precioVenta, precioLista, dsctoMaxTienda, precioVenta, precioVenta, nombre);
    });
});
