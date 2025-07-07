// Dependencias: valorTributario.js
class valorTributario {
    constructor(codigoProducto, precioFinal, indiceProducto) {
        this.codigoProducto = codigoProducto;
        this.precioFinal = precioFinal;
        this.indiceProducto = indiceProducto;
    }

    modificarPrecioFinal(precioFinal) {
        this.precioFinal = precioFinal;
    }

    calcularValores() {
        var precioFinal = parseFloat(this.precioFinal) || 0;
        var bruto = precioFinal;
        var neto = precioFinal / 1.19;
        var iva = bruto - neto;
        return {
            bruto: bruto,
            neto: neto,
            iva: iva
        };
    }
}

const productos = [];

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
            actualizarValores();
            console.log(`Switch cambiado para el producto: ${codigoProducto}, Índice: ${indiceProducto}`);
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
        var precioConDescuento = descuento === 0 ? 0 : precioUnitario * (1 - (descuento / 100));

        console.log('Precio final:', precioFinal, 'Precio con descuento:', precioConDescuento);

        let precioFinaldefinido = Math.round(precioFinal);
        let precioConDescuentodefinido = Math.round(precioConDescuento);

        producto.modificarPrecioFinal(precioFinal);

        tdPrecioVenta.textContent = formatCurrency(precioFinaldefinido);
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
                    totalIva += valores.iva;
                    totalBruto += valores.bruto;
                    totalNeto += valores.neto;
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

function formatCurrency(value) {
    const integerValue = Math.floor(value);
    let formattedValue = integerValue.toLocaleString('es-ES', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });

    if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
        formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
    }

    return `$ ${formattedValue}`;
}
