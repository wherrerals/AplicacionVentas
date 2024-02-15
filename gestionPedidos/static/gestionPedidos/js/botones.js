function agregarProducto(productoCodigo, nombre, stockTotal, precioLista, precioVenta, linkProducto, imagen) {
    
    var productoCodigo = productoCodigo;
    var nombre = nombre;
    var stockTotal = stockTotal;
    var precioLista = precioLista;
    var precioVenta = precioVenta;
    var linkProducto = linkProducto;
    var imagen = imagen;
    
    // Crear una nueva fila
    var newRow = document.createElement('tbody');

    // Definir el contenido de la fila
    newRow.innerHTML = `
<tr>
    <td style="font-size: 12px; background: transparent; border-style: none; padding-bottom: 0px;" rowspan="2">
        <div class="row">
            <div class="col-md-11 col-xxl-6" style="font-size: 14px; font-weight: bold;">
            <small>1)</small><small>&nbsp;&nbsp;</small><small style="font-weight-bold">${productoCodigo}</small>
            </div>
            <div class="col-md-11 col-xxl-7" style="text-align: center;">
                <img src="${imagen}" width="50" height="50" style="width: 50px;height: 50px;">
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
                <small style="font-size: 12px;">Stock:${stockTotal}</small>
            </div>
        </div>
    </td>
    <td style="background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
        <div style="font-size: 12px;">
            <small>${precioVenta}</small>
        </div>
        <div style="font-size: 11px;">
            <small style="color: rgb(153,153,153);">Antes: ${precioLista}</small>
        </div>
        <div class="row" style="font-size: 11px;">
            <div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="mostrar-descuento" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
                    <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"></path>
                </svg>
            </div>
            <div class="col-sm-7 col-md-8">
                <small style="color: rgb(255,0,0);" id="descuento" hidden>Max: ${linkProducto}</small>
            </div>
        </div>
    </td>
    <td style="font-size: 12px;background: transparent;border-style: none;">
        <div>
            <input class="form-control" type="text" style="font-size: 12px;width: 40px;">
        </div>
    </td>
    <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">${precioVenta}</td>
    <td style="font-size: 12px;background: transparent;border-style: none;">
        <input class="form-control" type="text" style="width: 65px;">
    </td>
    <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">
        <span>${precioVenta}</span>
    </td>
</tr> 
    <tr style="font-size: 12px;background: transparent;">
        <td style="font-size: 11px;background: transparent;padding-top: 0px;border-style: none;padding-bottom: 0px;"colspan="3">
            <input class="form-control" type="text" placeholder="Comentario" style="font-size: 12px;">
        </td>
        <td style="background: transparent;padding-top: 8px;padding-left: 50px;border-style: none;padding-bottom: 0px;">
            <a class="navbar-brand d-flex align-items-center" href="#" style="width: 18px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" id="eliminar-producto" class="bi bi-trash" style="width: 18px;height: 18px;">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z">
            </path>
            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z">
            </path>
        </svg>
    </tr>
    <tr style="font-size: 12px;background: transparent;">
        <td colspan="7" style="padding-top: 0px;background: transparent;"><span>${nombre}</span></td>
    </tr>
    `;
    
    // Agregar la fila a la tabla
    document.getElementById('productos').appendChild(newRow);

    // Agregar el evento de clic al ícono de descuento para alternar la visibilidad del elemento oculto
    newRow.querySelector('#mostrar-descuento').addEventListener('click', function() {
        AlternarMaxDescuento();
    });  

    //Eliminar fila de la tabla
    newRow.querySelector('#eliminar-producto').addEventListener('click', function() {
        newRow.remove();
    });

    function AlternarMaxDescuento() {
        var elemento = newRow.querySelector('#descuento');
        if (elemento.getAttribute('hidden') !== null) {
            elemento.removeAttribute('hidden');
        } else {
            elemento.setAttribute('hidden', '');
        }
    }

};

/*
// Función para guardar los productos en localStorage
function guardarProductos() {
    localStorage.setItem('productos', document.getElementById('productos').innerHTML);
}

function cargarProductosGuardados() {
    var productosGuardados = localStorage.getItem('productos');
    if (productosGuardados) {
        document.getElementById('productos').innerHTML = productosGuardados;
    }
}


// Función para cargar los productos desde localStorage al cargar la página
function cargarProductosGuardados() {
    var productosGuardados = localStorage.getItem('productos');
    if (productosGuardados) {
        document.getElementById('productos').innerHTML = productosGuardados;
    }
}

*/
window.addEventListener('DOMContentLoaded', function() {
    // Asignar el evento click al botón agregar_productos (siempre que exista)
    var botonAgregarProductos = document.getElementById('agregar_productos');
    if (botonAgregarProductos) {
        botonAgregarProductos.addEventListener('click', agregarProducto);
    }

});


function togglePassword() {
    var toggleButton = document.getElementById("togglePasswordButton");
    var passwordInput = document.getElementById("password");

    toggleButton.addEventListener("click", function() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            toggleButton.textContent = "Ocultar";
        } else {
            passwordInput.type = "password";
            toggleButton.textContent = "Mostrar";
        }
    });
}

togglePassword();