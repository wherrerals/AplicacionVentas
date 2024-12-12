class Producto {
    constructor(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, tipoEntrega, fechaEntrega) {
        this.productoCodigo = productoCodigo;
        this.nombre = nombre;
        this.imagen = imagen;
        this.precioVenta = precioVenta;
        this.stockTotal = stockTotal;
        this.precioLista = precioLista;
        this.precioDescuento = precioDescuento;
        this.precioSinDescuento = 0;
        this.totalProducto = precioVenta * cantidad;
        this.cantidad = cantidad;
        this.sucursal = sucursal;
        this.tipoEntrega = tipoEntrega;
        this.fechaEntrega = fechaEntrega;
    }

    async obtenerStock(codigoProducto) {
        try {
            const response = await fetch(`/ventas/obtener_stock_bodegas/?idProducto=${codigoProducto}`);
            if (!response.ok) {
                throw new Error("Error al obtener el stock");
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Error al obtener el stock:", error);
            return null;
        }
    }

    async actualizarStock(row) {
        const stockData = await this.obtenerStock(this.productoCodigo);
        if (stockData) {
            const bodegaMap = {
                "12": "GR",
                "13": "LC",
                "14": "PH",
                "15": "ME"
            };

            const stockTotal = stockData.reduce((total, bodega) => total + bodega.stock, 0);

            const stockTotalElem = row.querySelector('[name="stock_total"]');
            stockTotalElem.textContent = `Total: ${stockTotal}`;

            const selectBodega = row.querySelector('.form-select');
            const valueSeleccionado = selectBodega.value;
            const bodegaSeleccionada = bodegaMap[valueSeleccionado];
            const stockBodega = stockData.find(bodega => bodega.bodega === bodegaSeleccionada)?.stock || 0;

            const stockBodegaElem = row.querySelector('[name="stock_bodega"]');
            stockBodegaElem.textContent = `Stock: ${stockBodega}`;
        }
    }

    crearFila(contprod) {
        let newRow = document.createElement('tbody');
        newRow.className = 'product-row';
        newRow.innerHTML = `
            <tr>
                <td rowspan="2">
                    <div class="row">
                        <div class="col-6"><small>${contprod}) ${this.productoCodigo}</small></div>
                        <div class="col-6 text-center"><img src="${this.imagen}" width="50" height="50"></div>
                    </div>
                </td>
                <td rowspan="2">
                    <div class="row">
                        <select class="form-select">
                            <option value="12" ${this.sucursal === 'GR' ? 'selected' : ''}>GR</option>
                            <option value="13" ${this.sucursal === 'LC' ? 'selected' : ''}>LC</option>
                            <option value="14" ${this.sucursal === 'PH' ? 'selected' : ''}>PH</option>
                            <option value="15" ${this.sucursal === 'ME' ? 'selected' : ''}>ME</option>
                        </select>
                        <small name="stock_bodega">Stock: </small>
                        <small name="stock_total">Total: </small>
                    </div>
                </td>
                <td>
                    <div><small>Precio: ${this.precioVenta}</small></div>
                    <div><small>Antes: ${this.precioLista}</small></div>
                    <div><small>Descuento: ${this.precioDescuento}</small></div>
                </td>
                <td>
                    <input type="number" class="form-control" value="0" id="agg_descuento">
                </td>   
                <td>${this.precioSinDescuento}</td>
                <td>
                    <input type="number" class="form-control" value="${this.cantidad}">
                </td>
                <td><span>${this.totalProducto}</span></td>
            </tr>
            <tr>
                <td colspan="3">
                    <input type="text" class="form-control" placeholder="Comentario">
                </td>
                <td>
                    <a href="#" class="bi bi-trash" id="eliminarp"></a>
                </td>
            </tr>
            <tr>
                <td colspan="2"><span>${this.nombre}</span></td>
                <td colspan="2">
                    <select class="form-select" id="tipoEntrega">
                        <option value="1" ${this.tipoEntrega === 'Directa' ? 'selected' : ''}>Directa</option>
                        <option value="5" ${this.tipoEntrega === 'Despacho' ? 'selected' : ''}>Despacho</option>
                        <option value="2" ${this.tipoEntrega === 'Retiro' ? 'selected' : ''}>Retiro</option>
                    </select>
                </td>
                <td colspan="2">
                    <input type="date" class="form-control" value="${this.fechaEntrega}">
                </td>
            </tr>
        `;

        const stockTotalElem = newRow.querySelector('#stock_total');
        stockTotalElem.addEventListener('mouseover', async () => {
            const stockData = await this.obtenerStock(this.productoCodigo);
            if (stockData) {
                const tooltipContent = stockData.map(bodega => `${bodega.bodega}: ${bodega.stock}`).join('\n');
                stockTotalElem.title = `Stock en otras tiendas:\n${tooltipContent}`;
            }
        });

        this.limitarMaxDescuento(newRow);
        return newRow;
    }

    limitarMaxDescuento(row) {
        let descuentoMaxElem = row.querySelector('#descuento');
        let descuentoMax = parseFloat(descuentoMaxElem.textContent.replace('Max: ', ''));

        let inputDescuento = row.querySelector('#agg_descuento');
        inputDescuento.max = descuentoMax;

        inputDescuento.value = 0;
        inputDescuento.addEventListener('input', function () {
            let valor = parseFloat(inputDescuento.value);
            if (valor > descuentoMax) {
                inputDescuento.value = descuentoMax;
            }
            if (valor < 0) {
                inputDescuento.value = 0;
            }
        });
    }
}

function agregarProducto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad = 1, sucursal, tipoEntrega, fechaEntrega) {
    let contprod = document.querySelectorAll('#productos tbody').length + 1;

    let producto = new Producto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, tipoEntrega, fechaEntrega);
    let newRow = producto.crearFila(contprod);

    document.getElementById('productos').appendChild(newRow);

    newRow.querySelector('#eliminarp').addEventListener('click', function() {
        newRow.remove();
        const event = new CustomEvent('productoEliminado', { detail: { codigoProducto: productoCodigo } });
        document.dispatchEvent(event);
    });

    producto.actualizarStock(newRow);

    newRow.querySelector('.form-select').addEventListener('change', function () {
        producto.actualizarStock(newRow);
    });
}
