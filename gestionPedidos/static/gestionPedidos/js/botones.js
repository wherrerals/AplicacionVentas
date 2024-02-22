function agregarProducto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento) {

  var descuento = precioVenta - precioLista;
  console.log("Agregando producto:");
  console.log("Código:", productoCodigo);
  console.log("Nombre:", nombre);
  console.log("Imagen:", imagen);
  console.log("Precio de venta:", precioVenta);
  console.log("Stock total:", stockTotal);
  console.log("Precio anterior:", precioLista);
  console.log("Precio de descuento máximo:", precioDescuento);
  console.log("calculo descuento", descuento);

  
  
  // Crear una nueva fila
  var newRow = document.createElement('tbody');

  // Definir el contenido de la fila
  newRow.innerHTML = `
<tr>
  <td style="font-size: 12px; background: transparent; border-style: none; padding-bottom: 0px;" rowspan="2">
      <div class="row">
          <div class="col-md-11 col-xxl-6" style="font-size: 14px; font-weight: bold;">
          <small>1)</small><small>&nbsp;&nbsp;</small><small style="font-weight-bold" name="sku_producto">${productoCodigo}</small>
          </div>
          <div class="col-md-11 col-xxl-7" style="text-align: center;">
              <img src="${imagen}" width="50" height="50" style="width: 50px;height: 50px;" name="img_producto">
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
              <small style="color: rgb(255,0,0);" id="descuento" hidden>Max: ${precioDescuento}</small>
          </div>
      </div>
  </td>
  <td style="font-size: 12px;background: transparent;border-style: none;">
      <div>
          <input class="form-control" type="text" style="font-size: 12px;width: 40px;">
      </div>
  </td>
  <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">${descuento}</td>
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
  
  return resultado;
};

var contdir = 0;
function agergardireccion(){

  
  var newRow = document.createElement('div');
  contdir ++;
  newRow.className = "col-sm-1";
  newRow.style="padding: 0px;width: 280px";


  newRow.innerHTML =`
  <div class="col-sm-12" style="width: 100%;height: 10px;"><span>&nbsp;</span></div>
  <div class="col-sm-5" style="font-size: 12px;background: #f0f2f5;width: 250px;">
    <div class="row">
      <div class="col-sm-12" style="height: 15px;background: transparent;">
        <span>&nbsp;</span>
      </div>
      <div class="col" style="text-align: center;"><span
          style="font-weight: bold;">Dirección Nº ${contdir} </span></div>
      <div class="col-sm-12" style="height: 5px;background: transparent;">
        <span>&nbsp;</span>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-9"><span></span></div>
      <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;"><a
          class="navbar-brand d-flex align-items-center"
          href="lista_cotizaciones.html" style="width: 32px;"><svg
            xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
            fill="currentColor" viewBox="0 0 16 16" class="bi bi-pencil-square"
            style="font-size: 24px;">
            <path
              d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z">
            </path>
            <path fill-rule="evenodd"
              d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z">
            </path>
          </svg></a></div>
      <div class="col-sm-1" style="padding-right: 0px;padding-left: 10px;"><a
          class="navbar-brand d-flex align-items-center"
           style="width: 32px;"><svg
            xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
            fill="currentColor" viewBox="0 0 16 16" class="bi bi-backspace"
            style="font-size: 24px;" id="eliminar_dir">
            <path
              d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z">
            </path>
            <path
              d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z">
            </path>
          </svg></a></div>
      <div class="col-sm-12" style="height: 10px;background: transparent;">
        <span>&nbsp;</span>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-4"><label class="col-form-label"
          style="font-size: 13px;">Tipo</label></div>
      <div class="col"><select class="form-select"
          style="font-size: 12px;border-color: rgb(159,168,175);">
          <optgroup label="Tipo">
            <option value="12" selected="">Despacho</option>
            <option value="13">Facturación</option>
          </optgroup>
        </select></div>
    </div>
    <div class="row">
      <div class="col-sm-4"><label class="col-form-label"
          style="font-size: 13px;">ID</label></div>
      <div class="col"><input class="form-control" type="text"
          name="nombreDireccion"
          style="border-color: rgb(159,168,175);font-size: 12px;"></div>
    </div>
    <div class="row">
      <div class="col-sm-4"><label class="col-form-label"
          style="font-size: 13px;">País</label></div>
      <div class="col"><select class="form-select"
          style="font-size: 12px;border-color: rgb(159,168,175);">
          <optgroup label="País">
            <option value="12" selected="">Chile</option>
          </optgroup>
        </select></div>
    </div>
    <div class="row">
      <div class="col-sm-4"><label class="col-form-label"
          style="font-size: 13px;">Región</label></div>
      <div class="col"><select class="form-select"
          style="font-size: 12px;border-color: rgb(159,168,175);">
          <optgroup label="Región">
            <option value="12" selected="">Arica y Parinacota</option>
            <option value="1">Tarapacá</option>
            <option value="2">Antofagasta</option>
            <option value="2">Atacama</option>
            <option value="13" selected="">Metropolitana de Santiago</option>
          </optgroup>
        </select></div>
    </div>
    <div class="row">
      <div class="col-sm-4"><label class="col-form-label"
          style="font-size: 13px;">Ciudad</label></div>
      <div class="col"><input class="form-control" type="text" name="pais"
          style="border-color: rgb(159,168,175);font-size: 12px;"></div>
    </div>
    <div class="row">
      <div class="col-sm-4"><label class="col-form-label"
          style="font-size: 13px;">Comuna</label></div>
      <div class="col"><select class="form-select"
          style="font-size: 12px;border-color: rgb(159,168,175);">
          <optgroup label="Comuna">
            <option value="12" selected="">Arica</option>
            <option value="2" selected="">Las Condes</option>
            <option value="3">Santiago Centro</option>
            <option value="4">Vitacura</option>
          </optgroup>
        </select></div>
    </div>
    <div class="row">
      <div class="col-sm-4"><label class="col-form-label"
          style="font-size: 13px;">Dirección</label></div>
      <div class="col"><input class="form-control" type="text" name="pais"
          style="border-color: rgb(159,168,175);font-size: 12px;"></div>
    </div>
    <div class="row">
      <div class="col-sm-12" style="height: 15px;background: transparent;">
        <span>&nbsp;</span>
      </div>
      
    </div>
  </div>`;

  var tab1 = document.getElementById('dir');

  tab1.style.display = "flex";
  tab1.style.flexDirection = "row";
  tab1.style.overflowX = "auto";
  tab1.style.maxWidth = "100%";


  document.getElementById('dir').appendChild(newRow);

  newRow.querySelector('#eliminar_dir').addEventListener('click', function() {
    newRow.remove();
});

}

window.addEventListener('DOMContentLoaded', function() {
  // Asignar el evento click al botón agregar_productos (siempre que exista)
  var botonAgregarProductos = document.getElementById('agregar_dir');
  if (botonAgregarProductos) {
      botonAgregarProductos.addEventListener('click', agergardireccion);
  }

});

var contcon = 0;
function agregarontacto(){

  var newRow = document.createElement('div')
  newRow.className = "col-sm-1";
  newRow.style="padding: 0px;width: 280px";
  contcon ++;
  newRow.innerHTML =`

<div class="col-sm-12" style="width: 100%;height: 10px;"><span>&nbsp;</span> </div>
<div class="col-sm-5" style="font-size: 12px;background: #f0f2f5;width: 250px;">


  <div class="row">
    <div class="col-sm-12" style="height: 15px;background: transparent;"> <span>&nbsp;</span></div>
    <div class="col" style="text-align: center;">
        <span style="font-weight: bold;">Contacto Nº ${contcon} </span>
    </div>
    <div class="col-sm-12" style="height: 5px;background: transparent;"> <span>&nbsp;</span> </div>
  </div>

  <div class="row">
    <div class="col-sm-9"><span></span></div>
    <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;">
      <a class="navbar-brand d-flex align-items-center" href="lista_cotizaciones.html" style="width: 32px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-pencil-square" style="font-size: 24px;">
          <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"> </path>
          <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"> </path>
        </svg>
      </a>
    </div>
    

    <div class="col-sm-1" style="padding-right: 0px;padding-left: 10px;">
      <a class="navbar-brand d-flex align-items-center"  style="width: 32px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-backspace" style="font-size: 24px;" id="eliminar_contacto">
          <path d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z"> </path>
          <path d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"> </path>
        </svg>
      </a>
    </div>
    <div class="col-sm-12" style="height: 10px;background: transparent;"> <span>&nbsp;</span> </div>
  </div>


  <div class="row">
    <div class="col-sm-4">
      <label class="col-form-label" style="font-size: 13px;">Nombre
      </label>
    </div>
    <div class="col">
      <input class="form-control" type="text" name="nombreDireccion" style="border-color: rgb(159,168,175);font-size: 12px;">
    </div>
  </div>


  <div class="row">
    <div class="col-sm-4">
      <label class="col-form-label" style="font-size: 13px;">Apellido
      </label>
    </div>
    <div class="col"><input class="form-control" type="text" name="pais" style="border-color: rgb(159,168,175);font-size: 12px;"></div>
  </div>


  <div class="row">
    <div class="col-sm-4">
      <label class="col-form-label" style="font-size: 13px;">Teléfono
      </label>
    </div>
    <div class="col"><input class="form-control" type="tel" style="font-size: 12px;border-color: rgb(159,168,175);"></div>
  </div>


  <div class="row">
    <div class="col-sm-4">
      <label class="col-form-label" style="font-size: 13px;">Celular
      </label>
    </div>
    <div class="col"><input class="form-control" type="tel" style="font-size: 12px;border-color: rgb(159,168,175);"></div>
  </div>


  <div class="row">
    <div class="col-sm-4">
      <label class="col-form-label" style="font-size: 13px;">Email
      </label>
    </div>
    <div class="col"><input class="form-control" type="email" style="font-size: 12px;border-color: rgb(159,168,175);"></div>
  </div>


  <div class="row">
    <div class="col-sm-12" style="height: 15px;background: transparent;">
      <span>&nbsp;</span>
    </div>
  </div>

</div>
<!-- <div class="col-sm-1" style="padding: 0px;width: 20px;"><span></span></div> Revisar bien, es espacio lateral-->
`;

  var tab2 = document.getElementById('cont');
  tab2.style.display = "flex";
  tab2.style.flexDirection = "row";
  tab2.style.overflowX = "auto";
  tab2.style.maxWidth = "100%";

  document.getElementById('cont').appendChild(newRow);

  newRow.querySelector('#eliminar_contacto').addEventListener('click', function() {
      newRow.remove();
  });

}

window.addEventListener('DOMContentLoaded', function() {
    // Asignar el evento click al botón agregar_productos (siempre que exista)
    var botonAgregarProductos = document.getElementById('agregar_cont');
    if (botonAgregarProductos) {
        botonAgregarProductos.addEventListener('click', agregarontacto);
    }
});

/* tabladireccion.querySelector('#agregar_dir').addEventListener('click', function() {
  agergardireccion();
});   */


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


/* window.addEventListener('DOMContentLoaded', function() {
  // Asignar el evento click al botón agregar_productos (siempre que exista)
  var botonAgregarProductos = document.getElementById('agregar_dir');
  if (botonAgregarProductos) {
      botonAgregarProductos.addEventListener('click', agergardireccion);
  }

}); */


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

agregarProducto(C25500123,"WILLIAM ALEXIS HERRERA", "ISO.JPG", 2000.00, 50, 150.00, 500.0)