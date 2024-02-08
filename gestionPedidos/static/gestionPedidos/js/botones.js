// Función para cargar los productos desde localStorage al cargar la página
function cargarProductosGuardados() {
    var productosGuardados = localStorage.getItem('productos');
    if (productosGuardados) {
        document.getElementById('productos').innerHTML = productosGuardados;
    }
}


function agregarProducto(productoCodigo, stock, precioActual, precioAnterior, maxDescuento) {
    // Crear una nueva fila
    var newRow = document.createElement('tr');

    // Definir el contenido de la fila
    newRow.innerHTML = `

    <td>
    <div class="row">
        <div class="col-md-11 col-xxl-6">
            <small>1)</small>&nbsp;&nbsp;
            <small class="font-weight-bold">${productoCodigo}</small>
        </div>
        <div class="col-md-11 col-xxl-7 text-center">
            <img src="https://ledstudiocl.vtexassets.com/arquivos/ids/166187-80-auto/label-0.jpg" width="50" height="50">
        </div>
    </div>
</td>
<td>
    <div class="row">
        <div class="col-sm-12 col-lg-12 col-xl-11 col-xxl-10">
            <select class="form-select" style="font-size: 11px;">
                <optgroup label="Bodega">
                    <option value="12">GR</option>
                    <option value="13">LC</option>
                    <option value="14">PH</option>
                    <option value="15">ME</option>
                </optgroup>
            </select>
        </div>
        <div class="col text-center">
            <small class="font-size-12">Stock: ${stock}</small>
        </div>
    </div>
</td>
<td>
    <div class="font-size-12">
        <small>${precioActual}</small>
    </div>
    <div class="font-size-11">
        <small class="text-muted">Antes: ${precioAnterior}</small>
    </div>
    <div class="row font-size-11">
        <div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0;">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
                <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"></path>
            </svg>
        </div>
        <div class="col-sm-7 col-md-8">
            <small class="text-danger">Max: ${maxDescuento}</small>
        </div>
    </div>
</td>
<td>
    <input class="form-control" type="text">
</td>
<td class="font-size-11 text-center">${precioActual}</td>
<td>
    <input class="form-control" type="text" style="width: 65px;">
</td>
<td class="font-weight-bold font-size-11 text-center">${precioActual}
<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="eliminar-producto"
class="bi bi-trash" style="width: 18px;height: 18px;">
<path
    d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z">
</path>
<path
    d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z">
</path>
</svg>


    `;
    
    // Agregar la fila a la tabla
    document.getElementById('productos').appendChild(newRow);

    //Eliminar fila de la tabla
    newRow.querySelector('.eliminar-producto').addEventListener('click', function() {
        newRow.remove();
    });

  };


// Función para guardar los productos en localStorage
function guardarProductos() {
    localStorage.setItem('productos', document.getElementById('productos').innerHTML);
}

// Escuchar el evento DOMContentLoaded para cargar los productos guardados
window.addEventListener('DOMContentLoaded', function() {
    cargarProductosGuardados();

    // Asignar el evento click al botón agregar_productos
    document.getElementById('agregar_productos').addEventListener('click', agregarProducto);
});

function fechaHora(){

}

agregarProducto('N10100256', '12', '1.964.900', '2.999.900', '15%');
