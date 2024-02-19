$(document).ready(function(){
    $('#inputNumero').on('input', function(){ //escucha el evento de entrada en input con #inputNumero
        var numero = $(this).val();
        if(numero){
            $.ajax({ //realiza una solicitud ajax al servidor a la url buscar/
                url: 'buscar/', 
                data: {
                    'numero': numero //envia los datos ingresados por el usuario al servidor (sku)
                },
                dataType: 'json',  //indica el formato en el que espera los datos
                success: function(data){ // si la respuesta del servidor es exitosa se ejecuta la funcion
                    $('#resultados').empty(); //limpia resultados anteriores
                    if(data.resultados && data.resultados.length > 0){ //comprueba si hay resultados y si estos son mayores que 0
                        data.resultados.forEach(function(resultado){ // si se obtienen resultados itera sonbre estos para realizar:
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
                            productoElemento.textContent = `ID: ${resultado.codigo} | Nombre: ${resultado.nombre} | Stock: ${resultado.stockTotal}`;

                            // Agregar evento de clic al elemento
                            productoElemento.addEventListener('click', function() {
                                var codigo = this.getAttribute('data-codigo');
                                var nombre = this.getAttribute('data-nombre');
                                var imagen = this.getAttribute('data-imagen');
                                var precioVenta = parseFloat(this.getAttribute('data-precio'));
                                var stockTotal = parseInt(this.getAttribute('data-stockTotal'));
                                var precioLista = parseFloat(this.getAttribute('data-precioAnterior'));
                                var precioDescuento = parseFloat(this.getAttribute('data-maxDescuento'));
                                
                                agregarProducto(codigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento); //ejecuta la funcion agregar producto
                            });

                            $('#resultados').append(productoElemento); //agrega los resultados en el contenedor 
                        });
                    } else {
                        $('#resultados').text('No se encontraron resultados'); //si no encuentra resultados muestra el mensaje
                    }
                }
            });
        } else {
            $('#resultados').empty(); // si el usuario elimina el codito borra todos los resultados.
        }
    });
});
