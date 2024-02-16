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
                    console.log("resultado", data);
                    console.log("resultado2", typeof data);
                    $('#resultados').empty();
                    if(data.resultados && data.resultados.length > 0){
                        data.resultados.forEach(function(resultado){
                            // Convertir valores a números si son cadenas
                            resultado.precio = parseFloat(resultado.precio);
                            resultado.precioAnterior = resultado.precioAnterior;
                            resultado.maxDescuento = parseFloat(resultado.maxDescuento);
                            resultado.stockTotal = parseInt(resultado.stockTotal);
                            
                            // Agregar elementos al resultado
                            var productoElemento = document.createElement('p');
                            productoElemento.className = 'agregar_productos';
                            productoElemento.setAttribute('data-codigo', resultado.codigo);
                            productoElemento.setAttribute('data-nombre', resultado.nombre);
                            productoElemento.setAttribute('data-imagen', resultado.imagen);
                            productoElemento.setAttribute('data-precio', resultado.precio);
                            productoElemento.setAttribute('data-stockTotal', resultado.stockTotal);
                            productoElemento.setAttribute('data-precioAnterior', resultado.precioAnterior);
                            productoElemento.setAttribute('data-maxDescuento', resultado.maxDescuento);
                            productoElemento.textContent = `ID: ${resultado.codigo}, Nombre: ${resultado.nombre}, Stock: ${resultado.stockTotal}`;

                            // Agregar evento de clic al elemento
                            productoElemento.addEventListener('click', function() {
                                var codigo = this.getAttribute('data-codigo');
                                var nombre = this.getAttribute('data-nombre');
                                var imagen = this.getAttribute('data-imagen');
                                var precioVenta = parseFloat(this.getAttribute('data-precio'));
                                var stockTotal = parseInt(this.getAttribute('data-stockTotal'));
                                var precioLista = parseFloat(this.getAttribute('data-precioAnterior'));
                                var precioDescuento = parseFloat(this.getAttribute('data-maxDescuento'));
                                
                                agregarProducto(codigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento);
                            });

                            $('#resultados').append(productoElemento); 
                            console.log(resultado);
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
});
