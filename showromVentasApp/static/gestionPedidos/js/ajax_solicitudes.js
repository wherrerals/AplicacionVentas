$(document).ready(function () {
    $('#inputNumero').on('input', function () { // escucha el evento de entrada en input con #inputNumero
        let numero = $(this).val();
        let tipoDoucmento = $('#tipoDocumento').text().trim();
        if (numero) {
            let buscarProductosUrl = '/ventas/buscarproductos/'; // URL para buscar productos
            $.ajax({ // realiza una solicitud ajax al servidor a la url buscar/
                url: buscarProductosUrl,
                data: {
                    'numero': numero // envia los datos ingresados por el usuario al servidor (sku)
                },
                dataType: 'json', // indica el formato en el que espera los datos
                success: function (data) { // si la respuesta del servidor es exitosa se ejecuta la funcion
                    $('#resultados').empty(); // limpia resultados anteriores
                    if (data.resultados && data.resultados.length > 0) { // comprueba si hay resultados y si estos son mayores que 0
                        data.resultados.forEach(function (resultado) { // si se obtienen resultados itera sobre estos para realizar:
                            // Convertir valores a números si son cadenas
                            resultado.precio = parseFloat(resultado.precio);
                            resultado.precioAnterior = resultado.precioAnterior;
                            resultado.maxDescuento = parseFloat(resultado.maxDescuento);
                            resultado.stockTotal = parseInt(resultado.stockTotal);
                            const sucursal = $('#sucursal').text().trim();
                            

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
                            productoElemento.textContent = `${resultado.codigo} | ${resultado.nombre} | Stock Total: ${resultado.stockTotal}`;

                            // Agregar evento de clic al elemento
                            productoElemento.addEventListener('click', function () {
                                let codigo = this.getAttribute('data-codigo');
                                let nombre = this.getAttribute('data-nombre');
                                let imagen = this.getAttribute('data-imagen');
                                let precioVenta = parseFloat(this.getAttribute('data-precio'));
                                let stockTotal = parseInt(this.getAttribute('data-stockTotal'));
                                let precioLista = parseFloat(this.getAttribute('data-precioAnterior'));
                                let precioDescuento = parseFloat(this.getAttribute('data-maxDescuento'));

                                if (stockTotal <= 0) {
                                   cantidad = 0;
                                } else {
                                      cantidad = 1;
                                  } 
                                
                                console.log('Producto seleccionado:', codigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento);
                                
                                agregarProducto(codigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal); // Ejecuta la función agregar producto

                                // Limpia el input #inputNumero al seleccionar un producto
                                $('#inputNumero').val('');
                            });

                            $('#resultados').append(productoElemento); // Agrega los resultados en el contenedor

                            $('#resultados').on('click', '*', function () {
                                // Limpiar el div #resultados al hacer clic en cualquier elemento dentro de él
                                $('#resultados').empty();
                            });
                        });
                    } else {
                        $('#resultados').text('No se encontraron resultados'); // Si no encuentra resultados muestra el mensaje
                    }
                }
            });
        } else {
            $('#resultados').empty(); // Si el usuario elimina el número borra todos los resultados.
        }
    });
});
