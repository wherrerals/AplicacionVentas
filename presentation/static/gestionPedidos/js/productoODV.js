class Producto extends ProductoBase {
    constructor(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, cuponDescuento, descuentoAplcado, tipoentrega2, cantidadCoti, precioCoti, fechaEntrega = new Date().toISOString().split('T')[0]) {
        super({
            docEntry_linea, linea_documento, productoCodigo, nombre, imagen,
            precioVenta, stockTotal, precioLista, precioDescuento, cantidad,
            sucursal, comentario, cuponDescuento, descuentoAplcado
        });
        this.cantidadCoti = cantidadCoti;
        this.precioCoti = precioCoti;
        this.tipoEntrega2 = tipoentrega2;
        this.fechaEntrega = fechaEntrega;
    }

    crearFila(contprod) {
        let newRow = document.createElement('tbody');
        newRow.className = 'product-row';
        //aggregar id a la fila
        newRow.setAttribute('id', contprod);
        newRow.setAttribute('data-docentryLinea', this.docEntry_linea);
        newRow.setAttribute('data-itemcode', this.productoCodigo);

        // Verificar si el valor de docEntry_linea es "null"
        if (this.docEntry_linea === "null") {
            newRow.style.backgroundColor = '#F0F2F5'; // Color gris claro cuando es "null"
        }

        newRow.innerHTML = `
            <tr>
                <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;"rowspan="2">
                    <div class="row">
                        <div class="col-md-11 col-xxl-6" style="font-size: 14px;font-weight: bold;"><small style="font-weight: bold;">
                        <small id="indixe_producto" data-lineNum="${this?.linea_documento}">${contprod})</small><small>&nbsp;&nbsp;</small><small name="sku_producto">${this.productoCodigo}</small></div>
                        <div class="col-md-11 col-xxl-7" style="text-align: center;"><img src="${this.imagen}" style="width: 80px;height: 80px;" name="img_producto" id="img_productox"></div>
                    </div>
                </td>
                <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;"rowspan="2">
                    <div class="row">
                    <div class="col-sm-12 col-lg-12 col-xl-11 col-xxl-10">
                        <select class="form-select bodega-select" style="font-size: 11px;">
                          <optgroup label="Bodega">
                            <option id="LC" data-stock="" value="LC" ${this.sucursal === 'LC' ? 'selected' : '' } data-cantidadInicialSAP="${this.sucursal === 'LC' && this.cantidad !== undefined ? this.cantidad : 0}">Las Condes (LC)</option>
                            <option id="ME" data-stock="" value="ME" ${this.sucursal === 'ME' ? 'selected' : ''} data-cantidadInicialSAP="${this.sucursal === 'ME' && this.cantidad !== undefined ? this.cantidad : 0}">Panal (ME)</option>
                            <option id="PH" data-stock="" value="PH" ${this.sucursal === 'PH' ? 'selected' : ''} data-cantidadInicialSAP="${this.sucursal === 'PH' && this.cantidad !== undefined ? this.cantidad : 0}">Vitacura (PH)</option>
                            <option id="VI" data-stock="" value="VI" ${this.sucursal === 'VI' ? 'selected' : ''} data-cantidadInicialSAP="${this.sucursal === 'VI' && this.cantidad !== undefined ? this.cantidad : 0}">Viña del Mar (VI)</option>
                            <option id="GR" data-stock="" value="GR" ${this.sucursal === 'GR' ? 'selected' : ''} data-cantidadInicialSAP="${this.sucursal === 'GR' && this.cantidad !== undefined ? this.cantidad : 0}">Ñuñoa (GR)</option>
                            </optgroup>
                        </select>
                    </div>
                    <div class="col" style="text-align: left;">
                        <small style="font-size: 12px;" name="stock_bodega" id="stock_bodega">Stock: </small>
                        <small name="stock_total" id="stock_total">Total: </small>
                    </div>
                    </div>
                    <div class="col" style="text-align: left;">
                        <small style="font-size: 12px;" name="stock_tr">TR:  </small>
                        <small style="font-size: 12px;" name="stock_arribo">Arribo:  </small>
                        <small style="font-size: 12px;" id="stock_comprometido" name="stock_comprometido">Comp: </small>
                    </div>
                </td>
                
                <td style="background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
                    <div style="font-size: 12px;">
                        <small name="precio_venta" data-precio-unitario="100.00" data-precioUnitario="${this.precioVenta}">${formatCurrency(this.precioVenta)}</small>
                    </div>
                    <div style="font-size: 11px;">
                        <small style="color: rgb(153,153,153); name="precio_lista">Antes: ${formatCurrency(this.precioLista)}</small>
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
                        <input class="form-control format-number" type="number" style="font-size: 12px;width: 60px;" id="agg_descuento" min="0" value="${this.descuentoAplcado ?? 0}" onclick="this.select()">
                        <strong style="font-size: 9;width: 100px; color: red" id="desc_cupon" ${this.cuponDescuento ? '' : 'hidden'}>Cupon: ${this.cuponDescuento ?? 0}%</strong>
                    </div>
                </td>     
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;" id="Precio_Descuento">${this.precioSinDescuento}</td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <div>
                        <input class="form-control" type="number" style="font-size: 12px;width: 80px;" id="calcular_cantidad" name="cantidad" min="1" max="1000" value="${this.cantidad !== undefined ? this.cantidad : 0}" onclick="this.select()">
                    </div>
                    <div class="valorCotizacion" data-itemcode=${this.productoCodigo} hidden>
                        <b><small style="color: rgb(255,0,0);" id="valorCotizacion">Cotiz: ${this.cantidadCoti}</small></b>
                    </div>
                </td>
                <td style="font-size: 11px;font-weight: bold;background: transparent;border-style: none;text-align: center;">
                    <span id="precio_Venta">${this.totalProducto}</span>
                    <div class="valorCotizacion" data-itemcode=${this.productoCodigo} style="font-size: 11px;" hidden>
                    <span style="color: #FF0000;"><b>${formatCurrency(this.precioCoti)}</b></span>
                    </div>
                </td>
            </tr>
            <tr  style="font-size: 12px;background: transparent;">
                <td  style="font-size: 11px;background: transparent;padding-top: 0px;border-style: none;padding-bottom: 0px;" colspan="3">
                    <input class="form-control" type="text" placeholder="Comentario" id="comentarios-1" style="font-size: 12px;"  value="${this.comentario ?? ''}">
                </td>
                    <td style="background: transparent;padding-top: 8px;padding-left: 50px;border-style: none;padding-bottom: 0px;">
                        <a class="navbar-brand d-flex align-items-center bi bi-trash" href="#" style="width: 18px;"  id="eliminarp">

                        </a>
                    </td>
            </tr>
            <tr style="font-size: 12px;background: transparent;">
                <td colspan="3" style="padding-top: 0px;background: transparent;">
                    <div class="d-flex align-items-center gap-1">

                        <button 
                            class="btn btn-link btn-sm p-0 d-flex align-items-center justify-content-center text-danger"
                            style="width: 22px; height: 22px;"
                            onclick="generarFichaTecnica('${this.productoCodigo}')"
                            type="button"
                            title="Descargar ficha técnica PDF"
                        >
                            <i class="bi bi-file-earmark-pdf-fill" style="font-size: 16px;"></i>
                        </button>

                        <span name="nombre_producto" style="font-size: 12px; flex-grow: 1;">
                            ${this.nombre}
                        </span>



                    </div>
                </td>
                <td style="font-size: 12px;background: transparent;" colspan="2">
                    <select class="form-select" id="tipoEntrega" style="font-size: 12px;">
                        <optgroup label="Entrega">
                            <option value="1" ${this.tipoEntrega2 == 1 ? 'selected' : ''}>Directa</option>
                            <option value="5" ${this.tipoEntrega2 == 5 ? 'selected' : ''}>Despacho</option>
                            <option value="2" ${this.tipoEntrega2 == 2 ? 'selected' : ''}>Retiro Panal</option>
                            <option value="3" ${this.tipoEntrega2 == 3 ? 'selected' : ''}>Retiro LC</option>
                            <option value="4" ${this.tipoEntrega2 == 4 ? 'selected' : ''}>Retiro PH</option>
                        </optgroup>
                    </select>
                </td>
                <td colspan="2" style="background: transparent;">
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <input class="form-control" 
                            type="date" 
                            name="fechaEntrega" 
                            id="fecha_entrega_lineas" 
                            style="width: 100%; font-size: 13px; flex-grow: 1;" 
                            value="${this.fechaEntrega}">
                        
                        <span id="drag-handle" 
                            title="Arrastrar para reordenar" 
                            style="cursor: grab; color: #888; user-select: none; padding: 4px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M7 2a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                            </svg>
                        </span>
                    </div>
                </td>
            </tr>
        `;

        // Limpiar el contenido de inputNumero
        const inputNumero = document.getElementById('inputNumero');
        if (inputNumero) {
            inputNumero.value = '';
        }

        agregarTooltipStockBodegas(newRow, this.productoCodigo);

        this.limitarMaxDescuento(newRow);
        this.limitarCantidad(newRow);
        inicializarDragAndDrop(newRow);

        return newRow;
    }

    botonesCantidad(row) {
        let cantidadInput = row.querySelector('#calcular_cantidad');
    
        // Crear botones personalizados para incrementar y decrementar
        const incrementButton = document.createElement('button');
        incrementButton.textContent = '+';
        incrementButton.name = 'cantidad';
        incrementButton.className = 'agg_cantidad';
        incrementButton.style.cursor = 'pointer';
    
        const decrementButton = document.createElement('button');
        decrementButton.textContent = '-';
        decrementButton.name = 'cantidad';
        decrementButton.className = 'agg_cantidad';
        decrementButton.style.cursor = 'pointer';
    
        // Insertar los botones junto al input
        cantidadInput.insertAdjacentElement('afterend', incrementButton); 
        cantidadInput.insertAdjacentElement('afterend', decrementButton);
    
        // Retornar los botones para usarlos en otros métodos
        return { incrementButton, decrementButton };
    }




    
    limitarCantidad(row) {
        // Obtener el elemento #numero_orden
        const numeroOrdenElem = row.closest('.product-row') || row.querySelector('.product-row');

        if (!numeroOrdenElem) {
            console.error("Error: No se encontró el elemento con la clase .product-row en:", row);
        }

        const docEntry = numeroOrdenElem?.getAttribute('data-docentryLinea');


        // Referencias a elementos DOM
        const cantidadInput = row.querySelector('#calcular_cantidad');
        const stockBodegaElem = row.querySelector('[name="stock_bodega"]');

        const stockTotalElem = row.querySelector('[name="stock_total"]') || { textContent: '0' };
        const skuElem = row.querySelector('[name="sku_producto"]');
        
        // Si el producto comienza con "SV", no limitamos la cantidad
        if (skuElem && skuElem.textContent.startsWith('SV') || skuElem.textContent.startsWith('L') ) {
            return;
        }
    
        // Banderas y estado inicial
        let isUpdating = false;
        let lastValidatedQuantity = parseInt(cantidadInput.value || '0', 10);
        
        // Almacenar la cantidad inicial cuando carga el documento
        if (!cantidadInput.hasAttribute('data-initial-value') && docEntry) {
            cantidadInput.setAttribute('data-initial-value', cantidadInput.value || '0');
        }
        
        const cantidadInputs = row.querySelectorAll('#calcular_cantidad');
        cantidadInputs.forEach(cantidadInput => {
            cantidadInput.style.appearance = 'none';
            cantidadInput.style.MozAppearance = 'textfield'; // Firefox
        });
        
        
        
        // Crear los botones de incremento y decremento
        const { incrementButton, decrementButton } = this.botonesCantidad(row);
        
        const calcularCantidadMaxima = (valores) => {
            if (docEntry !== 'null') {
                return valores.cantidadInicial + valores.stockBodega2;
            } else {
                return valores.stockBodega2;
            }
        };

        // Evento para cuando cambia la selección de bodega
        const bodegaSelect = row.querySelector('.form-select.bodega-select');
        bodegaSelect.addEventListener('change', () => {
            // Obtener la opción seleccionada
            const opcionSeleccionada = bodegaSelect.options[bodegaSelect.selectedIndex];
            
            // Obtener el valor de stock de la opción seleccionada
            const stockBodegaSeleccionada = parseInt(opcionSeleccionada.getAttribute('data-stock') || '0', 10);
            
            // Obtener la cantidad inicial de la opción seleccionada
            const cantidadInicialSAP = parseInt(opcionSeleccionada.getAttribute('data-cantidadInicialSAP') || '0', 10);

            // Actualizar el texto y el atributo data-stock del elemento stockBodegaElem
            stockBodegaElem.textContent = `Stock: ${stockBodegaSeleccionada}`;
            stockBodegaElem.setAttribute('data-stock', stockBodegaSeleccionada);

            // Validar la cantidad actual contra el nuevo stock si es necesario
            const valores = obtenerValores();
            const cantidadMaxima = calcularCantidadMaxima(valores);

            if (valores.cantidadActual > cantidadMaxima) {
                cantidadInput.value = cantidadMaxima;
                lastValidatedQuantity = cantidadMaxima;
            }
        });

    const obtenerValores = () => {
        // Obtener el select de bodega
        const bodegaSelect = row.querySelector('.form-select.bodega-select');
        // Obtener la opción seleccionada
        const opcionSeleccionada = bodegaSelect.options[bodegaSelect.selectedIndex];
        // Obtener el valor de data-cantidadInicialSAP de la opción seleccionada
        const cantidadInicialSAP = parseInt(opcionSeleccionada.getAttribute('data-cantidadInicialSAP') || '0', 10);
        // Obtener el valor de data-stock de la opción seleccionada
        const stockBodegaSeleccionada = parseInt(opcionSeleccionada.getAttribute('data-stock') || '0', 10);

        return {
            stockBodega2: stockBodegaSeleccionada, // Ahora viene directamente de la opción seleccionada
            nombreBodega: opcionSeleccionada.value,
            cantidadActual: parseInt(cantidadInput.value || '0', 10),
            cantidadInicial: cantidadInicialSAP, // Usamos cantidadInicialSAP en lugar de cantidad inicial de input
            stockBodegaTexto: parseInt(stockBodegaElem.textContent.replace('Stock: ', '') || '0', 10),
            stockTotalTexto: parseInt(stockTotalElem.textContent.replace('Total: ', '') || '0', 10)
        };
    };
        
        // Función centralizada para cambiar la cantidad
        const cambiarCantidad = (nuevaCantidad) => {
            if (isUpdating) return;
            isUpdating = true;
            
            try {
                const valores = obtenerValores();
                const cantidadAnterior = lastValidatedQuantity; // Usar el último valor validado
                
                // Determinar la cantidad máxima permitida
                const cantidadMaxima = calcularCantidadMaxima(valores);
                
                // Validar y aplicar la nueva cantidad (asegurarse de que sea un número)
                let cantidadNumerica = parseInt(nuevaCantidad, 10);
                if (isNaN(cantidadNumerica)) cantidadNumerica = 0;
                
            
                let cantidadValidada;

                if (valores.stockBodega2 == 0){
                    cantidadValidada = Math.max(0, Math.min(cantidadNumerica, cantidadMaxima));
                } else {
                    cantidadValidada = Math.max(1, Math.min(cantidadNumerica, cantidadMaxima));
                }
                
                // Forzar el valor validado en el input (garantiza que siempre está dentro de límites)
                cantidadInput.value = cantidadValidada;
                
                // Calcular la diferencia entre la cantidad anterior y la nueva
                let diferencia = cantidadValidada - cantidadAnterior;
                
                // Solo continuar si hay un cambio real
                if (diferencia !== 0) {
                    // Actualizar stockBodega
                    
                let stockBodegaActualizado;
                    if (docEntry !== 'null') {
                        stockBodegaActualizado = valores.stockBodega2 - (cantidadValidada - valores.cantidadInicial);
                    } else {
                        stockBodegaActualizado = valores.stockBodega2 - cantidadValidada;
                    }
                    
                    // Desconectar observers temporalmente
                    const stockObserver = stockBodegaElem._observer;
                    if (stockObserver) stockObserver.disconnect();
                    
                    // Actualizar stockBodega
                    //stockBodegaElem.textContent = `Stock: ${Math.max(0, stockBodegaActualizado)}`;
                    
                    // Actualizar stockTotal
                    if (stockTotalElem && stockTotalElem.textContent) {
                        // Calcular stock total basado en la diferencia exacta
                        const stockTotalActualizado = valores.stockTotalTexto - diferencia;
                        //stockTotalElem.textContent = `Total: ${Math.max(0, stockTotalActualizado)}`;
                    }
                    
                    // Reconectar observers
                    if (stockObserver) {
                        stockObserver.observe(stockBodegaElem, { 
                            childList: true, 
                            subtree: true, 
                            attributes: true, 
                            attributeFilter: ['data-stock'] 
                        });
                    }
                    
                    // Disparar evento de input para notificar a otros componentes
                    cantidadInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                
                // Registrar la nueva cantidad validada incluso si no hubo cambio
                lastValidatedQuantity = cantidadValidada;
                
                // Habilitar/deshabilitar botones según límites
                incrementButton.disabled = cantidadValidada >= cantidadMaxima;
                incrementButton.style.opacity = incrementButton.disabled ? '0.5' : '1';
                
                decrementButton.disabled = cantidadValidada <= 0;
                decrementButton.style.opacity = decrementButton.disabled ? '0.5' : '1';
            } finally {
                isUpdating = false;
            }
        };
    
        // Implementar restricciones directas en el input
        cantidadInput.addEventListener('keydown', (event) => {
            // Permitir: backspace, delete, tab, escape, enter, puntos, comas y números
            if (
                event.key === 'Backspace' || 
                event.key === 'Delete' || 
                event.key === 'Tab' || 
                event.key === 'Escape' || 
                event.key === 'Enter' || 
                event.key === '.' || 
                event.key === ',' || 
                (event.key >= '0' && event.key <= '9')
            ) {
                // Permitir estas teclas
                return;
            }
            
            // Permitir: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X, flechas
            if (
                (event.ctrlKey && (event.key === 'a' || event.key === 'c' || event.key === 'v' || event.key === 'x')) || 
                event.key === 'ArrowLeft' || 
                event.key === 'ArrowRight'
            ) {
                // Permitir estas combinaciones
                return;
            }
            
            // Bloquear otras teclas
            event.preventDefault();
        });
    
        // Manejador para incremento con lógica explícita
        incrementButton.addEventListener('click', () => {
            const valores = obtenerValores();
            // Incrementar en 1 de forma explícita
            cambiarCantidad(valores.cantidadActual + 1);
        });
        
        // Manejador para decremento con lógica explícita
        decrementButton.addEventListener('click', () => {
            const valores = obtenerValores();
            // Decrementar en 1 de forma explícita
            cambiarCantidad(valores.cantidadActual - 1);
        });
        
        // Validar el input después de cambios directos
        cantidadInput.addEventListener('input', () => {
            if (!isUpdating) {
                const valores = obtenerValores();
                
                // Forzar validación inmediata para entrada directa
                cambiarCantidad(valores.cantidadActual);
            }
        });
        
        // Validación adicional al perder el foco
        cantidadInput.addEventListener('blur', () => {
            if (!isUpdating) {
                const valores = obtenerValores();
                const cantidadMaxima = calcularCantidadMaxima(valores);
                
                // Asegurar que el valor esté dentro de los límites al perder el foco
                if (valores.cantidadActual > cantidadMaxima) {
                    cambiarCantidad(cantidadMaxima);
                } else if (valores.cantidadActual < 0) {
                    cambiarCantidad(0);
                }
            }
        });
        
        // Manejar cambios en el stock de la bodega
        const manejarCambioBodega = () => {
            if (!isUpdating) {
                const valores = obtenerValores();
                const cantidadMaxima = calcularCantidadMaxima(valores);
                
                // Si la cantidad actual excede el nuevo máximo, ajustarla
                if (valores.cantidadActual > cantidadMaxima) {
                    cambiarCantidad(cantidadMaxima);
                } else {
                    // De lo contrario, actualizar visualización
                    cambiarCantidad(valores.cantidadActual);
                }
            }
        };
        
        // Observador para cambios en el stock
        const stockBodegaObserver = new MutationObserver(manejarCambioBodega);
        stockBodegaElem._observer = stockBodegaObserver;
        stockBodegaObserver.observe(stockBodegaElem, { 
            childList: true, 
            subtree: true, 
            attributes: true, 
            attributeFilter: ['data-stock'] 
        });
        
        // Inicializar estado
        lastValidatedQuantity = parseInt(cantidadInput.value || '0', 10);
        cambiarCantidad(lastValidatedQuantity);
    }


}


let lineasDocumento = {}; // Objeto para almacenar las líneas por producto


// Orden posicional histórico de agregarProducto en orden de venta.
// Mantenido para compatibilidad con call sites que aún pasan args sueltos.
const POSICIONALES_AGREGAR_PRODUCTO_ODV = [
    'docEntry_linea', 'linea_documento', 'productoCodigo', 'nombre', 'imagen',
    'precioVenta', 'stockTotal', 'precioLista', 'precioDescuento', 'cantidad',
    'sucursal', 'comentario', 'precioCoti', 'tipoEntrega2', 'fechaEntrega',
    'cuponDescuento', 'descuentoAplcado'
];

/**
 * Agrega un producto a la tabla de orden de venta. Acepta:
 *   - Forma nueva: agregarProducto({ docEntry_linea, linea_documento, ... })
 *   - Forma vieja: agregarProducto(docEntry_linea, linea_documento, ...)
 */
function agregarProducto(...rawArgs) {
    const opts = argsAOpts(rawArgs, POSICIONALES_AGREGAR_PRODUCTO_ODV);
    const {
        docEntry_linea,
        linea_documento,
        productoCodigo,
        nombre,
        imagen,
        precioVenta,
        stockTotal,
        precioLista,
        precioDescuento,
        cantidad = 1,
        sucursal,
        comentario,
        precioCoti,
        tipoEntrega2,
        fechaEntrega,
        cuponDescuento,
        descuentoAplcado = 0,
        cantidadCoti
    } = opts;

    lineasDocumento[productoCodigo] = {
        bodega: sucursal,
        cantidad: cantidad
    };

    let contprod = document.querySelectorAll('#productos tbody').length + 1; // Contador de productos

    const cantidadFinal = cantidad !== undefined ? cantidad : 1;
    // Orden de args alineado con el constructor de Producto:
    // (..., cuponDescuento, descuentoAplcado, tipoentrega2, cantidadCoti, precioCoti, fechaEntrega)
    const producto = new Producto(
        docEntry_linea, linea_documento, productoCodigo, nombre, imagen,
        precioVenta, stockTotal, precioLista, precioDescuento, cantidadFinal,
        sucursal, comentario,
        cuponDescuento, descuentoAplcado, tipoEntrega2,
        cantidadCoti, precioCoti, fechaEntrega
    );
    const newRow = producto.crearFila(contprod);

    // uid estable por fila — no cambia con drag&drop ni con recalcularIndices
    const uid = (window.crypto && crypto.randomUUID)
        ? crypto.randomUUID()
        : `prod_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    newRow.setAttribute('data-uid', uid);

    document.getElementById('productos').appendChild(newRow);

    aplicarUICupon(newRow, producto.cuponDescuento);

    newRow.querySelector('#mostrar-descuento').addEventListener('click', function () {
        producto.alternarMaxDescuento(newRow);
    });

    newRow.querySelector('#eliminarp').addEventListener('click', function () {
        const uidFila = newRow.getAttribute('data-uid');

        newRow.remove();

        const event = new CustomEvent('productoEliminado', {
            detail: {
                uid: uidFila,
                codigoProducto: productoCodigo,
                indiceProducto: contprod
            }
        });
        document.dispatchEvent(event);

        actualizarIndicesProductos();

        document.getElementById('inputNumero').focus();
    });

    producto.actualizarStock(newRow);


    const input_descuento = newRow.querySelector('#agg_descuento');
    const value_defecto = "0";
    input_descuento.addEventListener('input', () => {
        if (input_descuento.value === '') {
            input_descuento.value = value_defecto;
        }
    });

    newRow.querySelector('.form-select').addEventListener('change', function () {
        let stockBodegaElem = newRow.querySelector('[name="stock_bodega"]');
        let cantidadInput = newRow.querySelector('#calcular_cantidad');
        let stockTotalElem = newRow.querySelector('[name="stock_total"]');

        // Obtener valores antes del cambio
        let stockTotalActual = parseInt(stockTotalElem.textContent.replace('Total: ', '') || '0', 10);
        let cantidadActual = parseInt(cantidadInput.value || '0', 10);

        // Actualizar stock de la nueva bodega sin modificar el stock total
        producto.actualizarStock(newRow, false); // Pasar false para evitar la actualización del total

        setTimeout(() => { // Pequeño delay para asegurar que `actualizarStock` termine
            // Obtener el stock disponible de la NUEVA bodega seleccionada
            let stockDisponible = parseInt(stockBodegaElem.getAttribute('data-stock') || '0', 10);
            if (isNaN(stockDisponible) || stockDisponible < 0) stockDisponible = 0;

            // Establecer el nuevo máximo permitido
            cantidadInput.max = stockDisponible;

            let nuevaCantidad = 0;

            // **Disparar evento manualmente para forzar actualización**
            cantidadInput.dispatchEvent(new Event('input', { bubbles: true }));

            if (stockDisponible > 0) {
                nuevaCantidad = 1;
                cantidadInput.value = nuevaCantidad;
            } else {
                cantidadInput.value = 0;
                mostrarAlerta('No contamos con stock disponible para esta bodega.');
            }

            cantidadInput.dispatchEvent(new Event('input', { bubbles: true }));
        }, 50);
    });
    
    // Función para mostrar la alerta con Bootstrap
    function mostrarAlerta(mensaje) {
        let alerta = document.createElement('div');
        alerta.className = 'alert alert-warning alert-dismissible fade show';
        alerta.role = 'alert';
        alerta.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
    
        document.body.appendChild(alerta);
    
        // Remover la alerta después de unos segundos
        setTimeout(() => {
            alerta.remove();
        }, 3000);
    }    
    
    const inputNumero = document.getElementById("inputNumero");

    // Llamar a la función agregarInteractividad si es necesario

    agregarInteractividad(newRow, productoCodigo, contprod, uid);
}

document.addEventListener('productoEliminado', function(event) {
    const { codigoProducto } = event.detail;

    if (lineasDocumento[codigoProducto]) {
        let cantidadEliminada = lineasDocumento[codigoProducto].cantidad;
        
        // Buscar la fila eliminada
        let filaEliminada = document.querySelector(`.product-row [name="sku_producto"]:contains(${codigoProducto})`)?.closest('.product-row');
        if (!filaEliminada) return; // Si no encuentra la fila, salir

        // Obtener los elementos específicos de la fila eliminada
        let stockBodegaElem = filaEliminada.querySelector('[name="stock_bodega"]');
        let stockTotalElem = filaEliminada.querySelector('[name="stock_total"]');

        let stockBodegaActual = parseInt(stockBodegaElem.getAttribute('data-stock') || '0', 10);
        let stockTotalActual = parseInt(stockTotalElem.textContent.replace('Total: ', '') || '0', 10);

        // Restaurar stock sumando la cantidad eliminada
        //stockBodegaElem.textContent = `Stock: ${stockBodegaActual + cantidadEliminada}`;
        stockBodegaElem.setAttribute('data-stock', stockBodegaActual + cantidadEliminada);
        //stockTotalElem.textContent = `Total: ${stockTotalActual + cantidadEliminada}`;

        // Eliminar el producto de la memoria
        delete lineasDocumento[codigoProducto];
    }
});