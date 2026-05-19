class Producto extends ProductoBase {
    constructor(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, cantidadOriginal, sucursal, comentario, descuentoAplcado, estadoCheck) {
        super({
            docEntry_linea, linea_documento, productoCodigo, nombre, imagen,
            precioVenta, stockTotal, precioLista, precioDescuento, cantidad,
            sucursal, comentario,
            cuponDescuento: undefined, // solic_devolución no maneja cupón
            descuentoAplcado
        });
        this.cantidadOriginal = cantidadOriginal;
        this.estadoCheck = estadoCheck === 1; // bool
    }

    // Método para crear una fila en la tabla de productos
    crearFila(contprod) {
        let newRow = document.createElement('tbody');
        newRow.className = 'product-row';
        newRow.setAttribute('id', contprod);
        newRow.setAttribute('data-docentryLinea', this.docEntry_linea);
        newRow.setAttribute('data-itemcode', this.productoCodigo);
        newRow.setAttribute('data-indice', contprod); // Muy importante

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
                        <div class="col" style="text-align: center;">
                            <small style="font-size: 12px;" name="stock_bodega">Stock:  </small>
                            <small style="font-size: 12px;" id="stock_total" name="stock_total">Total: </small>
                        </div>
                    </div>
                </td>
                <td style="background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
                    <div style="font-size: 12px;">
                        <input class="form-control format-number" type="number" id="precio_venta2" style="font-size: 12px;width: 100px;" data-precioUnitario="${this.precioVenta}" min="1" max="999999999" value="${this.precioVenta}" readonly disabled>
                    </div>
                    <div style="font-size: 11px;">
                        <small class="numeric-value" style="color: rgb(153,153,153);" name="precio_lista" hidden>${formatCurrency(this.precioLista)}</small>
                    </div>

                    <div class="row" style="font-size: 11px;">
                        <div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0px;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="mostrar-descuento" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
                                <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z" hidden></path>
                            </svg>
                        </div>
                        <div class="col-sm-7 col-md-8">
                            <small  class="numeric-value" style="color: rgb(255,0,0);" id="descuento" name="descuento_max" hidden>Max: ${this.precioDescuento}%</small>
                        </div>
                    </div>
                </td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <div>
                        <input class="form-control format-number" type="number" style="font-size: 12px;width: 60px;" id="agg_descuento" min="0" value="${this.descuentoAplcado ?? 0}" onclick="this.select()" readonly disabled>
                    </div>
                </td>
                <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;" id="Precio_Descuento">${formatCurrency(this.precioSinDescuento)}</td>
                <td style="font-size: 12px;background: transparent;border-style: none;">
                    <input class="form-control format-number" type="number" style="font-size: 12px;width: 80px;"  id="calcular_cantidad" name="cantidad" min="1" max="${this.cantidadOriginal}" data-cantOriginal="${this.cantidadOriginal}" value="${this.cantidad}" onclick="this.select()">
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
                    <div class="form-check form-switch">
                        <input class="form-check-input switch-producto" type="checkbox" role="switch" id="switchCheckDefault" data-estado="${this.estadoCheck ? '1' : '0'}" ${this.estadoCheck ? 'checked' : ''}> 
                        <label class="form-check-label" for="switchCheckDefault"></label>
                    </div>
                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="eliminarp" class="bi bi-trash" style="width: 18px;height: 18px;" hidden>
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

        agregarTooltipStockBodegas(newRow, this.productoCodigo);

        return newRow;
    }
}

// Orden posicional histórico de agregarProducto en solicitud de devolución.
// Mantenido para compatibilidad con call sites que aún pasan args sueltos.
const POSICIONALES_AGREGAR_PRODUCTO_RR = [
    'docEntry_linea', 'linea_documento', 'productoCodigo', 'nombre', 'imagen',
    'precioVenta', 'stockTotal', 'precioLista', 'precioDescuento', 'cantidad',
    'cantidadOriginal', 'sucursal', 'comentario', 'descuentoAplcado', 'estadoCheck'
];

/**
 * Agrega un producto a la tabla de solicitud de devolución. Acepta:
 *   - Forma nueva: agregarProducto({ docEntry_linea, linea_documento, ... })
 *   - Forma vieja: agregarProducto(docEntry_linea, linea_documento, ...)
 */
function agregarProducto(...rawArgs) {
    const opts = argsAOpts(rawArgs, POSICIONALES_AGREGAR_PRODUCTO_RR);
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
        cantidadOriginal,
        sucursal,
        comentario,
        descuentoAplcado,
        estadoCheck
    } = opts;

    let contprod = document.querySelectorAll('#productos tbody').length + 1;

    // Crear una instancia de Producto
    let producto = new Producto(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, cantidadOriginal, sucursal, comentario, descuentoAplcado, estadoCheck);

    let newRow = producto.crearFila(contprod);

    document.getElementById('productos').appendChild(newRow);

    const indiceProducto = newRow.querySelector('#indixe_producto').getAttribute('data-indice'); 


    // Agregar eventos
    newRow.querySelector('#mostrar-descuento').addEventListener('click', function () {
        producto.alternarMaxDescuento(newRow);
    });

    newRow.querySelector('#eliminarp').addEventListener('click', function () {
        const indiceProducto = newRow.querySelector('#indixe_producto').getAttribute('data-indice');

        newRow.remove();

        const event = new CustomEvent('productoEliminado', {
            detail: {
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
    agregarInteractividad(newRow, productoCodigo, indiceProducto);
}