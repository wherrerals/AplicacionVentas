document.addEventListener("DOMContentLoaded", function () {
  function getQueryParam(param) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
  }

  const rutInputSearch = document.querySelector('input[type="search"]');
  const rutInputField = document.getElementById('rutSN');
  const rut = getQueryParam('rut');

  const fetchClienteData = (rut) => {
            if (rut) {
              const cleanedRut = rut.replace(/\./g, '').split('-')[0];
              const clienteElement = document.querySelector("#nombreApellidoSN p");
              const codigoElement = document.querySelector("#rut-display p");

            if (clienteElement && codigoElement) {
              clienteElement.textContent = "Cargando...";
              codigoElement.textContent = "Cargando...";
            } fetch(`/ventas/informacion_cliente/?rut=${cleanedRut}`)
              .then(response => {
                  if (!response.ok) throw new Error('Error al obtener la información del cliente');
                  return response.json();
              })
              .then(data => {
              
                  console.log("Datos del cliente:", data);
                  document.getElementById("nombreSN").value = data[0].nombre || '';
                  document.getElementById("apellidoSN").value = data[0].apellido || '';
                  document.getElementById("rutSN").value = data[0].rut || '';
                  document.getElementById("giroSN").value = data[0].giro || '';
                  document.getElementById("telefonoSN").value = data[0].telefono || '';
                  document.getElementById("emailSN").value = data[0].email || '';

                  document.querySelector("#nombreApellidoSN p").textContent = `${data[0].apellido || ''}`;
                  document.querySelector("#rut-display p").textContent = `${data[0].codigoSN || ''}`;                  
                
                  document.getElementById("rutSN").setAttribute("data-rut", data[0].rut || '');
                  document.getElementById("rutSN").readOnly = true;

                    // Lógica para seleccionar "Empresa" o "Persona"
                    if (data[0].grupoSN && data[0].grupoSN.trim() !== "") {
                      // Si tiene razón social (giro), es "Empresa"
                      document.getElementById("formCheck-6").checked = true; // Empresa
                  } else {
                      // Si no tiene razón social (giro), es "Persona"
                      document.getElementById("formCheck-5").checked = true; // Persona
                  }

                  // Actualizar etiquetas y mostrar/ocultar campos dinámicamente
                  cambiarLabel('grupoSN', 'nombreLabel', 'apellidoSN', 'apellidorow');

                  // Llama a cargarContactos después de asignar data-rut
                  cargarContactos();
                  cargarDirecciones();
              })
              .catch(error => {
                  console.error('Error en la solicitud AJAX:', error);
              });
      } else {
          console.error("No se proporcionó un RUT en la URL");
      }
  };

  // Si hay un `rut` en la URL, cargar datos
  if (rut) {
      fetchClienteData(rut);
  }

  const handleRutInput = (inputElement) => {
      inputElement.addEventListener("keydown", function (event) {
          if (event.key === "Enter") {
              event.preventDefault(); // Evita el comportamiento predeterminado
              let inputRut = inputElement.value.trim();
              if (inputRut) {
                  // Quitar puntos y todo después del guion antes de buscar
                  inputRut = inputRut.replace(/\./g, '').split('-')[0];
                  fetchClienteData(inputRut);

                  // Limpiar el campo de entrada
                  inputElement.value = '';
              } else {
                  alert("Por favor, ingrese un RUT válido para buscar.");
              }
          }
      });
  };


  //Actualiza el texto de codigo cliente en cliente.html
  document.getElementById('rutSN').addEventListener('input', function (event) {
    const inputText = event.target.value;
    const rutDisplayParagraph = document.querySelector('#rut-display p');

    const modifiedText = inputText.length > 0 ? inputText.slice(0, -1) + 'C' : '';
  
    rutDisplayParagraph.textContent = modifiedText;
  });
  
  // Aplicar el manejo de entrada a ambos campos
  if (rutInputSearch) {
      handleRutInput(rutInputSearch);
  }
  if (rutInputField) {
      handleRutInput(rutInputField);
  }
});


