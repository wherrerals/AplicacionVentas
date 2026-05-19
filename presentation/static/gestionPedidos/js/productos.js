class Producto extends ProductoBase {
    constructor(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, cuponDescuento, descuentoAplcado) {
        super({
            docEntry_linea, linea_documento, productoCodigo, nombre, imagen,
            precioVenta, stockTotal, precioLista, precioDescuento, cantidad,
            sucursal, comentario, cuponDescuento, descuentoAplcado
        });
    }

    crearFila(contprod) {
        let newRow = document.createElement('tbody');
        newRow.className = 'product-row';
        newRow.setAttribute('id', contprod);
        newRow.setAttribute('data-docentryLinea', this.docEntry_linea);
        newRow.setAttribute('data-itemcode', this.productoCodigo);


        // draggable se maneja solo desde el handle, no en toda la fila

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
                          <select class="form-select bodega-select" style="font-size: 11px;">
                            <optgroup label="Bodega">
                            <option value="LC" ${this.sucursal === 'LC' ? 'selected' : ''}>Las Condes (LC)</option>
                            <option value="PH" ${this.sucursal === 'PH' ? 'selected' : ''}>Vitacura (PH)</option>
                            <option value="ME" ${this.sucursal === 'ME' ? 'selected' : ''}>Panal (ME)</option>
                            <option value="VI" ${this.sucursal === 'VI' ? 'selected' : ''}>Viña del Mar (VI)</option>
                            <option value="GR" ${this.sucursal === 'GR' ? 'selected' : ''}>Ñuñoa (GR)</option>
                            </optgroup>
                          </select>
                        </div>
                        <div class="col" style="text-align: left;">
                            <small style="font-size: 12px;" name="stock_bodega">Stock:  </small>
                            <small style="font-size: 12px;" id="stock_total" name="stock_total">Total: </small>
                            <div id="warning_container" style="display: inline-block;" hidden>
                                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-exclamation-triangle" viewBox="0 0 16 16" style="color: rgba(255, 7, 7, 1);margin-left: 2px;" name="warning_icon">
                                    <path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/>
                                    <path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
                                </svg>
                            </div>
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
                        <small class="numeric-value" name="precio_venta" data-precio-unitario="100.00" data-precioUnitario="${this.precioVenta}">${formatCurrencyCLP(this.precioVenta)}</small>
                    </div>
                    <div style="font-size: 11px;">
                        <small class="numeric-value" style="color: rgb(153,153,153);" name="precio_lista">${formatCurrencyCLP(this.precioLista)}</small>
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
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;" id="Precio_Descuento">${formatCurrencyCLP(this.precioSinDescuento)}</td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <input class="form-control format-number" type="number" style="font-size: 12px;width: 80px;"  id="calcular_cantidad" name="cantidad" min="1" max="1000" value="${this.cantidad}" onclick="this.select()">
                </td>
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">
                    <span id="precio_Venta" data-totalProductValue="${this.totalProducto}">${formatCurrencyCLP(this.totalProducto)}</span>
                </td>
            </tr> 
            <tr style="font-size: 12px;background: transparent;">
                <td style="font-size: 11px;background: transparent;padding-top: 0px;border-style: none;padding-bottom: 0px;"colspan="3">
                    <input class="form-control" type="text" placeholder="Comentario" id="comentarios-1" style="font-size: 12px;" value="${this.comentario ?? ''}"></input>
                </td>
                <td style="background: transparent;padding-top: 8px;padding-left: 50px;border-style: none;padding-bottom: 0px;">
                    <div class="d-flex align-items-center gap-2">
                        <!-- Botón eliminar -->
                        <a class="navbar-brand d-flex align-items-center" href="#" style="width: 18px;">
                          <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="eliminarp" class="bi bi-trash" style="width: 18px;height: 18px;">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"> </path>
                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"> </path>
                          </svg>
                        </a>

                    </div>
                </td>
            <tr style="font-size: 12px;background: transparent;">
                
                <td colspan="7" style="padding-top: 0px; background: transparent;">
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

                    <span id="drag-handle" 
                        title="Arrastrar para reordenar" 
                        style="cursor: grab; color: #888; user-select: none; padding: 4px 12px; display: flex; align-items: center; justify-content: center;">
                        
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M7 2a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM7 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                        </svg>
                    </span>

                </div>
                </td>
            </tr>
            </tr>
        `;

        agregarTooltipStockBodegas(newRow, this.productoCodigo);

        this.limitarMaxDescuento(newRow);
        inicializarDragAndDrop(newRow);

        return newRow;
    }
}

// Orden posicional histórico de agregarProducto en cotización.
// Mantenido para compatibilidad con call sites que aún pasan args sueltos.
const POSICIONALES_AGREGAR_PRODUCTO_COTIZACION = [
    'docEntry_linea', 'linea_documento', 'productoCodigo', 'nombre', 'imagen',
    'precioVenta', 'stockTotal', 'precioLista', 'precioDescuento', 'cantidad',
    'sucursal', 'comentario', 'cuponDescuento', 'descuentoAplcado'
];

/**
 * Agrega un producto a la tabla. Acepta:
 *   - Forma nueva: agregarProducto({ docEntry_linea, linea_documento, ... })
 *   - Forma vieja: agregarProducto(docEntry_linea, linea_documento, ...)
 */
function agregarProducto(...rawArgs) {
    const opts = argsAOpts(rawArgs, POSICIONALES_AGREGAR_PRODUCTO_COTIZACION);
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
        cuponDescuento,
        descuentoAplcado
    } = opts;

    let contprod = document.querySelectorAll('#productos tbody').length + 1;

    let producto = new Producto(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, cuponDescuento, descuentoAplcado);

    let newRow = producto.crearFila(contprod);

    // uid estable por fila — no cambia con drag&drop ni con recalcularIndices
    const uid = (window.crypto && crypto.randomUUID)
        ? crypto.randomUUID()
        : `prod_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    newRow.setAttribute('data-uid', uid);

    document.getElementById('productos').appendChild(newRow);

    aplicarUICupon(newRow, producto.cuponDescuento);

    const indiceProducto = newRow.querySelector('#indixe_producto').getAttribute('data-indice');

    const input_descuento = newRow.querySelector('#agg_descuento');
    const value_defecto = "0";
    input_descuento.addEventListener('input', () => {
        if (input_descuento.value === '') {
            input_descuento.value = value_defecto;
        }
    });

    const input_cantidad = newRow.querySelector('#calcular_cantidad');
    const value_defecto_cant = "1";
    input_cantidad.addEventListener('input', () => {
        if (input_cantidad.value === '') {
            input_cantidad.value = value_defecto_cant;
        }
    });

    // Agregar eventos
    newRow.querySelector('#mostrar-descuento').addEventListener('click', function () {
        producto.alternarMaxDescuento(newRow);
    });

    newRow.querySelector('#eliminarp').addEventListener('click', function () {
        const uidFila = newRow.getAttribute('data-uid');
        const indiceProducto = newRow.querySelector('#indixe_producto').getAttribute('data-indice');

        newRow.remove();

        const event = new CustomEvent('productoEliminado', {
            detail: {
                uid: uidFila,
                codigoProducto: productoCodigo,
                indiceProducto: indiceProducto
            }
        });
        document.dispatchEvent(event);

        actualizarIndicesProductos();

        document.getElementById('inputNumero').focus();
    });

    producto.actualizarStock(newRow);

    // Evento para actualizar el stock al cambiar de bodega
    newRow.querySelector('.form-select').addEventListener('change', function () {
        producto.actualizarStock(newRow);
    });

    // Llamar a la función agregarInteractividad si es necesario
    agregarInteractividad(newRow, productoCodigo, indiceProducto, uid);
}