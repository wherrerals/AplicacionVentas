class Producto {
    constructor(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, tipoEntrega, fechaEntrega = new Date().toISOString().split('T')[0]) {
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
            // Mapear las bodegas válidas (excluyendo GR)
            const bodegaMap = {
                "LC": "LC",
                "PH": "PH",
                "ME": "ME"
            };

            // Filtrar los datos de stock excluyendo la bodega "GR"
            const stockFiltrado = stockData.filter(bodega => bodega.bodega !== "GR");

            // Calcular el stock total sumando solo las bodegas válidas
            const stockTotal = stockFiltrado.reduce((total, bodega) => total + bodega.stock, 0);

            // Mostrar el stock total
            const stockTotalElem = row.querySelector('[name="stock_total"]');
            stockTotalElem.textContent = `Total: ${stockTotal}`;

            // Obtener el value de la bodega seleccionada
            const selectBodega = row.querySelector('.form-select');
            const valueSeleccionado = selectBodega.value;

            // Usar el mapa para obtener el código correspondiente
            const bodegaSeleccionada = bodegaMap[valueSeleccionado];

            // Encontrar el stock de la bodega seleccionada
            const stockBodega = stockFiltrado.find(bodega => bodega.bodega === bodegaSeleccionada)?.stock || 0;

            // Mostrar el stock de la bodega seleccionada
            const stockBodegaElem = row.querySelector('[name="stock_bodega"]');
            stockBodegaElem.textContent = `Stock: ${stockBodega}`;
        }
    }




    crearFila(contprod, valorTipoEntrega) {
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
                        <select class="form-select bodega-select" style="font-size: 11px;">
                          <optgroup label="Bodega">
                            <option value="LC" ${this.sucursal === 'LC' ? 'selected' : ''}>LC</option>
                            <option value="PH" ${this.sucursal === 'PH' ? 'selected' : ''}>PH</option>
                            <option value="ME" ${this.sucursal === 'ME' ? 'selected' : ''}>ME</option>
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
                    <div style="font-size: 12px;">
                        <small name="precio_venta" data-precio-unitario="100.00">${this.precioVenta}</small>
                    </div>
                    <div style="font-size: 11px;">
                        <small style="color: rgb(153,153,153); name="precio_lista">Antes: ${this.precioLista}</small>
                    </div>

                    <div class="row" style="font-size: 11px;">
                        <div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="mostrar-descuento" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
                                <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"></path>
                            </svg>
                        </div>
                        <div class="col-sm-7 col-md-8">
                            <small style="color: rgb(255,0,0);" id="descuento" name="descuento_max" hidden>Max: ${this.precioDescuento}</small>
                        </div>
                    </div>
                </td>

                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <div>
                        <input class="form-control" type="number" style="font-size: 12px;width: 60px;" id="agg_descuento" min="0" value="0">
                    </div>
                </td>
                   
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;" id="Precio_Descuento">${this.precioSinDescuento}</td>
                <td style="font-size: 12px;background: transparent;border-style: none;">    
                    <input class="form-control" type="number" style="width: 65px;" id="calcular_cantidad" name="cantidad" min="1" max="1000" value="${this.cantidad !== undefined ? this.cantidad : 0}">
                </td>
                <td style="font-size: 11px;font-weight: bold;background: transparent;border-style: none;text-align: center;">
                    <span id="precio_Venta">${this.totalProducto}</span>
                </td>
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
                            <option value="1" ${valorTipoEntrega === '1' ? 'selected' : ''}>Directa</option>
                            <option value="5" ${valorTipoEntrega === '5' ? 'selected' : ''}>Despacho</option>
                            <option value="2" ${['2', '3', '4'].includes(valorTipoEntrega) ? 'selected' : ''}>Retiro</option>
                        </optgroup>
                    </select>
                </td>
                <td td colspan="2" style="background: transparent;">
                    <input class="form-control" type="date" name="fechaEntrega" style="width: 90%;font-size: 13px;" value="${this.fechaEntrega}">
                </td>
            </tr>
        `;



        // Limpiar el contenido de inputNumero
        const inputNumero = document.getElementById('inputNumero');
        if (inputNumero) {
            inputNumero.value = ''; // Limpia el campo
            console.log("Campo 'inputNumero' limpiado.");
        }

        // Agregar evento mouseover para mostrar stock en otras tiendas
        const precioVentaElem = newRow.querySelector('#stock_total');
        precioVentaElem.addEventListener('mouseover', async () => {
            const stockData = await this.obtenerStock(this.productoCodigo);
            if (stockData) {
                // Filtrar las bodegas para excluir "GR"
                const stockFiltrado = stockData.filter(bodega => bodega.bodega !== "GR");

                // Crear el contenido del tooltip solo con las bodegas válidas
                const tooltipContent = stockFiltrado
                    .map(bodega => `${bodega.bodega}: ${bodega.stock}`)
                    .join('\n');

                // Asignar el contenido del tooltip
                precioVentaElem.title = `Stock en otras tiendas:\n${tooltipContent}`;
            }
        });


        this.limitarMaxDescuento(newRow);
        this.limitarCantidad(newRow);
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

    limitarCantidad(row) {

        // Obtener el elemento #numero_orden
        const numeroOrdenElem = document.getElementById('numero_orden');
        const docEntry = numeroOrdenElem?.getAttribute('data-docentry');

        // Verificar si hay un valor en data-docentry
        if (docEntry) {
            console.log("No se ejecuta limitarCantidad porque data-docentry tiene un valor:", numeroOrdenElem);
            return;
        }

        let cantidadInput = row.querySelector('#calcular_cantidad');
        let stockBodegaElem = row.querySelector('[name="stock_bodega"]'); // Referencia al elemento de stock



        // Función para validar y limitar la cantidad
        const validarCantidad = () => {
            let maxStock = parseInt(stockBodegaElem.textContent.replace('Stock: ', ''), 10) || 0;
            let cantidadActual = parseInt(cantidadInput.value, 10) || 0;

            if (cantidadActual > maxStock) {
                cantidadInput.value = maxStock;
            } else if (cantidadActual < 1) {
                cantidadInput.value = 0;
            }
        };

        // Agregar evento para validar en tiempo real
        cantidadInput.addEventListener('input', validarCantidad);
        cantidadInput.addEventListener('change', validarCantidad);

        // Si el stock cambia dinámicamente (llamado después de actualizar stock)
        const stockBodegaObserver = new MutationObserver(validarCantidad);
        stockBodegaObserver.observe(stockBodegaElem, { childList: true, subtree: true });
    }

}


function agregarProducto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad = 1, sucursal, tipoEntrega, fechaEntrega) {
    let contprod = document.querySelectorAll('#productos tbody').length + 1; // Contador de productos

    const tipoEntregaSeleccionado = document.getElementById('tipoEntrega-1')?.value || '1'; // Obtener el valor del tipo de entrega seleccionado

    // Crear instancia del producto
    const producto = new Producto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, tipoEntregaSeleccionado, fechaEntrega);
    const newRow = producto.crearFila(contprod, tipoEntregaSeleccionado); // Crear la fila del producto

    document.getElementById('productos').appendChild(newRow); // Agregar la fila al tbody


    newRow.querySelector('#mostrar-descuento').addEventListener('click', function () {
        producto.alternarMaxDescuento(newRow);
    });

    newRow.querySelector('#eliminarp').addEventListener('click', function () {
        newRow.remove();
        const event = new CustomEvent('productoEliminado', { detail: { codigoProducto: productoCodigo } });
        document.dispatchEvent(event);
    });


    // Validar que la cantidad no supere el stock
    const cantidadInput = newRow.querySelector('#calcular_cantidad');
    cantidadInput.addEventListener('input', function () {
        const max = parseInt(cantidadInput.max, 10) || 0;
        if (parseInt(cantidadInput.value, 10) > max) {
            cantidadInput.value = max;
        }
    });

    producto.actualizarStock(newRow);

    // Evento para actualizar el stock al cambiar de bodega
    newRow.querySelector('.form-select').addEventListener('change', function () {
        producto.actualizarStock(newRow);
    });
    const inputNumero = document.getElementById("inputNumero");

    // Llamar a la función agregarInteractividad si es necesario
    agregarInteractividad(newRow, productoCodigo);

}
