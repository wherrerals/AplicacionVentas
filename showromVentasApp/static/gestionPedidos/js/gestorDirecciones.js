class DireccionManager {
  constructor() {
    this.contdir = 0; // Inicializamos el contador
    this.initializeEvents();
  }

  initializeEvents() {
    // Evento para agregar dirección en la pestaña principal
    document.getElementById('agregar_dir').addEventListener('click', () => this.agregarDireccion('dir', 'Despacho'));
    // Evento para agregar dirección dentro del modal de facturación
    document.getElementById('agregar_dir_facturacion').addEventListener('click', () => this.agregarDireccion('listaDireccionFacturacion', 'Facturación'));
    // Evento para agregar dirección dentro del modal de despacho
    document.getElementById('agregar_dir_despacho').addEventListener('click', () => this.agregarDireccion('listaDireccionDespacho', 'Despacho'));
  }

  agregarDireccion(containerId, tipoDireccion) {
    this.contdir++;  // Incrementa el contador cada vez que se agrega una nueva dirección

    // Crear una nueva fila para la dirección
    let newRow = document.createElement('div');
    newRow.className = "col-sm-5";
    newRow.style = "font-size: 12px;background: #f0f2f5;width: 230px; margin-right: 10px;";
    newRow.innerHTML = `
        <div class="col-sm-12" style="width: 100%;height: 10px;"><span>&nbsp;</span></div>
        
          <div class="row">
            <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span></div>
            <div class="col" style="text-align: center;">
              <span style="font-weight: bold;">Dirección Nº ${this.contdir}</span></div>
            <div class="col-sm-12" style="height: 5px;background: transparent;"><span>&nbsp;</span></div>
          </div>
  
          <div class="row">
            <div class="col-sm-8"><span></span></div>
            <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;"> </div>
            <div class="col-sm-1" style="padding-right: 0px;padding-left: 10px;">
              <a class="navbar-brand d-flex align-items-center" style="width: 32px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-backspace" style="font-size: 24px;" id="eliminar_dir">
                  <path d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z"></path>
                  <path d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"></path>
                </svg>
              </a>
            </div>
            <div class="col-sm-12" style="height: 10px;background: transparent;"><span>&nbsp;</span></div>
          </div>

          <div class="row">
            <div class="col-sm-4">
              <label class="col-form-label" style="font-size: 13px;">Tipo</label>
            </div>
            <div class="col">
              <select class="form-select" name="tipodireccion[]" style="font-size: 12px;border-color: rgb(159,168,175);">
                <optgroup label="Tipo">
                  <option value="12" ${tipoDireccion === 'Despacho' ? 'selected' : ''}>Despacho</option>
                  <option value="13" ${tipoDireccion === 'Facturación' ? 'selected' : ''}>Facturación</option>
                </optgroup>
              </select>
            </div>
          </div>

          <div class="row">
            <div class="col-sm-4">
              <label class="col-form-label" style="font-size: 13px;">Nombre</label> 
            </div>
            <div class="col">
              <input class="form-control" type="text" name="nombre_direccion[]" id="nombre_direccion" style="border-color: rgb(159,168,175);font-size: 12px;">
            </div>
          </div>

          <div class="row">
            <div class="col-sm-4">
              <label class="col-form-label" style="font-size: 13px;">País</label>
            </div>
            <div class="col">
              <select class="form-select" name="pais[]" style="font-size: 12px;border-color: rgb(159,168,175);">
                <optgroup label="País">
                  <option value="Chile" selected="">Chile</option>
                </optgroup>
              </select>
            </div>
          </div>

          <div class="row">
            <div class="col-sm-4">
              <label class="col-form-label" style="font-size: 13px;">Región</label>
            </div>
            <div class="col">
              <select class="form-select" name="region[]" style="font-size: 12px;border-color: rgb(159,168,175);">
                <optgroup label="Región">
                  <option value="15">Arica y Parinacota</option>
                  <option value="1">Tarapacá</option>
                  <option value="2">Antofagasta</option>
                  <option value="3">Atacama</option>
                  <option value="4">Coquimbo</option>
                  <option value="5">Valparaíso</option>
                  <option value="13">Metropolitana de Santiago</option>
                  <option value="6">Libertador General Bernardo O'Higgins</option>
                  <option value="7">Maule</option>
                  <option value="16">Ñuble</option>
                  <option value="8">Biobío</option>
                  <option value="9">La Araucanía</option>
                  <option value="14">Los Ríos</option>
                  <option value="10">Los Lagos</option>
                  <option value="11">Aysén del General Carlos Ibáñez del Campo</option>
                  <option value="12">Magallanes y de la Antártica Chilena</option>
                </optgroup>
              </select>
            </div>
          </div>


          <div class="row">
            <div class="col-sm-4">
              <label class="col-form-label" style="font-size: 13px;">Comuna</label>
            </div>
            <div class="col">
              <select class="form-select" name="comuna[]" style="font-size: 12px;border-color: rgb(159,168,175);">
                <option value="">Seleccione una comuna</option>
                <!-- Las comunas se cargarán dinámicamente aquí -->
              </select>
            </div>
          </div>

          <div class="row">
            <div class="col-sm-4">
              <label class="col-form-label" style="font-size: 13px;">Ciudad</label>
            </div>
            <div class="col">
              <input class="form-control" type="text" name="ciudad[]" id="ciudad" style="border-color: rgb(159,168,175);font-size: 12px;">
            </div>
          </div>

          <div class="row">
            <div class="col-sm-4">
              <label clas s="col-form-label" style="font-size: 13px;">Dirección</label>
            </div>
            <div class="col">
              <input class="form-control" type="text" name="direccion[]" id="direccion" style="border-color: rgb(159,168,175);font-size: 12px;">
            </div>
          </div>

          <div class="row">
            <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span></div>
          </div>
      
        <div class="col-sm-1" style="padding: 0px;width: 20px;"><span></span></div>
      `;
  
      // Agregar la nueva fila al contenedor indicado
    let container = document.getElementById(containerId);
    container.style.display = "flex";
    container.style.flexDirection = "row";
    container.style.overflowX = "auto"; // Permitir desplazamiento horizontal
    container.appendChild(newRow);
      
      container.appendChild(newRow);
      newRow.querySelector('#eliminar_dir').addEventListener('click', () => newRow.remove());
    }
  }
  

  // Crear una instancia de DireccionManager al cargar la página
  $(document).ready(() => {
    new DireccionManager();
  });

  
