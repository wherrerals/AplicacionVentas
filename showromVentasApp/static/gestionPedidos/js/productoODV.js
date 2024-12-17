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
    
            const selectBodega = row.querySelector('.form-select');
            const valueSeleccionado = selectBodega.value;
            const bodegaSeleccionada = bodegaMap[valueSeleccionado];
            const stockBodega = stockData.find(bodega => bodega.bodega === bodegaSeleccionada)?.stock || 0;
    
            // Actualizar el texto del stock de la bodega seleccionada
            const stockBodegaElem = row.querySelector('[name="stock_bodega"]');
            stockBodegaElem.textContent = `Stock: ${stockBodega}`;
    
            // Establecer el valor máximo del campo cantidad
            const cantidadInput = row.querySelector('#calcular_cantidad');
            cantidadInput.max = stockBodega;
    
            // Validar que el valor actual no exceda el stock
            if (parseInt(cantidadInput.value, 10) > stockBodega) {
                cantidadInput.value = stockBodega;
            }
        }
    }

    

    crearFila(contprod) {
        let newRow = document.createElement('tbody');
        newRow.className = 'product-row';
        newRow.innerHTML = `
            <tr>
                <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;"rowspan="2">
                    <div class="row">
                        <div class="col-md-11 col-xxl-6" style="font-size: 14px;font-weight: bold;"><small style="font-weight: bold;"><small>${contprod})</small><small>&nbsp;&nbsp;</small><small name="sku_producto">${this.productoCodigo}</small></div>
                        <div class="col-md-11 col-xxl-7" style="text-align: center;"><img src="${this.imagen}" width="50" height="50" style="width: 50px;height: 50px;"></div>
                    </div>
                </td>
                <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;"rowspan="2">
                    <div class="row">
                    <div class="col-sm-12 col-lg-12 col-xl-11 col-xxl-10">
                        <select class="form-select" style="font-size: 11px;">
                          <optgroup label="Bodega">
                            <option value="12" ${this.sucursal === 'GR' ? 'selected' : ''}>GR</option>
                            <option value="13" ${this.sucursal === 'LC' ? 'selected' : ''}>LC</option>
                            <option value="14" ${this.sucursal === 'PH' ? 'selected' : ''}>PH</option>
                            <option value="15" ${this.sucursal === 'ME' ? 'selected' : ''}>ME</option>
                            </optgroup>
                        </select>
                    </div>
                    <div class="col" style="text-align: center;">
                        <small style="font-size: 12px;" name="stock_bodega">Stock: </small>
                        <small name="stock_total" id="stock_total">Total: </small>
                    </div>
                    </div>
                </td>
                <td style="background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
                    <div style="font-size: 12px;"><small>Precio: ${this.precioVenta}</small></div>
                    <div style="font-size: 11px;"><small style="color: rgb(153,153,153);">Antes: ${this.precioLista}</small>
                    </div>
                    <div class="row" style="font-size: 11px;">
                    <div div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="mostrar-descuento" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
                    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z">
                    </path>
                    </svg></div>
                      <div class="col-sm-7 col-md-8"><small id="descuento" style="color: rgb(255,0,0);">Max: ${this.precioDescuento}</small></div>
                    </div>
                </td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <div><input class="form-control" type="number" style="font-size: 12px;width: 60px; value="0" id="agg_descuento">
                </td>   
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">${this.precioSinDescuento}</td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <input class="form-control" type="number" style="width: 65px;" id="calcular_cantidad" name="cantidad" min="1" max="1000" value="${this.cantidad}">
                </td>
                <td style="font-size: 11px;font-weight: bold;background: transparent;border-style: none;text-align: center;"><span>${this.totalProducto}</span></td>
            </tr>
            <tr  style="font-size: 12px;background: transparent;">
                <td  style="font-size: 11px;background: transparent;padding-top: 0px;border-style: none;padding-bottom: 0px;" colspan="3">
                    <input class="form-control" type="text" placeholder="Comentario" style="font-size: 12px;">
                </td>
                    <td style="background: transparent;padding-top: 8px;padding-left: 50px;border-style: none;padding-bottom: 0px;">
                        <a class="navbar-brand d-flex align-items-center bi bi-trash" href="#" style="width: 18px;"  id="eliminarp">
                            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-trash" style="width: 18px;height: 18px;">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z">
                                </path>
                                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z">
                                </path>
                            </svg>
                        </a>
                    </td>
            </tr>
            <tr style="font-size: 12px;background: transparent;">
                <td colspan="3" style="padding-top: 0px;background: transparent;">
                    <span>${this.nombre}</span>
                </td>
                <td style="font-size: 12px;background: transparent;" colspan="2">
                    <select class="form-select" id="tipoEntrega" style="font-size: 12px;">
                      <optgroup label="Entrega">
                        <option value="1" ${this.tipoEntrega === 'Directa' ? 'selected' : ''}>Directa</option>
                        <option value="5" ${this.tipoEntrega === 'Despacho' ? 'selected' : ''}>Despacho</option>
                        <option value="2" ${this.tipoEntrega === 'Retiro' ? 'selected' : ''}>Retiro</option>
                    </optgroup>
                    </select>
                </td>
                <td td colspan="2" style="background: transparent;">
                    <input class="form-control" type="date" name="fechaEntrega" style="width: 90%;font-size: 13px;" value="${this.fechaEntrega}">
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

      
    // Método para alternar la visibilidad del descuento
    alternarMaxDescuento(row) {
        let elemento = row.querySelector('#descuento');
        if (elemento.getAttribute('hidden') !== null) {
            elemento.removeAttribute('hidden');
        } else {
            elemento.setAttribute('hidden', '');
        }
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

    // Crear una instancia de valorTributario para este producto
    let valorTributarioProducto = new valorTributario(productoCodigo, precioVenta * cantidad);
    productos.push(valorTributarioProducto);

    console.log('Producto agregado:', valorTributarioProducto);

    // Agregar eventos
    newRow.querySelector('#eliminarp').addEventListener('click', function () {
        newRow.remove();
        const event = new CustomEvent('productoEliminado', { detail: { codigoProducto: productoCodigo } });
        document.dispatchEvent(event);
    });

    // Actualizar stock al cambiar bodega
    newRow.querySelector('.form-select').addEventListener('change', function () {
        producto.actualizarStock(newRow);
    });

    // Validar que la cantidad no supere el stock
    const cantidadInput = newRow.querySelector('input[type="number"]');
    cantidadInput.addEventListener('input', function () {
        const max = parseInt(cantidadInput.max, 10) || 0;
        if (parseInt(cantidadInput.value, 10) > max) {
            cantidadInput.value = max;
        }
        calcularPrecioTotal(); // Recalcular el precio total
    });

    const descuentoInput = newRow.querySelector('#agg_descuento');
    descuentoInput.addEventListener('input', aplicarDescuento);

    calcularPrecioTotal();

    // Función para calcular el precio total
    function calcularPrecioTotal() {
        const cantidad = parseFloat(cantidadInput.value) || 0;
        const precioUnitario = parseFloat(precioVenta) || 0;
        const precioTotal = cantidad * precioUnitario;
        const descuento = parseFloat(descuentoInput.value) || 0;

        // Calcular el precio con descuento
        const precioFinal = descuento === 0 ? precioTotal : precioTotal - (precioTotal * (descuento / 100));
        const precioConDescuento = descuento === 0 ? 0 : precioUnitario * (1 - (descuento / 100));

        // Actualizar la instancia de valorTributario
        valorTributarioProducto.modificarPrecioFinal(precioFinal);

        newRow.querySelector('#precio_Venta').textContent = precioFinal.toFixed(2);
        newRow.querySelector('#Precio_Descuento').textContent = precioConDescuento.toFixed(2);

        actualizarValores(); // Actualizar los valores totales
    }

    // Función para aplicar el descuento
    function aplicarDescuento() {
        calcularPrecioTotal();
    }

    // Escuchar el evento productoEliminado para actualizar los valores totales
    document.addEventListener('productoEliminado', function (event) {
        const codigoProducto = event.detail.codigoProducto;

        // Eliminar el producto del array de valorTributario
        const index = productos.findIndex(producto => producto.codigoProducto === codigoProducto);
        if (index > -1) {
            productos.splice(index, 1);
        }

        actualizarValores(); // Actualizar los valores totales
    });

    // Función para actualizar los valores de IVA, bruto y neto
    function actualizarValores() {
        let totalIva = 0;
        let totalBruto = 0;
        let totalNeto = 0;

        productos.forEach(producto => {
            const valores = producto.calcularValores();
            totalIva += parseFloat(valores.iva);
            totalBruto += parseFloat(valores.bruto);
            totalNeto += parseFloat(valores.neto);
        });

        console.log('Total IVA:', totalIva, 'Total Bruto:', totalBruto, 'Total Neto:', totalNeto);

        document.querySelector('#iva small').textContent = `$${totalIva.toFixed(0)}`;
        document.querySelector('#total_bruto small').textContent = `$${totalBruto.toFixed(0)}`;
        document.querySelector('#total_neto small').textContent = `$${totalNeto.toFixed(0)}`;
    }
}
