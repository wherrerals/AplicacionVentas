// Hereda de ValorTributarioBase (interaccionBase.js).
class valorTributario extends ValorTributarioBase {
    calcularValores() {
        var precioFinal = parseFloat(this.precioFinal) || 0;
        var bruto = Math.round(precioFinal / 1.19);
        var neto = precioFinal;
        var iva = bruto - neto;
        return {
            bruto: bruto,
            neto: Math.round(neto),
            iva: Math.round(iva)
        };
    }
}

function agregarInteractividad(newRow, codigoProducto, indiceProducto) {
    var inputCantidad = newRow.querySelector('#calcular_cantidad');
    var inputDescuento = newRow.querySelector('#agg_descuento');
    var inputPrecioVenta = newRow.querySelector('#precio_venta2');
    var tdPrecioVenta = newRow.querySelector('#precio_Venta');
    var tdPrecioDescuento = newRow.querySelector('#Precio_Descuento');

    var valorBruto = document.querySelector('#total_bruto small');
    var valorIva = document.querySelector('#iva small');
    var valorNeto = document.querySelector('#total_neto small');

    var producto = new valorTributario(codigoProducto, parseFloat(inputPrecioVenta.value) || 0, indiceProducto);
    productos.push(producto);

    console.log('Producto agregado:', producto);

    const switchCheckbox = newRow.querySelector('.switch-producto');
    if (switchCheckbox) {
        switchCheckbox.addEventListener('change', () => {

            switchCheckbox.dataset.estado = switchCheckbox.checked ? "1" : "0";

            actualizarValores();
            manejarSwitches();
            console.log(`Switch cambiado para el producto: ${codigoProducto}, Índice: ${indiceProducto}`);
            console.log(`Nuevo estado data-estado: ${switchCheckbox.dataset.estado}`);

        });
    }

    inputCantidad.addEventListener('input', calcularPrecioTotal);
    inputDescuento.addEventListener('input', calcularPrecioTotal);
    inputPrecioVenta.addEventListener('input', actualizarPrecioVenta);

    calcularPrecioTotal();

    function actualizarPrecioVenta() {
        producto.precioFinal = parseFloat(inputPrecioVenta.value) || 0;
        calcularPrecioTotal();
    }

    function calcularPrecioTotal() {
        var cantidad = parseFloat(inputCantidad.value) || 0;
        var precioUnitario = parseFloat(inputPrecioVenta.value) || 0;
        var descuento = parseFloat(inputDescuento.value) || 0;

        var precioTotal = cantidad * precioUnitario;
        var precioFinal = descuento === 0 ? precioTotal : precioTotal - (precioTotal * (descuento / 100));
        var precioConDescuento = precioUnitario * (1 - (descuento / 100));

        console.log('Precio final:', precioFinal, 'Precio con descuento:', precioConDescuento);

        let precioFinaldefinido = Math.round(precioFinal * 1000) / 1000;
        let precioConDescuentodefinido = Math.round(precioConDescuento * 1000) / 1000;

        const precioNeto_n = precioUnitario / 1.19;
        let precioConDescuento2 = precioNeto_n * (1 - (descuento / 100));
        precioConDescuento2 = Math.round(precioConDescuento2 * 10000) / 10000;
        let precioFinal_n = precioConDescuento2 * cantidad;
        precioFinal_n = Math.round(precioFinal_n);

        producto.modificarPrecioFinal(precioFinal_n);

        tdPrecioVenta.textContent = formatCurrency( Math.round(precioFinal_n * 1.19));
        tdPrecioDescuento.textContent = formatCurrency(precioConDescuentodefinido);

        actualizarValores();
    }

    document.addEventListener('productoEliminado', function (event) {
        const { codigoProducto, indiceProducto } = event.detail;

        console.log(`Producto eliminado: ${codigoProducto}, Índice: ${indiceProducto}`);

        // Eliminar solo el producto con el índice específico
        const index = productos.findIndex(producto =>
            producto.codigoProducto === codigoProducto && producto.indiceProducto == indiceProducto
        );

        if (index > -1) {
            productos.splice(index, 1);
        }


        // Actualizar los valores totales
        actualizarValores();
    });


    function actualizarValores() {
        let totalIva = 0;
        let totalBruto = 0;
        let totalNeto = 0;

        productos.forEach(producto => {
            // Buscar la fila del producto usando el índice
            const filaProducto = document.querySelector(`.product-row[data-indice="${producto.indiceProducto}"]`);

            // Verifica si la fila existe y si el switch está activado
            if (filaProducto) {
                const checkbox = filaProducto.querySelector('.switch-producto');
                if (checkbox && checkbox.checked) {
                    const valores = producto.calcularValores();
                    //totalIva += valores.iva;
                    totalNeto += valores.neto;
                    totalBruto = Math.round(totalNeto * 1.19);
                    totalIva = totalBruto - totalNeto;
                }
            }
        });

        document.querySelector('#total_neto').setAttribute('data-total-neto', totalNeto);
        document.querySelector('#total_bruto').setAttribute('data-total-bruto', totalBruto);

        totalIva = Math.round(totalIva);
        totalBruto = Math.round(totalBruto);
        totalNeto = Math.round(totalNeto);

        document.querySelector('#iva').textContent = formatCurrency(totalIva);
        document.querySelector('#total_bruto').textContent = formatCurrency(totalBruto);
        document.querySelector('#total_neto').textContent = formatCurrency(totalNeto);
    }

}

// formatCurrency vive en productosUtils.js