// Inicializa los eventos y configuraciones
function initDireccionManager() {
    $(document).ready(() => {
        // Evento para abrir el modal de despacho
        $('#dirDespModal').on('show.bs.modal', () => {
            let clienteRut = $('#inputCliente').attr('data-rut');
            console.log("RUT del cliente:", clienteRut);
            if (clienteRut) {
                cargarDirecciones(clienteRut, "12", '#listaDireccionDespacho'); // Cargar solo direcciones de despacho (tipo 12)
            } else {
                $('#listaDireccionDespacho').html('<p>No se ha seleccionado un cliente.</p>');
            }
        });

        // Evento para abrir el modal de facturación
        $('#dirFactModal').on('show.bs.modal', () => {
            let clienteRut = $('#inputCliente').attr('data-rut');
            console.log("RUT del cliente:", clienteRut);
            if (clienteRut) {
                cargarDirecciones(clienteRut, "13", '#listaDireccionFacturacion'); // Cargar solo direcciones de facturación (tipo 13)
            } else {
                $('#listaDireccionFacturacion').html('<p>No se ha seleccionado un cliente.</p>');
            }
        });
    });
}

// Función para cargar direcciones del cliente seleccionado
function cargarDirecciones(clienteRut, tipoDireccion, listaSelector) {
    let buscarClientesUrl = '/ventas/buscar_clientes/';

    $.ajax({
        url: buscarClientesUrl,
        data: { 'numero': clienteRut },
        dataType: 'json',
        success: (data) => {
            $(listaSelector).empty(); // Limpiar el contenido previo

            if (data.resultadosClientes && data.resultadosClientes.length > 0) {
                const cliente = data.resultadosClientes[0];
                const direcciones = cliente.direcciones || [];
                console.log("Direcciones encontradas:", direcciones);

                // Filtrar direcciones por tipo
                const direccionesFiltradas = direcciones.filter(direccion => direccion.tipoDireccion === tipoDireccion);

                if (direccionesFiltradas.length > 0) {
                    direccionesFiltradas.forEach((direccion, index) => {
                        let direccionElemento = `

                             <div class="col-sm-5" style="font-size: 12px;background: #f0f2f5;width: 230px; margin-right: 10px;">
                                <div class="row">
                                    <div class="col-sm-12" style="height: 15px; background: transparent;"><span>&nbsp;</span></div>
                                    <div class="col" style="text-align: center;">
                                        <span style="font-weight: bold;">Dirección Nº${index + 1}</span>
                                    </div>
                                    <div class="col-sm-12" style="height: 5px; background: transparent;"><span>&nbsp;</span></div>
                                </div>
                                <div class="row">
                                  <div class="col-sm-8"><span></span></div>
                                  <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;">
                                    <a class="navbar-brand d-flex align-items-center" style="width: 32px;" id="editar_dir_${index}">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-pencil-square" style="font-size: 24px;">
                                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"></path>
                                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"></path>
                                      </svg>
                                    </a>
                                  </div>
                                  <div class="col-sm-1" style="padding-right: 0px;padding-left: 10px;">
                                    <a class="navbar-brand d-flex align-items-center" style="width: 32px;"  id="eliminar_dir_${index}">
                                      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-backspace" style="font-size: 24px;">
                                        <path d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z"></path>
                                        <path d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"></path>
                                      </svg>
                                    </a>
                                  </div>
                                  <div class="col-sm-12" style="height: 10px;background: transparent;"><span>&nbsp;</span></div>
                                </div>

                                <input type="hidden" name="contacto_id[]" value="${direccion.id}" id="contacto_id_${index}">

                                <div class="row">
                                    <div class="col-sm-4">
                                      <label class="col-form-label" style="font-size: 13px;">Tipo</label>
                                    </div>
                                    <div class="col">
                                        <select class="form-select" name="tipoDireccion_static[]" id=tipoDireccion_${index} value="${direccion.tipoDireccion}" style="font-size: 12px; border-color: rgb(159,168,175);" disabled>
                                            <optgroup label="Tipo">
                                                <option value="12" ${direccion.tipoDireccion === "12" ? "selected" : ""}>Despacho</option>
                                                <option value="13" ${direccion.tipoDireccion === "13" ? "selected" : ""}>Facturación</option>
                                            </optgroup>
                                        </select>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-sm-4">
                                      <label class="col-form-label" style="font-size: 13px;">Nombre</label>
                                      </div>
                                    <div class="col">
                                    <input class="form-control" name="direccion_static[]" id=direccion_${index} type="text" value="${direccion.nombreDireccion}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled>
                                    </div>
                                </div>

                                <div class="row">
                                  <div class="col-sm-4">
                                    <label class="col-form-label" style="font-size: 13px;">País</label>
                                  </div>
                                  <div class="col">
                                    <select class="form-select" id=pais_${index} name="pais_static[]" style="font-size: 12px; border-color: rgb(159,168,175);" disabled>
                                      <optgroup label="País">
                                        <option value="${direccion.pais}" selected>Chile</option>
                                      </optgroup>
                                    </select>
                                  </div>
                                </div>


                                <div class="row">
                                <div class="col-sm-4">
                                  <label class="col-form-label" style="font-size: 13px;">Región</label>
                                </div>
                                <div class="col">
                                  <select class="form-select" id="region_${index}" name="region_static[]" style="font-size: 12px; border-color: rgb(159,168,175);" disabled>
                                    <optgroup label="Región">
                                      <option value="15" ${direccion.region === "Arica y Parinacota" ? "selected" : ""}>Arica y Parinacota</option>
                                      <option value="1" ${direccion.region === "Tarapacá" ? "selected" : ""}>Tarapacá</option>
                                      <option value="2" ${direccion.region === "Antofagasta" ? "selected" : ""}>Antofagasta</option>
                                      <option value="3" ${direccion.region === "Atacama" ? "selected" : ""}>Atacama</option>
                                      <option value="4" ${direccion.region === "Coquimbo" ? "selected" : ""}>Coquimbo</option>
                                      <option value="5" ${direccion.region === "Valparaíso" ? "selected" : ""}>Valparaíso</option>
                                      <option value="13" ${direccion.region === "Metropolitana de Santiago" ? "selected" : ""}>Metropolitana de Santiago</option>
                                      <option value="6" ${direccion.region === "Libertador General Bernardo O'Higgins" ? "selected" : ""}>Libertador General Bernardo O'Higgins</option>
                                      <option value="7" ${direccion.region === "Maule" ? "selected" : ""}>Maule</option>
                                      <option value="16" ${direccion.region === "Ñuble" ? "selected" : ""}>Ñuble</option>
                                      <option value="8" ${direccion.region === "Biobío" ? "selected" : ""}>Biobío</option>
                                      <option value="9" ${direccion.region === "La Araucanía" ? "selected" : ""}>La Araucanía</option>
                                      <option value="14" ${direccion.region === "Los Ríos" ? "selected" : ""}>Los Ríos</option>
                                      <option value="10" ${direccion.region === "Los Lagos" ? "selected" : ""}>Los Lagos</option>
                                      <option value="11" ${direccion.region === "Aysén del General Carlos Ibáñez del Campo" ? "selected" : ""}>Aysén del General Carlos Ibáñez del Campo</option>
                                      <option value="12" ${direccion.region === "Magallanes y de la Antártica Chilena" ? "selected" : ""}>Magallanes y de la Antártica Chilena</option>
                                    </optgroup>
                                  </select>
                                </div>
                              </div>


                                <div class="row">
                                  <div class="col-sm-4">
                                    <label class="col-form-label" style="font-size: 13px;">Comuna</label>
                                  </div>
                                    <div class="col">
                                        <select class="form-select" id="comuna_${index}" name="comuna_static[]" style="font-size: 12px; border-color: rgb(159,168,175);" disabled>
                                            <optgroup label="Comuna">
                                                <!-- Las opciones de comunas se cargarán dinámicamente -->
                                            </optgroup>
                                        </select>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Ciudad</label></div>
                                    <div class="col"><input id=ciudad_${index} name="cuidad_static[]" class="form-control" type="text" value="${direccion.ciudad}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                                </div>


                                <div class="row">
                                    <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Dirección</label></div>
                                    <div class="col"><input id=nombreDireccion_${index} name="nombreDireccion_static[]" class="form-control" type="text" value="${direccion.calleNumero}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                                </div>
                            </div>
                        `;
                        $(listaSelector).append(direccionElemento); // Agregar la dirección al modal correspondiente

                        $(document).on('click', `#editar_dir_${index}`, function() {
                          console.log("Habilitando edición para la dirección con index:", index);
                          
                          // Hacer los campos editables
                          $(`#tipoDireccion_${index}`).prop('disabled', false);
                          $(`#direccion_${index}`).prop('disabled', false);
                          $(`#pais_${index}`).prop('disabled', false);
                          $(`#region_${index}`).prop('disabled', false);
                          $(`#ciudad_${index}`).prop('disabled', false);
                          $(`#comuna_${index}`).prop('disabled', false);
                          $(`#nombreDireccion_${index}`).prop('disabled', false);
                          
                          // Añadir los atributos name a los campos editados
                          $(`#tipoDireccion_${index}`).attr('name', 'tipodireccion[]');
                          $(`#direccion_${index}`).attr('name', 'nombre_direccion[]');
                          $(`#pais_${index}`).attr('name', 'pais[]');
                          $(`#region_${index}`).attr('name', 'region[]');
                          $(`#ciudad_${index}`).attr('name', 'ciudad[]');
                          $(`#comuna_${index}`).attr('name', 'comuna[]');
                          $(`#nombreDireccion_${index}`).attr('name', 'direccion[]');
                          $(`#contacto_id_${index}`).attr('name', 'direccionid[]');
                      
                          console.log("Edición habilitada para la dirección con index:", index);
                      });
                      

                        $(`#eliminar_dir_${index}`).on('click', function() {
                          if (confirm('¿Estás seguro que deseas eliminar esta direccion?')) {
                              $(this).closest('.col-sm-5').remove();
                          }
                      });
                      
                    });
                } else {
                    console.log(`No hay direcciones de tipo ${tipoDireccion} para este cliente`);
                    $(listaSelector).html(`<p id="dirmens1">No hay direcciones disponibles de este tipo.</p>`);
                }
            } else {
                console.log("No se encontraron clientes con el RUT proporcionado");
                $(listaSelector).html('<p id="dirmens1>Error al cargar direcciones.</p>');
            }
        },
        error: (xhr, status, error) => {
            console.error('Error al obtener las direcciones del cliente:', error);
            $(listaSelector).html('<p id="dirmens1>Error al cargar direcciones.</p>');
        }
    });
}