// Función para cargar contactos, ahora debería funcionar
function cargarContactos() {
  const clienteRut = $('#rutSN').attr('data-rut');
  console.log("Valor de clienteRut desde data-rut:", clienteRut);

  if (clienteRut && clienteRut.trim() !== "") {
      $.ajax({
          url: '/ventas/buscar_clientes/',
          data: { 'numero': clienteRut },
          dataType: 'json',
          success: function(data) {
              $('#cont').empty();
              if (data.resultadosClientes && data.resultadosClientes.length > 0) {
                  const cliente = data.resultadosClientes[0];
                  const contactos = cliente.contactos;
                  contactos.forEach(function(contacto, index) {
                      let contactoElemento = `
                      <div class="col-sm-5" style="font-size: 12px;background: #f0f2f5;width: 230px; margin-right: 10px;">
                          <div class="row">
                              <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span></div>
                              <div class="col" style="text-align: center;"> 
                                  <span style="font-weight: bold;">Contacto Nº${index + 1}</span>
                              </div>
                              <div class="col-sm-12" style="height: 5px;background: transparent;"><span>&nbsp;</span></div>
                          </div>
                          <div class="row">
                            <div class="col-sm-8"><span></span></div>
                            <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;">
                              <a class="navbar-brand d-flex align-items-center" style="width: 32px;" id="editar_contacto_${index}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-pencil-square" style="font-size: 24px;">
                                  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"></path>
                                  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"></path>
                                </svg>
                              </a>
                            </div>
                            <div class="col-sm-1" style="padding-right: 0px;padding-left: 10px;">
                              <a class="navbar-brand d-flex align-items-center" style="width: 32px;" id="eliminar_contacto_${index}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-backspace" style="font-size: 24px;">
                                  <path d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z"></path>
                                  <path d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"></path>
                                </svg>
                              </a>
                            </div>
                          <div class="col-sm-12" style="height: 10px;background: transparent;"><span>&nbsp;</span></div>
                          </div>
  
                          <input type="hidden" name="contacto_id[]" value="${contacto.id}" id="contacto_id_${index}">
  
  
                          <div class="row">
                              <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Nombre</label></div>
                              <div class="col"><input class="form-control" type="text" name="nombre_static[]" value="${contacto.nombre}" id="nombre_${index}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                          </div>
                          <div class="row">
                              <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Apellido</label></div>
                              <div class="col"><input class="form-control" type="text" name="apellido_static[]" value="${contacto.apellido}" id="apellido_${index}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                          </div>
                          <div class="row">
                              <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Teléfono</label></div>
                              <div class="col"><input class="form-control" type="text" name="telefono_static[]" value="${contacto.telefono}" id="telefono_${index}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                          </div>
                          <div class="row">
                              <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Celular</label></div>
                              <div class="col"><input class="form-control" type="text" name="celular_static[]" value="${contacto.celular}" id="celular_${index}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                          </div>
                          <div class="row">
                              <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Email</label></div>
                              <div class="col"><input class="form-control" type="email" name="email_static[]" value="${contacto.email}" id="email_${index}" style="border-color: rgb(159,168,175); font-size: 12px;" disabled></div>
                          </div>
                      </div>
                      `;
  
                      $('#cont').append(contactoElemento);
  
                      // Evento para habilitar la edición
                      $(`#editar_contacto_${index}`).on('click', function() {
                        $(`#nombre_${index}`).prop('disabled', false);
                        $(`#apellido_${index}`).prop('disabled', false);
                        $(`#telefono_${index}`).prop('disabled', false);
                        $(`#celular_${index}`).prop('disabled', false);
                        $(`#email_${index}`).prop('disabled', false);
  
                        $(`#nombre_${index}`).attr('name', 'nombre[]');
                        $(`#apellido_${index}`).attr('name', 'apellido[]');
                        $(`#telefono_${index}`).attr('name', 'telefono[]');
                        $(`#celular_${index}`).attr('name', 'celular[]');
                        $(`#email_${index}`).attr('name', 'email[]');
                        $(`#contacto_id_${index}`).attr('name', 'contacto_id[]');
                      });
  
                      // Evento para eliminar con confirmación
                      $(`#eliminar_contacto_${index}`).on('click', function() {
                          if (confirm('¿Estás seguro que deseas eliminar este contacto?')) {
                              $(this).closest('.col-sm-5').remove();
                          }
                      });
                  });
              } else {
                  $('#cont').html('<p>No hay contactos disponibles para este cliente.</p>');
              }
          },
          error: function(xhr, status, error) {
              $('#cont').html('<p>Error al cargar contactos.</p>');
          }
      });
  } else {
      $('#cont').html('<p>No se ha seleccionado un cliente.</p>');
  }
}


