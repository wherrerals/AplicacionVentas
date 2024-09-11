document.addEventListener('DOMContentLoaded', function () {

    console.log('Documento cargado. JS activo.');
    // Función para obtener el valor de un parámetro de consulta y convertirlo a entero
    function getQueryParamInt(param) {
        const urlParams = new URLSearchParams(window.location.search);
        const paramValue = urlParams.get(param);
        if (paramValue !== null) {
            return parseInt(paramValue, 10); // Parseamos el valor a entero base 10
        }
        return null;
    }

    const docEntry = getQueryParamInt('docEntry'); // Aquí obtenemos el docNum como entero
    console.log('docEntry obtenido:', docEntry);

    if (docEntry !== null) { // Verificamos que docNum no sea null antes de usarlo
        console.log('docEntry:', docEntry);
        fetch(`generar_cotizacion/${docEntry}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data);
                if (data && data.DocumentLines && data.DocumentLines.length > 0) {
                    const documentLines = data.DocumentLines;
                    console.log('Procesando líneas de documentos...');

                    documentLines.forEach(line => {

                        var newRow = document.createElement('tbody');
                        contprod++;

                        newRow.innerHTML =
                        `
<tr>
    <td style="font-size: 12px; background: transparent; border-style: none; padding-bottom: 0px;" rowspan="2">
        <div class="row">
            <div class="col-md-11 col-xxl-6" style="font-size: 14px; font-weight: bold;">
                <small>${contprod})</small><small>&nbsp;&nbsp;</small><small style="font-weight-bold"
                    name="sku_producto">${line.ItemCode}</small>
            </div>
            <div class="col-md-11 col-xxl-7" style="text-align: center;">
                <img src="" width="50" height="50" style="width: 50px;height: 50px;" name="img_producto">
            </div>
        </div>
    </td>
    <td style="font-size: 12px; background: transparent; border-style: none; padding-bottom: 0px;" rowspan="2">
        <div class="row">
            <div class="col-sm-12 col-lg-12 col-xl-11 col-xxl-10">
                <select class="form-select" style="font-size: 11px;">
                    <optgroup label="Bodega">
                        <option value="12" selected="">GR</option>
                        <option value="13">LC</option>
                        <option value="14">PH</option>
                        <option value="15">ME</option>
                    </optgroup>
                </select>
            </div>
            <div class="col" style="text-align: center;>
                <small style=" font-size: 12px;" name="stock_total">Stock:${line.Quantity}</small>
            </div>
        </div>
    </td>
    <td style="background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
        <div style="font-size: 12px;">
            <small name="precio_venta">${line.Price}</small>
        </div>
        <div style="font-size: 11px;">
            <small style="color: rgb(153,153,153);" name="precio_lista">Antes: ${line.LineTotal}</small>
        </div>
        <div class="row" style="font-size: 11px;">
            <div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16"
                    id="mostrar-descuento" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
                    <path
                        d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z">
                    </path>
                </svg>
            </div>
            <div class="col-sm-7 col-md-8">
                <small style="color: rgb(255,0,0);" id="descuento" name="descuento_max" hidden>Max:
                    ${line.LineTotal}</small>
            </div>
        </div>
    </td>
    <td style="font-size: 12px;background: transparent;border-style: none;">
        <div>
            <input class="form-control" type="number" style="font-size: 12px;width: 60px;" id="agg_descuento" min="1"
                max="1000">
        </div>
    </td>
    <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;"
        id="Precio_Descuento">${line.LineTotal}</td>
    <td style="font-size: 12px;background: transparent;border-style: none;">
        <input class="form-control" type="number" style="width: 65px;" id="calcular_cantidad" min="1" max="1000"
            value=0>
    </td>
    <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">
        <span id="precio_Venta">${line.LineTotal}</span>
    </td>
</tr>
<tr style="font-size: 12px;background: transparent;">
    <td style="font-size: 11px;background: transparent;padding-top: 0px;border-style: none;padding-bottom: 0px;"
        colspan="3">
        <input class="form-control" type="text" placeholder="Comentario" style="font-size: 12px;">
    </td>
    <td style="background: transparent;padding-top: 8px;padding-left: 50px;border-style: none;padding-bottom: 0px;">
        <a class="navbar-brand d-flex align-items-center" href="#" style="width: 18px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16"
                id="eliminarp" class="bi bi-trash" style="width: 18px;height: 18px;">
                <path
                    d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z">
                </path>
                <path
                    d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z">
                </path>
            </svg>
</tr>
<tr style="font-size: 12px;background: transparent;">
    <td colspan="7" style="padding-top: 0px;background: transparent;"><span>${line.ItemDescription}</span></td>
</tr>
`;

      // Agregar la fila a la tabla
  document.getElementById('productos').appendChild(newRow);
                    });
                } else {
                    console.log('No se encontraron líneas de documentos válidas en la respuesta');
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    } else {
        console.error('El parámetro docEntry no se encontró en la URL o no es un número válido');
    }
});

const productosTable = document.getElementById('productos');
if (productosTable) {
    productosTable.appendChild(newRow);
} else {
    console.error('No se encontró el elemento con id "productos" en el DOM');
}