// Inicializar la gestión de direcciones al cargar la página
$(document).ready(() => {
    initDireccionManager();
});


$(document).on('change', '[id^="region_"]', function() {
  const regionId = $(this).val();  // Obtener el valor de la región seleccionada
  const index = $(this).attr('id').split('_')[1];  // Extraer el índice dinámico del ID
  const comunaSelect = $(`#comuna_${index}`);  // Seleccionar el select de comuna correspondiente

  console.log("Región seleccionada:", regionId);
  console.log("Index detectado:", index);
  console.log("Select de comunas encontrado:", comunaSelect);

  if (regionId) {
    cargarComunas(regionId, comunaSelect);  // Llamar a la función para cargar comunas
  } else {
    $(comunaSelect).empty().append('<option value="">Seleccione una comuna</option>');  // Si no hay región seleccionada
  }
});


function cargarComunas(regionId, comunaSelect, comunaSeleccionada = null) {
  console.log("Cargando comunas para la región con ID:", regionId);


  $.ajax({
    url: `/ventas/obtener_comunas_por_region/?idRegion=${regionId}`,  // Asegúrate de que esta ruta sea la correcta
    method: 'GET',
    success: function(data) {
      console.log("Datos recibidos del servidor:", data);
      $(comunaSelect).empty();
      $(comunaSelect).append('<option value="">Seleccione una comuna</option>');

      // Rellenar el select con las comunas obtenidas
      data.forEach(function(comuna) {
        let selected = comunaSeleccionada && comunaSeleccionada === comuna.nombre ? "selected" : "";
        $(comunaSelect).append(`<option value="${comuna.codigo}" ${selected}>${comuna.nombre}</option>`);
      });

      console.log("Select de comunas actualizado.");
    },
    error: function(xhr, status, error) {
      console.error("Error al cargar comunas:", error);
      $(comunaSelect).empty().append('<option value="">Error al cargar comunas</option>');
    }
  });
}


$(document).on('change', 'select[name="region[]"]', function() {
  const regionId = $(this).val();  // Obtener el valor de la región seleccionada

  // Subir al contenedor padre y luego buscar el siguiente select de comuna
  const comunaSelect = $(this).closest('.row').next().find('select[name="comuna[]"]');

  console.log("Región seleccionada:", regionId);  // Verificar qué región se seleccionó
  console.log("Select de comunas encontrado:", comunaSelect);

  if (regionId) {
    cargarComunas(regionId, comunaSelect);  // Llamar a la función para cargar comunas
  } else {
    $(comunaSelect).empty().append('<option value="">Seleccione una comuna</option>');  // Si no hay región seleccionada
  }
});


