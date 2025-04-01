class ContactoManager {
  constructor() {
    this.contcon = 0; // Inicializamos el contador
    this.initializeEvents();
  }


    initializeEvents() {
        // Verificar si el elemento 'agregar_cont' existe antes de agregar el evento
        const agregarCont = document.getElementById('agregar_cont');
        if (agregarCont) {
            agregarCont.addEventListener('click', () => this.agregarContacto('cont'));
            console.log('Evento de agregar contacto inicializado.');
        }

        // Verificar si el elemento 'agregar_cont_modal' existe antes de agregar el evento
        const agregarContModal = document.getElementById('agregar_cont_modal');
        if (agregarContModal) {
            agregarContModal.addEventListener('click', () => this.agregarContacto('listaContactos'));
        }
    }

  agregarContacto(containerId) {
    this.contcon++;  // Incrementa el contador cada vez que se agrega un nuevo contacto

    // Crear una nueva fila para el contacto
    let newRow = document.createElement('div');
    newRow.className = "col-sm-5 contactos";
    newRow.style = "font-size: 12px;background: #f0f2f5;width: 230px; margin-right: 10px;";
    newRow.innerHTML = `
        <div class="row">
            <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span></div>
            <div class="col" style="text-align: center;">
                <span style="font-weight: bold;">Contacto Nº ${this.contcon}</span>
            </div>
            <div class="col-sm-12" style="height: 5px;background: transparent;"><span>&nbsp;</span></div>
        </div>
        
        <div class="row">
          <div class="col-sm-8"><span></span></div>
          <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;"> </div>
          <div class="col-sm-1" style="padding-right: 0px;padding-left: 10px;">
            <a class="navbar-brand d-flex align-items-center" style="width: 32px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-backspace" style="font-size: 24px;" id="eliminar_contacto">
                <path d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z"></path>
                <path d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"></path>
              </svg>
            </a>
          </div>
          <div class="col-sm-12" style="height: 10px;background: transparent;"><span>&nbsp;</span></div>
        </div>

        <div class="row">
            <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Nombre</label></div>
            <div class="col"><input class="form-control" id="nombreContacto" type="text" name="nombre[]" style="border-color: rgb(159,168,175);font-size: 12px;"></div>
        </div>
        <div class="row">
            <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Apellido</label></div>
            <div class="col"><input class="form-control" id="apellidoContacto" type="text" name="apellido[]" style="border-color: rgb(159,168,175);font-size: 12px;"></div>
        </div>
        <div class="row">
            <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Teléfono</label></div>
            <div class="col"><input class="form-control" id="telefonoContacto" type="tel" name="telefono[]" value="+56" style="font-size: 12px;border-color: rgb(159,168,175);"></div>
        </div>
        <div class="row">
            <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Celular</label></div>
            <div class="col"><input class="form-control" id="celularContacto" name="celular[]" value="+56" type="tel" style="font-size: 12px;border-color: rgb(159,168,175);"></div>
        </div>
        <div class="row">
            <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Email</label></div>
            <div class="col"><input class="form-control" id="emailContacto" type="email" name="email[]" style="font-size: 12px;border-color: rgb(159,168,175);"></div>
        </div>
    `;

    // Agregar la nueva fila al contenedor indicado
    let container = document.getElementById(containerId);
    container.style.display = "flex";
    container.style.flexDirection = "row";
    container.style.overflowX = "auto"; // Permitir desplazamiento horizontal
    container.appendChild(newRow);

    // Asignar el evento de eliminación a la nueva fila
    newRow.querySelector('#eliminar_contacto').addEventListener('click', () => {
        newRow.remove();
    });
  }
}

// Inicializar el gestor de contactos
const contactoManager = new ContactoManager();

$(document).ready(function() {
  $('#contactoModal').on('show.bs.modal', function() {
      let clienteRut = $('#inputCliente').attr('data-rut');
      if (clienteRut) {
          $.ajax({
              url: '/ventas/buscar_clientes/',
              data: { 'numero': clienteRut },
              dataType: 'json',
              success: function(data) {
                  $('#listaContactos').empty(); // Limpiar la lista de contactos anteriores

                  if (data.resultadosClientes && data.resultadosClientes.length > 0) {
                      const cliente = data.resultadosClientes[0];
                      const contactos = cliente.contactos;
                      console.log('contacto de Cliente encontrado: ', contactos);

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

                              <input type="hidden" name="contacto_id[]" data-bpcode="${contacto.codigoInternoSap}" value="${contacto.id}" id="contacto_id_${index}">


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

                          $('#listaContactos').append(contactoElemento);

                          // Cambiar los nombres de los campos para capturar solo si han sido modificados
                          $(`#nombre_${index}`).attr('name', 'nombre[]');
                          $(`#apellido_${index}`).attr('name', 'apellido[]');
                          $(`#telefono_${index}`).attr('name', 'telefono[]');
                          $(`#celular_${index}`).attr('name', 'celular[]');
                          $(`#email_${index}`).attr('name', 'email[]');
                          $(`#contacto_id_${index}`).attr('name', 'contacto_id[]');
                          
                          // Evento para habilitar la edición
                          $(`#editar_contacto_${index}`).on('click', function() {
                            // Hacer los campos editables
                            $(`#nombre_${index}`).prop('disabled', false);
                            $(`#apellido_${index}`).prop('disabled', false);
                            $(`#telefono_${index}`).prop('disabled', false);
                            $(`#celular_${index}`).prop('disabled', false);
                            $(`#email_${index}`).prop('disabled', false);
                        
                            // Cambiar el nombre para capturar solo si han sido modificados

                        });

                          // Evento para eliminar con confirmación
                          $(`#eliminar_contacto_${index}`).on('click', function() {
                              if (confirm('¿Estás seguro que deseas eliminar este contacto?')) {
                                  $(this).closest('.col-sm-5').remove();
                              }
                          });
                      });

                      // Actualizar el contador según los contactos ya existentes
                      contactoManager.contcon = contactos.length;

                  } else {
                      $('#listaContactos').html('<p id="elimcontac">No hay contactos disponibles para este cliente.</p>');
                  }
              },
              error: function(xhr, status, error) {
                  $('#listaContactos').html('<p id="elimcontac">Error al cargar contactos.</p>');
              }
          });
      } else {
          $('#listaContactos').html('<p id="elimcontac">No se ha seleccionado un cliente.</p>');
      }
  });
});
