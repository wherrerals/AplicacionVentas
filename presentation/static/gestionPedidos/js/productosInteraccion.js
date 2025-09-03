// Dependencias: valorTributario.js
class valorTributario {
    constructor(codigoProducto, precioFinal, indiceProducto) {
        this.codigoProducto = codigoProducto;
        this.precioFinal = precioFinal;
        this.indiceProducto = indiceProducto;
    }

    // Metodo para modificar el precio final
    modificarPrecioFinal(precioFinal) {
        this.precioFinal = precioFinal;
    }

    // Metodo para calcular IVA, bruto y neto
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

// Array global para almacenar las instancias de valorTributario
const productos = [];

function agregarInteractividad(newRow, codigoProducto, indiceProducto) {
    // Obtener referencias a los elementos dentro de la fila
    var inputCantidad = newRow.querySelector('#calcular_cantidad');
    var inputDescuento = newRow.querySelector('#agg_descuento');
    var spanPrecioVenta = newRow.querySelector('small[name="precio_venta"]').getAttribute('data-precioUnitario');
    var tdPrecioVenta = newRow.querySelector('#precio_Venta');
    var tdPrecioDescuento = newRow.querySelector('#Precio_Descuento');

    // Select the small elements inside the divs by their ID
    var valorBruto = document.querySelector('#total_bruto small');
    var valorIva = document.querySelector('#iva small');
    var valorNeto = document.querySelector('#total_neto small');

    // Crear instancia de valorTributario y agregarla al array
    var producto = new valorTributario(codigoProducto, 0, indiceProducto);
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
        var precioUnitario = parseFloat(spanPrecioVenta) || 0;
        var precioTotal = cantidad * precioUnitario;
        //var descuento = parseFloat(inputDescuento.value) || 0;

        // Verificar si hay un cupon visible con descuento aplicado
        var cuponInfo = newRow.querySelector('#desc_cupon');
        var descuento = 0;

        if (cuponInfo && !cuponInfo.hidden && cuponInfo.dataset.value) {
            descuento = parseFloat(cuponInfo.dataset.value) || 0;
        } else {
            descuento = parseFloat(inputDescuento.value) || 0;
        }

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
        console.log('Precio Unitario:', precioUnitario, 'Precio neto:', precioNeto_n, 'Precio con descuento redondeado:', precioConDescuento2, 'Precio final antes de IVA:', precioFinal_n, 'Precio final después de IVA:', precioFinal_n,);

        // Actualizar el producto en la lista
        producto.modificarPrecioFinal(precioFinal_n);

        tdPrecioVenta.textContent = formatCurrency( Math.round(precioFinal_n * 1.19));
        tdPrecioDescuento.textContent = formatCurrency(precioConDescuentodefinido);

        actualizarValores();
    }

    // Función para aplicar el descuento
    function aplicarDescuento() {
        calcularPrecioTotal();
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
    

    // Función para actualizar los valores de IVA, bruto y neto sumando todos los productos
    function actualizarValores() {
        let totalIva = 0;
        let totalBruto = 0;
        let totalNeto = 0;
    
        productos.forEach(producto => {
            const valores = producto.calcularValores();
            //totalIva += valores.iva;
            totalNeto += valores.neto;
            totalBruto = Math.round(totalNeto * 1.19);
            totalIva = totalBruto - totalNeto;


            console.log('totalIva:', totalIva, 'totalBruto:', totalBruto, 'totalNeto:', totalNeto);
        });


        //asignar valor a data-total-neto para enviarlo al backend
        document.querySelector('#total_neto').setAttribute('data-total-neto', totalNeto);
        document.querySelector('#total_bruto').setAttribute('data-total-bruto', totalBruto);    
        document.querySelector('#iva').textContent = formatCurrency(totalIva);
        document.querySelector('#total_bruto').textContent = formatCurrency(totalBruto);
        document.querySelector('#total_neto').textContent = formatCurrency(totalNeto);


    }

}


function formatCurrency(value) {
    // Convertimos el valor a número entero
    const integerValue = Math.floor(value);
    
    // Usamos toLocaleString con minimumFractionDigits: 0 para no mostrar decimales
    let formattedValue = integerValue.toLocaleString('es-ES', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0  // Esto asegura que no se muestren decimales
    });

    // Si el valor tiene 4 dígitos y no incluye un punto, lo añadimos manualmente
    if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
        formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
    }

    // Agregamos el símbolo de peso al principio
    return `$ ${formattedValue}`;
}