class Producto {
    constructor(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, descuentoAplcado, tipoentrega2, cantidadCoti, precioCoti, fechaEntrega = new Date().toISOString().split('T')[0]) {
        
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
        this.cantidadCoti = cantidadCoti;
        this.precioCoti = precioCoti;
        this.comentario = comentario;
        this.tipoEntrega2 = tipoentrega2;
        this.fechaEntrega = fechaEntrega;
        this.descuentoAplcado = descuentoAplcado ?? 0;

        console.log("atributos del constructor mapeados",
            {
                docEntry_linea: this.docEntry_linea,
                linea_documento: this.linea_documento,
                productoCodigo: this.productoCodigo,
                nombre: this.nombre,
                imagen: this.imagen,
                precioVenta: this.precioVenta,
                stockTotal: this.stockTotal,
                precioLista: this.precioLista,
                precioDescuento: this.precioDescuento,
                precioSinDescuento: this.precioSinDescuento,
                totalProducto: this.totalProducto,
                cantidad: this.cantidad,
                sucursal: this.sucursal,
                cantidadCoti: this.cantidadCoti,
                precioCoti: this.precioCoti,
                comentario: this.comentario,
                tipoEntrega2: this.tipoEntrega2,
                fechaEntrega: this.fechaEntrega,
                descuentoAplcado: this.descuentoAplcado}

        );



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


    async actualizarStock(row, actualizarStockTotal = true) {
        console.log("Producto a actualizar:", this.productoCodigo);
    
        const stockData = await this.obtenerStock(this.productoCodigo);
        
        console.log("Stock data en actualizar Stock:", stockData);
    
        if (stockData) {
            // Mapear las bodegas válidas (excluyendo GR)
            const bodegaMap = {
                "LC": "LC",
                "PH": "PH",
                "ME": "ME"
            };
    
            // Filtrar los datos de stock excluyendo la bodega "GR"
            const stockFiltrado = stockData.filter(bodega => bodega.bodega !== "GR");
    
            console.log("Stock filtrado en actualizar Stock:", stockFiltrado);
    
            // Calcular el stock total sumando solo las bodegas válidas
            const stockTotal = stockFiltrado.reduce((total, bodega) => total + bodega.stock, 0);
    
            // Mostrar el stock total solo si se solicita
            if (actualizarStockTotal) {
                const stockTotalElem = row.querySelector('[name="stock_total"]');
                console.log("Stock total actualizado en actualizar Stock:", stockTotal);
                stockTotalElem.textContent = `Total: ${stockTotal}`;
            }
    
            // Obtener el value de la bodega seleccionada
            const selectBodega = row.querySelector('.form-select');
            const valueSeleccionado = selectBodega.value;
    
            // Usar el mapa para obtener el código correspondiente
            const bodegaSeleccionada = bodegaMap[valueSeleccionado];
    
            // Encontrar el stock de la bodega seleccionada
            const stockBodega = stockFiltrado.find(bodega => bodega.bodega === bodegaSeleccionada)?.stock || 0;
            const name_bodega = stockFiltrado.find(bodega => bodega.bodega === bodegaSeleccionada)?.bodega || 0;
    
            console.log("Bodega seleccionada zzzzz:", name_bodega);
    
            // Mostrar el stock de la bodega seleccionada
            const stockBodegaElem = row.querySelector('[name="stock_bodega"]');
            stockBodegaElem.textContent = `Stock: ${stockBodega}`;
            stockBodegaElem.setAttribute('data-stock', stockBodega);  // Almacenar el valor en un atributo data-stock
    
            console.log("Stock actualizado:", stockBodega);
            
            // NUEVO: Asignar stock a cada option del select
            for (const bodega of stockFiltrado) {
                const optionElement = selectBodega.querySelector(`option[id="${bodega.bodega}"]`);
                if (optionElement) {
                    optionElement.setAttribute('data-stock', bodega.stock);
                    // Opcionalmente, puedes mostrar el stock en el texto del option
                    // optionElement.textContent = `${bodega.bodega} (${bodega.stock})`;
                }
            }
            
            // Retornar el stock total calculado para uso externo
            return stockTotal;
        }
        return 0;
    }

    crearFila(contprod) {
        let newRow = document.createElement('tbody');
        newRow.className = 'product-row';
        //aggregar id a la fila
        newRow.setAttribute('id', contprod);
        newRow.setAttribute('data-docentryLinea', this.docEntry_linea);
        newRow.setAttribute('data-itemcode', this.productoCodigo);
        newRow.innerHTML = `
            <tr>
                <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;"rowspan="2">
                    <div class="row">
                        <div class="col-md-11 col-xxl-6" style="font-size: 14px;font-weight: bold;"><small style="font-weight: bold;">
                        <small id="indixe_producto" data-lineNum="${this?.linea_documento}">${contprod})</small><small>&nbsp;&nbsp;</small><small name="sku_producto">${this.productoCodigo}</small></div>
                        <div class="col-md-11 col-xxl-7" style="text-align: center;"><img src="${this.imagen}" width="50" height="50" style="width: 50px;height: 50px;" name="img_producto" id="img_productox"></div>
                    </div>
                </td>
                <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;"rowspan="2">
                    <div class="row">
                    <div class="col-sm-12 col-lg-12 col-xl-11 col-xxl-10">
                        <select class="form-select bodega-select" style="font-size: 11px;">
                          <optgroup label="Bodega">
                            <option id="LC" data-stock="" value="LC" ${this.sucursal === 'LC' ? 'selected' : '' } data-cantidadInicialSAP="${this.sucursal === 'LC' && this.cantidad !== undefined ? this.cantidad : 0}">LC</option>
                            <option id="ME" data-stock="" value="ME" ${this.sucursal === 'ME' ? 'selected' : ''} data-cantidadInicialSAP="${this.sucursal === 'ME' && this.cantidad !== undefined ? this.cantidad : 0}">ME</option>
                            <option id="PH" data-stock="" value="PH" ${this.sucursal === 'PH' ? 'selected' : ''} data-cantidadInicialSAP="${this.sucursal === 'PH' && this.cantidad !== undefined ? this.cantidad : 0}">PH</option>
                            </optgroup>
                        </select>
                    </div>
                    <div class="col" style="text-align: center;">
                        <small style="font-size: 12px;" name="stock_bodega" id="stock_bodega">Stock: </small>
                        <small name="stock_total" id="stock_total">Total: </small>
                    </div>
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
                        <input class="form-control" type="number" style="font-size: 12px;width: 60px;" id="agg_descuento" min="0" value="${this.descuentoAplcado ?? 0}">
                    </div>
                </td>
                   
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;" id="Precio_Descuento">${this.precioSinDescuento}</td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <div>
                        <input class="form-control" type="number" style="font-size: 12px;width: 60px;" id="calcular_cantidad" name="cantidad" min="1" max="1000" value="${this.cantidad !== undefined ? this.cantidad : 0}">
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
                    <span name="nombre_producto">${this.nombre}</span>
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
                <td td colspan="2" style="background: transparent;">
                    <input class="form-control" type="date" name="fechaEntrega" id="fecha_entrega_lineas" style="width: 90%;font-size: 13px;" value="${this.fechaEntrega}">
                </td>
            </tr>
        `;

        function formatCurrency(value) {
            // Convertimos el valor a número entero
            const integerValue = Math.floor(value);
            let formattedValue = integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
        
            // Si el valor tiene 4 dígitos y no incluye un punto, lo añadimos manualmente
            if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
                formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
            }
        
            // Agregamos el símbolo de peso al principio
            return `$ ${formattedValue}`;
        }

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

        inputDescuento.value = this.descuentoAplcado;  // Cambié de 0 a this.descuentoAplcado

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
        } else {
            console.log("Elemento encontrado:", numeroOrdenElem);
            console.log("DocEntry en limitarCantidad:", numeroOrdenElem.getAttribute('data-docentryLinea'));
        }
        
