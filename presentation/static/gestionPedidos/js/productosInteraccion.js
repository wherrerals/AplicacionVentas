class valorTributario {
    constructor(codigoProducto, precioFinal, indiceProducto) {
        this.codigoProducto = codigoProducto;
        this.precioFinal = precioFinal; // total neto línea (sin IVA)
        this.indiceProducto = indiceProducto;
    }

    // Metodo para modificar el precio final (total neto línea)
    modificarPrecioFinal(precioFinal) {
        this.precioFinal = precioFinal;
    }

    // Metodo para devolver neto, bruto y IVA (pero bruto e IVA se recalculan a nivel documento)
    calcularValores() {
        var neto = this.precioFinal || 0;
        return {
            neto: neto
        };
    }
}

// Función de redondeo genérica
function roundTo(num, decimals) {
    const factor = Math.pow(10, decimals);
    return Math.round(num * factor) / factor;
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

        // 1 obtner el precio neto 
        const precioNeto  = precioUnitario / 1.19;

        // 2. Precio neto unitario con descuento (redondeado a 4 decimales)
        let precioConDescuento2 = roundTo(precioNeto * (1 - descuento / 100), 4);

        // 3. Total neto de la línea (sin redondear a pesos todavía)
        const precioFinal_n = roundTo(precioConDescuento2 * cantidad, 0);

        console.log('Precio Unitario:', precioUnitario, 'Precio neto:', precioNeto      , 'Precio con descuento redondeado:', precioConDescuento2, 'Precio final antes de IVA:', precioFinal_n, 'Precio final después de IVA:', precioFinal_n,);

        // Actualizar el producto en la lista
        producto.modificarPrecioFinal(precioFinal_n);

        tdPrecioVenta.textContent = formatCurrency(precioFinaldefinido);
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


    function redondeoCondicional(numero) {
        const parteDecimal = +(numero - Math.floor(numero)).toFixed(2);

        // Si la parte decimal es mayor o igual a 0.45 -> redondeamos hacia arriba
        if (parteDecimal >= 0.15) {
            return Math.ceil(numero);
        }

        // En caso contrario, redondeo normal al entero más cercano
        return Math.round(numero);
    }


    // Función para actualizar los valores de IVA, bruto y neto sumando todos los productos
    function actualizarValores() {
        let totalNeto = 0;
    
        productos.forEach(producto => {
            const valores = producto.calcularValores();
            //totalIva += valores.iva;
            totalNeto += valores.neto;

        });

        // Aquí recién redondeamos a pesos (entero)
        let totalBruto = roundTo(totalNeto * 1.19, 2);

        console.log('Total bruto antes de redondeo condicional:', totalBruto);
        
        // Regla de negocio: si los decimales >= 0.15, subimos al siguiente entero.
        // Ejemplo: 6899.15 -> 6900, 6899.14 -> 6899
        totalBruto = redondeoCondicional(totalBruto);

        let totalIva = totalBruto - totalNeto;


        console.log('totalIva:', totalIva, 'totalBruto:', totalBruto, 'totalNeto:', totalNeto);

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