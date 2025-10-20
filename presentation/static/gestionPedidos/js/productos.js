class Producto {
    constructor(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, cuponDescuento, descuentoAplcado) {
        
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
        this.descuentoAplcado = descuentoAplcado ?? 0;
        this.cuponDescuento = cuponDescuento

    }
    

    async obtenerStock(codigoProducto) {
        try {
            const response = await fetch(`/ventas/obtener_stock_bodegas/?idProducto=${codigoProducto}`);
            if (!response.ok) {
                throw new Error("Error al obtener el stock");
            }
            const data = await response.json();
            //console.log("info bodegas:", data)
            return data; // Lista de objetos con bodega y stock
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
                "ME": "ME",
                "VI": "VI"
            };

            // Filtrar los datos de stock excluyendo la bodega "GR"
            const stockFiltrado = stockData.filter(bodega => bodega.bodega !== "GR");

            // Calcular el stock total sumando solo las bodegas válidas
            const stockTotal = stockFiltrado.reduce((total, bodega) => total + bodega.stock, 0);

            // Mostrar el stock total
            const stockTotalElem = row.querySelector('[name="stock_total"]');
            stockTotalElem.textContent = `Total: ${stockTotal}`;
            stockTotalElem.style.color = stockTotal === 0 ? 'red' : 'black';

            let warningIcon = row.querySelector('#warning_container');
            console.log("capturado el warning icon:", warningIcon);

            if (stockTotal === 0) {
                console.log("No hay stock disponible para el producto:", this.productoCodigo);
                warningIcon.hidden = false;
            } else {
                console.log("Hay stock disponible para el producto:", this.productoCodigo);
                warningIcon.hidden = true;
            }

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

    // Método para crear una fila en la tabla de productos
    crearFila(contprod) {
        let newRow = document.createElement('tbody');
        newRow.className = 'product-row';
        newRow.setAttribute('id', contprod);
        newRow.setAttribute('data-docentryLinea', this.docEntry_linea);
        newRow.setAttribute('data-itemcode', this.productoCodigo);

        // Verificar si el valor de docEntry_linea es "null"
        if (this.docEntry_linea === "null") {
            newRow.style.backgroundColor = '#F0F2F5'; // Color gris claro cuando es "null"
        }

        newRow.innerHTML = `
        <tr>
            <tr>
                <td style="font-size: 12px; background: transparent; border-style: none; padding-bottom: 0px;" rowspan="2">
                    <div class="row">
                        <div class="col-md-11 col-xxl-6" style="font-size: 14px; font-weight: bold;">
                        <small id="indixe_producto" data-lineNum="${this?.linea_documento}" data-indice="${contprod}">${contprod})</small><small>&nbsp;&nbsp;</small><small style="font-weight-bold" name="sku_producto">${this.productoCodigo}</small>
                        </div>
                        <div class="col-md-11 col-xxl-7" style="text-align: center;">
                            <img src="${this.imagen}" style="width: 80px;height: 80px;" name="img_producto" id="img_productox">
                        </div>
                    </div>
                </td>
                <td style="font-size: 12px; background: transparent; border-style: none; padding-bottom: 0px;" rowspan="2">
                    <div class="row">
                        <div class="col-sm-12 col-lg-12 col-xl-11 col-xxl-10">
                          <select class="form-select bodega-select" style="font-size: 11px;>
                            <optgroup label="Bodega">
                            <option value="LC" ${this.sucursal === 'LC' ? 'selected' : ''}>LC</option>
                            <option value="PH" ${this.sucursal === 'PH' ? 'selected' : ''}>PH</option>
                            <option value="ME" ${this.sucursal === 'ME' ? 'selected' : ''}>ME</option>
                            <option value="VI" ${this.sucursal === 'VI' ? 'selected' : ''}>VI</option>
                            </optgroup>
                          </select>
                        </div>
                        <div class="col" style="text-align: center;">
                            <small style="font-size: 12px;" name="stock_bodega">Stock:  </small>
                            <small style="font-size: 12px;" id="stock_total" name="stock_total">Total: </small>
                            <div id="warning_container" style="display: inline-block;" hidden>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle" viewBox="0 0 16 16" style="color: rgba(255, 7, 7, 1);margin-left: 5px;" name="warning_icon">
                                <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/>
                                <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
                            </svg>
                            </div>
                        </div>
                    </div>
                </td>
                <td style="background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
                    <div style="font-size: 12px;">
                        <small class="numeric-value" name="precio_venta" data-precio-unitario="100.00" data-precioUnitario="${this.precioVenta}">${formatCurrency(this.precioVenta)}</small>
                    </div>
                    <div style="font-size: 11px;">
                        <small class="numeric-value" style="color: rgb(153,153,153);" name="precio_lista">${formatCurrency(this.precioLista)}</small>
                    </div>

                    <div class="row" style="font-size: 11px;">
                        <div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="mostrar-descuento" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
                                <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"></path>
                            </svg>
                        </div>
                        <div class="col-sm-7 col-md-8">
                            <small  class="numeric-value" style="color: rgb(255,0,0);" id="descuento" name="descuento_max" hidden>Max: ${this.precioDescuento}%</small>
                        </div>
                    </div>
                </td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <div>
                        <input class="form-control format-number" type="number" style="font-size: 12px;width: 60px;" id="agg_descuento" min="0" value="${this.descuentoAplcado ?? 0}" onclick="this.select()">
                        <strong style="font-size: 9;width: 100px; color: red" id="desc_cupon" ${this.cuponDescuento ? '' : 'hidden'}>Cupon: ${this.cuponDescuento ?? 0}%</strong>
                    </div>
                </td>
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;" id="Precio_Descuento">${formatCurrency(this.precioSinDescuento)}</td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <input class="form-control format-number" type="number" style="font-size: 12px;width: 80px;"  id="calcular_cantidad" name="cantidad" min="1" max="1000" value="${this.cantidad}" onclick="this.select()">
                </td>
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">
                    <span id="precio_Venta" data-totalProductValue="${this.totalProducto}">${formatCurrency(this.totalProducto)}</span>
                </td>
            </tr> 
            <tr style="font-size: 12px;background: transparent;">
                <td style="font-size: 11px;background: transparent;padding-top: 0px;border-style: none;padding-bottom: 0px;"colspan="3">
                    <input class="form-control" type="text" placeholder="Comentario" id="comentarios-1" style="font-size: 12px;" value="${this.comentario ?? ''}"></input>
                </td>
                <td style="background: transparent;padding-top: 8px;padding-left: 50px;border-style: none;padding-bottom: 0px;">
                    <a class="navbar-brand d-flex align-items-center" href="#" style="width: 18px;">
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="eliminarp" class="bi bi-trash" style="width: 18px;height: 18px;">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"> </path>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"> </path>
                      </svg>
                    </a>
                </td>
            <tr style="font-size: 12px;background: transparent;">
                <td colspan="7" style="padding-top: 0px;background: transparent;"><span name="nombre_producto">${this.nombre}</span></td>
            </tr>
            </tr>
        `;

        function formatCurrency(value) {
            // Convertimos el valor a número entero
            const integerValue = value;
            let formattedValue = integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
        
            // Si el valor tiene 4 dígitos y no incluye un punto, lo añadimos manualmente
            if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
                formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
            }
        
            // Agregamos el símbolo de peso al principio
            return `$ ${formattedValue}`;
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
        // Obtener el valor del descuento máximo
        let descuentoMaxElem = row.querySelector('#descuento');
        let descuentoMax = parseFloat(descuentoMaxElem.textContent.replace('Max: ', ''));
    
        // Configurar el input para limitar el valor máximo
        let inputDescuento = row.querySelector('#agg_descuento');
        inputDescuento.max = descuentoMax;
    
        // Establecer el valor inicial del descuento aplicado en el input
        inputDescuento.value = this.descuentoAplcado;  // Cambié de 0 a this.descuentoAplcado
    
        // Validar el valor actual del input
        inputDescuento.addEventListener('input', function () {
            let valor = parseFloat(inputDescuento.value);
    
            // Si el valor es mayor que el descuento máximo, ajustarlo
            if (valor > descuentoMax) {
                inputDescuento.value = descuentoMax;
            }
    
            // Si el valor es menor que 0, ajustarlo a 0
            if (valor < 0) {
                inputDescuento.value = 0;
            }
        });
    }
    
}

// Función global para manejar la adición de productos
function agregarProducto(docEntry_linea,linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad = 1, sucursal, comentario, cuponDescuento, descuentoAplcado) {
    // Contador de productos
    console.log("cantidad: ", cantidad);
    console.log("sucursal: ", sucursal);

    let contprod = document.querySelectorAll('#productos tbody').length + 1;

    // Crear una instancia de Producto
    let producto = new Producto(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, cuponDescuento, descuentoAplcado);
    
    let newRow = producto.crearFila(contprod);

    document.getElementById('productos').appendChild(newRow);


    console.log("Producto creado xxx:", producto);
    console.log("Producto creado:", producto.cuponDescuento, producto.precioDescuento);


    // ---- APLICAR UI DEL CUPÓN ANTES de inicializar interactividad ----
    if (producto.cuponDescuento && Number(producto.cuponDescuento) > 0) {
        const descuentoCupon = Number(producto.cuponDescuento);

        const inputDescuentoRow = newRow.querySelector('#agg_descuento');
        if (inputDescuentoRow) {
            inputDescuentoRow.max = descuentoCupon;
            inputDescuentoRow.value = 0;
            inputDescuentoRow.setAttribute('disabled', 'disabled');
        }

        const descElem = newRow.querySelector('#desc_cupon');
        if (descElem) {
            descElem.textContent = `Cupon: ${descuentoCupon}%`;
            descElem.hidden = false;
            descElem.dataset.value = descuentoCupon; // <- importante para calcular correctamente
        }
    }


    const indiceProducto = newRow.querySelector('#indixe_producto').getAttribute('data-indice'); 


    // Agregar eventos
    newRow.querySelector('#mostrar-descuento').addEventListener('click', function () {
        producto.alternarMaxDescuento(newRow);
    });

    newRow.querySelector('#eliminarp').addEventListener('click', function () {
        // Obtener el índice del producto dentro de la tabla
        const indiceProducto = newRow.querySelector('#indixe_producto').getAttribute('data-indice'); 
    
        // Eliminar la fila del DOM
        newRow.remove();
    
        // Emitir el evento con código del producto e índice
        const event = new CustomEvent('productoEliminado', {
            detail: { 
                codigoProducto: productoCodigo,
                indiceProducto: indiceProducto // Pasar el índice específico
            }
        });
    
        console.log('Evento emitido:', event);
        document.dispatchEvent(event);
    
        // Actualizar los índices de los productos visibles
        actualizarIndicesProductos();

        document.getElementById('inputNumero').focus();
    });
    
    function actualizarIndicesProductos() {
        // Seleccionar todas las filas de los productos
        const filasProductos = document.querySelectorAll('.product-row'); // Asegúrate de que las filas tengan esta clase
        filasProductos.forEach((fila, index) => {
            // Buscar el elemento que muestra el índice y actualizarlo
            const indiceElemento = fila.querySelector('#indixe_producto'); // Ajusta el selector si es necesario
            if (indiceElemento) {
                indiceElemento.textContent = `${index + 1})`; // Actualiza el índice visible
            }
        });
    }    

    producto.actualizarStock(newRow);

    // Evento para actualizar el stock al cambiar de bodega
    newRow.querySelector('.form-select').addEventListener('change', function () {
        producto.actualizarStock(newRow);
    });

    // Llamar a la función agregarInteractividad si es necesario
    agregarInteractividad(newRow, productoCodigo, indiceProducto);
}