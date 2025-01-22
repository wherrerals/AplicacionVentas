// Dependencias: valorTributario.js
class valorTributario {
    constructor(codigoProducto, precioFinal) {
        this.codigoProducto = codigoProducto;
        this.precioFinal = precioFinal;
    }

    // Metodo para modificar el precio final
    modificarPrecioFinal(precioFinal) {
        this.precioFinal = precioFinal;
    }

    // Metodo para calcular IVA, bruto y neto
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

// Array global para almacenar las instancias de valorTributario
const productos = [];

function agregarInteractividad(newRow, codigoProducto) {
    // Obtener referencias a los elementos dentro de la fila
    var inputCantidad = newRow.querySelector('#calcular_cantidad');
    var inputDescuento = newRow.querySelector('#agg_descuento');
    var spanPrecioVenta = newRow.querySelector('small[name="precio_venta"]');
    var tdPrecioVenta = newRow.querySelector('#precio_Venta');
    var tdPrecioDescuento = newRow.querySelector('#Precio_Descuento');

    // Select the small elements inside the divs by their ID
    var valorBruto = document.querySelector('#total_bruto small');
    var valorIva = document.querySelector('#iva small');
    var valorNeto = document.querySelector('#total_neto small');

    // Crear instancia de valorTributario y agregarla al array
    var producto = new valorTributario(codigoProducto, 0);
    productos.push(producto);

    console.log('Producto agregado:', producto);

    // Agregar evento de cambio al input de cantidad para calcular el precio total
    inputCantidad.addEventListener('input', calcularPrecioTotal);

    // Agregar evento de cambio al input de descuento para aplicar el descuento
    inputDescuento.addEventListener('input', aplicarDescuento);

    // Llamar a calcularPrecioTotal para inicializar los valores al agregar el producto
    calcularPrecioTotal();

    // Función para calcular el precio total
    function calcularPrecioTotal() {
        var cantidad = parseFloat(inputCantidad.value) || 0;
        var precioUnitario = parseFloat(spanPrecioVenta.textContent) || 0;
        var precioTotal = cantidad * precioUnitario;
        var descuento = parseFloat(inputDescuento.value) || 0;

        // Si el descuento es 0, el precio con descuento también será 0
        var precioFinal = descuento === 0 ? precioTotal : precioTotal - (precioTotal * (descuento / 100));
        var precioConDescuento = descuento === 0 ? 0 : precioUnitario * (1 - (descuento / 100));

        // Actualizar el producto en la lista
        producto.modificarPrecioFinal(precioFinal);

        tdPrecioVenta.textContent = precioFinal.toFixed(2);
        tdPrecioDescuento.textContent = precioConDescuento.toFixed(2);

        actualizarValores();
    }

    // Función para aplicar el descuento
    function aplicarDescuento() {
        calcularPrecioTotal();
    }

    document.addEventListener('productoEliminado', function (event) {
        const codigoProducto = event.detail.codigoProducto;
        console.log('Producto eliminado:', codigoProducto);

        // Buscar el índice del producto a eliminar
        const index = productos.findIndex(producto => producto.codigoProducto === codigoProducto);
        console.log('Índice encontrado:', index);

        if (index > -1) {
            productos.splice(index, 1);
        }

        // Imprimir el estado actual del array productos después de la eliminación
        console.log('Estado actual del array productos:', productos);

        // Actualizar los valores totales
        actualizarValores();
    });

    // Función para actualizar los valores de IVA, bruto y neto sumando todos los productos
    function actualizarValores() {
        let totalIva = 0;
        let totalBruto = 0;
        let totalNeto = 0;

        productos.forEach(producto => {
            const valores = producto.calcularValores();
            totalIva += valores.iva;
            totalBruto += valores.bruto;
            totalNeto += valores.neto;
        });

        // Redondear los totales al final
        totalIva = Math.round(totalIva);
        totalBruto = Math.round(totalBruto);
        totalNeto = Math.round(totalNeto);

        console.log('Total IVA:', totalIva, 'Total Bruto:', totalBruto, 'Total Neto:', totalNeto);

        document.querySelector('#iva').textContent = `$${totalIva.toFixed(0)}`;
        document.querySelector('#total_bruto').textContent = `$${totalBruto.toFixed(0)}`;
        document.querySelector('#total_neto').textContent = `$${totalNeto.toFixed(0)}`;
    }

}
