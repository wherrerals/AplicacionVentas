class DireccionManager {
  constructor() {
    this.contdir = 0; // Inicializamos el contador
    this.initializeEvents();
  }

  initializeEvents() {
    // Evento para agregar dirección en la pestaña principal
    document.getElementById('agregar_dir').addEventListener('click', () => this.agregarDireccion('dir'));
    // Evento para agregar dirección dentro del modal de facturación
    document.getElementById('agregar_dir_facturacion').addEventListener('click', () => this.agregarDireccion('listaDireccionFacturacion'));
    // Evento para agregar dirección dentro del modal de despacho
    document.getElementById('agregar_dir_despacho').addEventListener('click', () => this.agregarDireccion('listaDireccionDespacho'));
  }

  agregarDireccion(containerId) {
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
                  <option value="12" selected="">Despacho</option>
                  <option value="13">Facturación</option>
                </optgroup>
              </select>
            </div>
          </div>

          <div class="row">
            <div class="col-sm-4">
              <label class="col-form-label" style="font-size: 13px;">Dirección</label> 
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
                  <option value="12" selected="">Chile</option>
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
                  <option value="12" selected="">Arica y Parinacota</option>
                  <option value="1">Tarapacá</option>
                  <option value="2">Antofagasta</option>
                  <option value="2">Atacama</option>
                  <option value="13" selected="">Metropolitana de Santiago</option>
                </optgroup>
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
              <label class="col-form-label" style="font-size: 13px;">Comuna</label>
            </div>
            <div class="col">
              <select class="form-select" name="comuna[]" style="font-size: 12px;border-color: rgb(159,168,175);">
                <optgroup label="Comuna">
                  <option value="12" selected="">Arica</option>
                  <option value="2" selected="">Las Condes</option>
                  <option value="3">Santiago Centro</option>
                  <option value="4">Vitacura</option>
                </optgroup>
              </select>
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
  document.addEventListener('DOMContentLoaded', () => new DireccionManager());
  
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
                                      <label class="col-form-label" style="font-size: 13px;">ID</label>
                                      </div>
                                    <div class="col">
                                    <input class="form-control" name="direccion_static[]" id=direccion_${index} type="text" value="${direccion.id}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled>
                                    </div>
                                </div>

                                <div class="row">
                                  <div class="col-sm-4">
                                    <label class="col-form-label" style="font-size: 13px;">País</label>
                                  </div>
                                  <div class="col">
                                    <select class="form-select" id=pais_${index} name="pais_static[]" style="font-size: 12px; border-color: rgb(159,168,175);" disabled>
                                      <optgroup label="País">
                                        <option value="${direccion.pais}" selected>chile</option>
                                      </optgroup>
                                    </select>
                                  </div>
                                </div>


                                <div class="row">
                                <div class="col-sm-4">
                                  <label class="col-form-label" style="font-size: 13px;">Región</label>
                                </div>
                                <div class="col">
                                  <select class="form-select" id=region_${index} name="region_static[]" style="font-size: 12px; border-color: rgb(159,168,175);"disabled>
                                    <optgroup label="Región">
                                      <option value="12" ${direccion.region === "Arica y Parinacota" ? "selected" : ""}>Arica y Parinacota</option>
                                      <option value="1" ${direccion.region === "Tarapacá" ? "selected" : ""}>Tarapacá</option>
                                      <option value="2" ${direccion.region === "Antofagasta" ? "selected" : ""}>Antofagasta</option>
                                      <option value="3" ${direccion.region === "Atacama" ? "selected" : ""}>Atacama</option>
                                      <option value="13" ${direccion.region === "Metropolitana de Santiago" ? "selected" : ""}>Metropolitana de Santiago</option>
                                    </optgroup>
                                  </select>
                                </div>
                              </div>


                                <div class="row">
                                    <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Ciudad</label></div>
                                    <div class="col"><input id=ciudad_${index} name="cuidad_static[]" class="form-control" type="text" value="${direccion.ciudad}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                                </div>

                                <div class="row">
                                  <div class="col-sm-4">
                                    <label class="col-form-label" style="font-size: 13px;">Comuna</label>
                                  </div>
                                  <div class="col">
                                    <select class="form-select" id=comuna_${index} name="comuna_static[]" style="font-size: 12px; border-color: rgb(159,168,175);"disabled>
                                      <optgroup label="Comuna">
                                        <option value="12" ${direccion.comuna === "Arica" ? "selected" : ""}>Arica</option>
                                        <option value="2" ${direccion.comuna === "Las Condes" ? "selected" : ""}>Las Condes</option>
                                        <option value="3" ${direccion.comuna === "Santiago Centro" ? "selected" : ""}>Santiago Centro</option>
                                        <option value="4" ${direccion.comuna === "Vitacura" ? "selected" : ""}>Vitacura</option>
                                      </optgroup>
                                    </select>
                                  </div>
                                </div>


                                <div class="row">
                                    <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Dirección</label></div>
                                    <div class="col"><input id=nombreDireccion_${index} name="nombreDireccion_static[]" class="form-control" type="text" value="${direccion.nombreDireccion}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                                </div>
                            </div>
                        `;
                        $(listaSelector).append(direccionElemento); // Agregar la dirección al modal correspondiente

                        $(`#editar_dir_${index}`).on('click', function() {
                          // Hacer los campos editables
                          $(`#tipoDireccion_${index}`).prop('disabled', false);
                          $(`#direccion_${index}`).prop('disabled', false);
                          $(`#pais_${index}`).prop('disabled', false);
                          $(`#region_${index}`).prop('disabled', false);
                          $(`#ciudad_${index}`).prop('disabled', false);
                          $(`#comuna_${index}`).prop('disabled', false);
                          $(`#nombreDireccion_${index}`).prop('disabled', false);
                          
                          $(`#tipoDireccion_${index}`).attr('name', 'tipodireccion[]');
                          $(`#direccion_${index}`).attr('name', 'nombre_direccion[]');
                          $(`#pais_${index}`).attr('name', 'pais[]');
                          $(`#region_${index}`).attr('name', 'region[]');
                          $(`#ciudad_${index}`).attr('name', 'ciudad[]');
                          $(`#comuna_${index}`).attr('name', 'comuna[]');
                          $(`#nombreDireccion_${index}`).attr('name', 'direccion[]');
                          $(`#direccion_id${index}`).attr('name', 'direccionid[]');
                      });

                        $(`#eliminar_dir_${index}`).on('click', function() {
                          if (confirm('¿Estás seguro que deseas eliminar esta direccion?')) {
                              $(this).closest('.col-sm-5').remove();
                          }
                      });
                      
                    });
                } else {
                    console.log(`No hay direcciones de tipo ${tipoDireccion} para este cliente`);
                    $(listaSelector).html(`<p>No hay direcciones disponibles de este tipo.</p>`);
                }
            } else {
                console.log("No se encontraron clientes con el RUT proporcionado");
                $(listaSelector).html('<p>Error al cargar direcciones.</p>');
            }
        },
        error: (xhr, status, error) => {
            console.error('Error al obtener las direcciones del cliente:', error);
            $(listaSelector).html('<p>Error al cargar direcciones.</p>');
        }
    });
}

// Inicializar la gestión de direcciones al cargar la página
$(document).ready(() => {
    initDireccionManager();
});