        const docEntry = numeroOrdenElem?.getAttribute('data-docentryLinea');
        
    
        // Referencias a elementos DOM
        const cantidadInput = row.querySelector('#calcular_cantidad');
        const stockBodegaElem = row.querySelector('[name="stock_bodega"]');

        console.log("Stock bodega en limitarCantidad:", stockBodegaElem.textContent);

        const stockTotalElem = row.querySelector('[name="stock_total"]') || { textContent: '0' };
        const skuElem = row.querySelector('[name="sku_producto"]');
        
        // Si el producto comienza con "SV", no limitamos la cantidad
        if (skuElem && skuElem.textContent.startsWith('SV')) {
            return;
        }
    
        // Banderas y estado inicial
        let isUpdating = false;
        let lastValidatedQuantity = parseInt(cantidadInput.value || '0', 10);
        
        // Almacenar la cantidad inicial cuando carga el documento
        if (!cantidadInput.hasAttribute('data-initial-value') && docEntry) {
            cantidadInput.setAttribute('data-initial-value', cantidadInput.value || '0');

            console.log("Cantidad inicial:", cantidadInput.value);
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
                console.log("Stock bodega 2 en calcularCantidadMaxima:", valores.stockBodega2);
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
                        console.log("diferencia de entrada:", diferencia);
                        
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


function agregarProducto(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad = 1, sucursal, comentario, precioCoti, tipoEntrega2, fechaEntrega, descuentoAplcado = 1 - 1) {
    
    
    lineasDocumento[productoCodigo] = {
        bodega: sucursal,
        cantidad: cantidad
    };    

    console.log("Cantidad recibida en agregarProducto:", cantidad);


    let contprod = document.querySelectorAll('#productos tbody').length + 1; // Contador de productos

    // Crear instancia del producto

    const cantidadFinal = cantidad !== undefined ? cantidad : 1;
    const producto = new Producto(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidadFinal, sucursal, comentario, precioCoti, tipoEntrega2, fechaEntrega, descuentoAplcado);
    const newRow = producto.crearFila(contprod); // Crear la fila del producto

    document.getElementById('productos').appendChild(newRow); // Agregar la fila al tbody


    newRow.querySelector('#mostrar-descuento').addEventListener('click', function () {
        producto.alternarMaxDescuento(newRow);
    });

    newRow.querySelector('#eliminarp').addEventListener('click', function () {
        // Eliminar la fila del DOM
        newRow.remove();
    
        // Emitir un evento personalizado pasando el código del producto
        const event = new CustomEvent('productoEliminado', {
            detail: { codigoProducto: productoCodigo,
                indiceProducto: contprod

            }
        });
        console.log('Evento emitido:', event);
        document.dispatchEvent(event);

        // Actualizar los índices de los productos visibles
        actualizarIndicesProductos();
        
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

    newRow.querySelector('.form-select').addEventListener('change', function () {
        let stockBodegaElem = newRow.querySelector('[name="stock_bodega"]');
        let cantidadInput = newRow.querySelector('#calcular_cantidad');
        let stockTotalElem = newRow.querySelector('[name="stock_total"]');

        console.log("Stock bodega actual:", stockBodegaElem.textContent);
        console.log("Stock total actual:", stockTotalElem.textContent);
        console.log("Cantidad actual:", cantidadInput.value);
        
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
            
            // Verificar el stock y ajustar la cantidad
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
            
            // Calcular la diferencia de cantidad y corregir el stock total
            let diferenciaCantidad = nuevaCantidad - cantidadActual;
            
            // Actualizar el stock de la bodega actual basado en el stock disponible
            let stockBodegaActualizado = stockDisponible - nuevaCantidad;
            //stockBodegaElem.textContent = `Stock: ${stockBodegaActualizado}`;
            console.log("Nuevo stock de bodega:", stockBodegaActualizado);
            
            // Ajustar el total asegurando que no quede negativo
            let nuevoStockTotal = Math.max(0, stockTotalActual - diferenciaCantidad);
            //stockTotalElem.textContent = `Total: ${nuevoStockTotal}`;
            console.log("Nuevo stock total:", nuevoStockTotal);
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
    agregarInteractividad(newRow, productoCodigo, contprod);

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