// Función para cargar direcciones
function cargarDirecciones() {
  console.log("Encargado de ejecutar direcciones...");
  const clienteRut = $('#rutSN').attr('data-rut');
  console.log("Valor de clienteRut para direcciones:", clienteRut);

  if (clienteRut && clienteRut.trim() !== "") {
      $.ajax({
          url: '/ventas/buscar_clientes/',
          data: { 'numero': clienteRut },
          dataType: 'json',
          success: function(data) {
              $('#dir').empty(); // Limpiar el contenido previo

              if (data.resultadosClientes && data.resultadosClientes.length > 0) {
                  const cliente = data.resultadosClientes[0];
                  const direcciones = cliente.direcciones || [];

                  direcciones.forEach((direccion, index) => {
                      console.log("tipoDireccion", direccion.tipoDireccion);
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

                              <input type="hidden" name="direccionid[]" value="${direccion.id}" id="contacto_id_${index}">

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
                                        <option value="15" ${direccion.region_numero === 15 ? "selected" : ""}>Arica y Parinacota</option>
                                        <option value="1" ${direccion.region_numero === 1 ? "selected" : ""}>Tarapacá</option>
                                        <option value="2" ${direccion.region_numero === 2 ? "selected" : ""}>Antofagasta</option>
                                        <option value="3" ${direccion.region_numero === 3 ? "selected" : ""}>Atacama</option>
                                        <option value="4" ${direccion.region_numero === 4 ? "selected" : ""}>Coquimbo</option>
                                        <option value="5" ${direccion.region_numero === 5 ? "selected" : ""}>Valparaíso</option>
                                        <option value="13" ${direccion.region_numero === 13 ? "selected" : ""}>Metropolitana de Santiago</option>
                                        <option value="6" ${direccion.region_numero === 6 ? "selected" : ""}>Libertador General Bernardo O'Higgins</option>
                                        <option value="7" ${direccion.region_numero === 7 ? "selected" : ""}>Maule</option>
                                        <option value="16" ${direccion.region_numero === 16 ? "selected" : ""}>Ñuble</option>
                                        <option value="8" ${direccion.region_numero === 8 ? "selected" : ""}>Biobío</option>
                                        <option value="9" ${direccion.region_numero === 9 ? "selected" : ""}>La Araucanía</option>
                                        <option value="14" ${direccion.region_numero === 14 ? "selected" : ""}>Los Ríos</option>
                                        <option value="10" ${direccion.region_numero === 10 ? "selected" : ""}>Los Lagos</option>
                                        <option value="11" ${direccion.region_numero === 11 ? "selected" : ""}>Aysén del General Carlos Ibáñez del Campo</option>
                                        <option value="12" ${direccion.region_numero === 12 ? "selected" : ""}>Magallanes y de la Antártica Chilena</option>
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


                      $('#dir').append(direccionElemento);

                      const regionSelect = $(`#region_${index}`);
                      const comunaSelect = $(`#comuna_${index}`);
                      cargarComunas(direccion.region_numero, comunaSelect, direccion.comuna_codigo);


                      $(document).on('click', `#editar_dir_${index}`, function() {
                          //console.log("Habilitando edición para la dirección con index:", index);
                          
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
                      
                          //console.log("Edición habilitada para la dirección con index:", index);
                      });
                      

                        $(`#eliminar_dir_${index}`).on('click', function() {
                          if (confirm('¿Estás seguro que deseas eliminar esta direccion?')) {
                              $(this).closest('.col-sm-5').remove();
                          }
                      });
                      
                    });
              } else {
                  $('#dir').html('<p>No hay direcciones disponibles para este cliente.</p>');
              }
          },
          error: function(xhr, status, error) {
              $('#dir').html('<p>Error al cargar direcciones.</p>');
          }
      });
  } else {
      $('#dir').html('<p>No se ha seleccionado un cliente.</p>');
  }
}

// Función para inicializar región y comunas al cargar la página
function inicializarRegionYComuna(direccion, index) {
  const regionSelect = $(`#region_${index}`); // Selector del campo de región
  const comunaSelect = $(`#comuna_${index}`); // Selector del campo de comuna

  // Seleccionar la región
  regionSelect.val(direccion.region_numero).trigger('change'); // Dispara el evento change para cargar comunas

  // Cargar las comunas y seleccionar la correspondiente
  cargarComunas(direccion.region_numero, comunaSelect, direccion.comuna_codigo);
}

// Evento para cuando cambia la región (ya implementado)
$(document).on('change', '[id^="region_"]', function () {
  const regionId = $(this).val(); // Obtener el valor de la región seleccionada
  const index = $(this).attr('id').split('_')[1]; // Extraer el índice dinámico del ID
  const comunaSelect = $(`#comuna_${index}`); // Seleccionar el select de comuna correspondiente

  //console.log("Región seleccionada:", regionId);
  //console.log("Index detectado:", index);
  //console.log("Select de comunas encontrado:", comunaSelect);

  if (regionId) {
    cargarComunas(regionId, comunaSelect); // Llamar a la función para cargar comunas
  } else {
    $(comunaSelect).empty().append('<option value="">Seleccione una comuna</option>'); // Limpiar si no hay región seleccionada
  }
});

// Función para cargar comunas y seleccionar la correspondiente
function cargarComunas(regionId, comunaSelect, comunaSeleccionada = null) {
  //console.log("Cargando comunas para la región con ID:", regionId);

  $.ajax({
    url: `/ventas/obtener_comunas_por_region/?idRegion=${regionId}`, // Asegúrate de que esta ruta sea la correcta
    method: 'GET',
    success: function (data) {
      console.log("Datos recibidos del servidor:", data);
      $(comunaSelect).empty();
      $(comunaSelect).append('<option value="">Seleccione una comuna</option>');

      // Rellenar el select con las comunas obtenidas
      data.forEach(function (comuna) {
        let selected = comunaSeleccionada && comunaSeleccionada === comuna.codigo ? "selected" : "";
        $(comunaSelect).append(`<option value="${comuna.codigo}" ${selected}>${comuna.nombre}</option>`);
      });

      //console.log("Select de comunas actualizado.");
    },
    error: function (xhr, status, error) {
      console.error("Error al cargar comunas:", error);
      $(comunaSelect).empty().append('<option value="">Error al cargar comunas</option>');
    }
  });
}
