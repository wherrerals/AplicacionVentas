// productoBase.js
// Clase base compartida por productos.js (cotización) y productoODV.js (orden de venta).
// Debe cargarse DESPUÉS de productosUtils.js y ANTES de productos.js / productoODV.js.

class ProductoBase {
    constructor({
        docEntry_linea,
        linea_documento,
        productoCodigo,
        nombre,
        imagen,
        precioVenta,
        stockTotal,
        precioLista,
        precioDescuento,
        cantidad,
        sucursal,
        comentario,
        cuponDescuento,
        descuentoAplcado
    }) {
        this.docEntry_linea = docEntry_linea;
        this.linea_documento = linea_documento;
        this.productoCodigo = productoCodigo;
        this.nombre = nombre;
        this.imagen = imagen;
        this.precioVenta = precioVenta;
        this.stockTotal = stockTotal;
        this.precioLista = precioLista;
        this.precioDescuento = Math.round(precioDescuento);
        this.precioSinDescuento = 0;
        this.totalProducto = precioVenta * cantidad;
        this.cantidad = cantidad;
        this.sucursal = sucursal;
        this.comentario = comentario;
        this.cuponDescuento = cuponDescuento;
        this.descuentoAplcado = descuentoAplcado ?? 0;
    }

    async obtenerStock(codigoProducto) {
        return obtenerStockBodegas(codigoProducto);
    }

    async actualizarStock(row, actualizarStockTotal = true) {
        const stockData = await this.obtenerStock(this.productoCodigo);
        if (!stockData) return 0;

        const stockFiltrado = stockData.filter(b => b.bodega !== "LLLLL");
        const stockTotalBodegasValidas = stockData.filter(b => b.bodega !== "LLLLL" && BODEGA_MAP[b.bodega]);
        const stockTotal = stockTotalBodegasValidas.reduce((total, b) => total + b.stock_disponible, 0);
        const treeTypeItem = stockData.find(item => item.product_type === 'iSalesTree');

        if (actualizarStockTotal) {
            const stockTotalElem = row.querySelector('[name="stock_total"]');
            if (stockTotalElem) {
                const totalMostrar = treeTypeItem ? treeTypeItem.stock_total : stockTotal;
                stockTotalElem.textContent = `Total: ${totalMostrar}`;
                stockTotalElem.style.color = totalMostrar === 0 ? 'red' : 'black';
            }
        }

        // Cotización tiene #warning_container; ODV no.
        const warningIcon = row.querySelector('#warning_container');
        if (warningIcon) {
            warningIcon.hidden = stockTotal !== 0;
        }

        const selectBodega = row.querySelector('.form-select');
        const valueSeleccionado = selectBodega.value;
        const bodegaSeleccionada = BODEGA_MAP[valueSeleccionado];

        const stockBodega = stockFiltrado.find(b => b.bodega === bodegaSeleccionada)?.stock_disponible || 0;
        const stockBodegaElem = row.querySelector('[name="stock_bodega"]');
        stockBodegaElem.textContent = `Stock: ${stockBodega}`;
        stockBodegaElem.setAttribute('data-stock', stockBodega);

        const tr_bodega = `TR_${bodegaSeleccionada}`;
        const stockTRElem = row.querySelector('[name="stock_tr"]');
        const stockTR = stockFiltrado.find(b => b.bodega === tr_bodega)?.stock_transito || 0;
        stockTRElem.textContent = `TR: ${stockTR}`;

        const stockArriboElem = row.querySelector('[name="stock_arribo"]');
        const stockArribo = stockFiltrado.find(b => b.bodega === 'RECEP_CD')?.stock_arribo || 0;
        stockArriboElem.textContent = `Arribo: ${stockArribo}`;

        const stockComprometidoElem = row.querySelector('[name="stock_comprometido"]');
        const stockComprometido = stockFiltrado.find(b => b.bodega === bodegaSeleccionada)?.stock_comprometido || 0;
        stockComprometidoElem.textContent = `Comp: ${stockComprometido}`;

        // ODV usa options con id="LC", id="PH", etc. para data-stock por bodega.
        // En cotización las options no tienen id; el querySelector retorna null y no hace nada.
        for (const bodega of stockFiltrado) {
            const optionElement = selectBodega.querySelector(`option[id="${bodega.bodega}"]`);
            if (optionElement) {
                optionElement.setAttribute('data-stock', bodega.stock_disponible);
            }
        }

        return stockTotal;
    }

    alternarMaxDescuento(row) {
        const elemento = row.querySelector('#descuento');
        if (elemento.getAttribute('hidden') !== null) {
            elemento.removeAttribute('hidden');
        } else {
            elemento.setAttribute('hidden', '');
        }
    }

    limitarMaxDescuento(row) {
        const descuentoMaxElem = row.querySelector('#descuento');
        const descuentoMax = parseFloat(descuentoMaxElem.textContent.replace('Max: ', ''));

        const inputDescuento = row.querySelector('#agg_descuento');
        inputDescuento.max = descuentoMax;
        inputDescuento.value = this.descuentoAplcado;

        inputDescuento.addEventListener('input', function () {
            const valor = parseFloat(inputDescuento.value);
            if (valor > descuentoMax) {
                inputDescuento.value = descuentoMax;
            }
            if (valor < 0) {
                inputDescuento.value = 0;
            }
        });
    }
}

