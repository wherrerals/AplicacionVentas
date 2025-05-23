// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function() {
// Obtiene una referencia al botón para agregar contacto
let btnAgregarContacto = document.getElementById("btnAgregarContacto");
btnAgregarContacto.addEventListener("click", function() {
      // Crea el modal
      let modalHtml = `
      <div class="modal fade" role="dialog" tabindex="-1" id="contactoModal"aria-labelledby="contactoModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content" style="width: 200%;" >
            <div class="modal-header">
              <h1 class="fs-5 modal-title" id="exampleModalLabel-2">Agregar Contacto</h1><button
                class="btn-close" type="button" aria-label="Close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" style="padding: 9px;">
              <div class="row" style="margin-right: 0px;margin-left: 0px;width: 490px;">
                <div class="col-sm-12" style="width: 100%;"><a class="navbar-brand d-flex align-items-center"
                    href="lista_cotizaciones.html" style="width: 107px;"><svg
                      xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor"
                      viewBox="0 0 16 16" class="bi bi-person-fill-add" style="font-size: 45px;">
                      <path
                        d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0m-2-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0">
                      </path>
                      <path
                        d="M2 13c0 1 1 1 1 1h5.256A4.493 4.493 0 0 1 8 12.5a4.49 4.49 0 0 1 1.544-3.393C9.077 9.038 8.564 9 8 9c-5 0-6 3-6 4">
                      </path>
                    </svg></a></div>
                <div class="col-sm-12" style="width: 100%;height: 10px;"><span>&nbsp;</span></div>

                <div class="col-sm-5" style="font-size: 12px;background: #f0f2f5;width: 230px;">
                  <div class="row">
                    <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span>
                    </div>
                    <div class="col" style="text-align: center;"><span style="font-weight: bold;">Contacto Nº
                        1</span></div>
                    <div class="col-sm-12" style="height: 5px;background: transparent;"><span>&nbsp;</span>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-sm-9"><span></span></div>
                    <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;"><a
                        class="navbar-brand d-flex align-items-center" href="lista_cotizaciones.html"
                        style="width: 32px;"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
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
                        class="navbar-brand d-flex align-items-center" href="lista_cotizaciones.html"
                        style="width: 32px;"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
                          fill="currentColor" viewBox="0 0 16 16" class="bi bi-backspace"
                          style="font-size: 24px;">
                          <path
                            d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z">
                          </path>
                          <path
                            d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z">
                          </path>
                        </svg></a></div>
                    <div class="col-sm-12" style="height: 10px;background: transparent;"><span>&nbsp;</span>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-sm-4">
                      <label class="col-form-label" style="font-size: 13px;">Nombre</label>
                    </div>
                    <div class="col">
                      <input class="form-control" type="text" name="nombreDireccion" style="border-color: rgb(159,168,175);font-size: 12px;">
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-sm-4">
                      <label class="col-form-label" style="font-size: 13px;">Apellido</label>
                    </div>
                    <div class="col"><input class="form-control" type="text" name="pais"
                        style="border-color: rgb(159,168,175);font-size: 12px;"></div>
                  </div>
                  <div class="row">
                    <div class="col-sm-4"><label class="col-form-label"
                        style="font-size: 13px;">Teléfono</label></div>
                    <div class="col"><input class="form-control" type="tel"
                        style="font-size: 12px;border-color: rgb(159,168,175);"></div>
                  </div>
                  <div class="row">
                    <div class="col-sm-4"><label class="col-form-label"
                        style="font-size: 13px;">Celular</label></div>
                    <div class="col"><input class="form-control" type="tel"
                        style="font-size: 12px;border-color: rgb(159,168,175);"></div>
                  </div>
                  <div class="row">
                    <div class="col-sm-4"><label class="col-form-label" style="font-size: 13px;">Email</label>
                    </div>
                    <div class="col"><input class="form-control" type="email"
                        style="font-size: 12px;border-color: rgb(159,168,175);"></div>
                  </div>
                  <div class="row">
                    <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span>
                    </div>
                    <div class="col-sm-12" style="height: 15px;background: var(--bs-body-bg);">
                      <span>&nbsp;</span>
                    </div>
                  </div>
                </div>

                <div class="col-sm-1" style="padding: 0px;width: 20px;"><span></span></div>
      
                <div class="col-sm-1" style="padding: 0px;width: 20px;"><span></span></div>
              </div>
            </div>
            <div class="modal-footer"><button class="btn btn-secondary" type="button"
                data-bs-dismiss="modal">Cerrar</button><button class="btn btn-primary"
                type="button">Grabar</button></div>
          </div>
        </div>
      </div>
    </div>
      `;

      // Crea un elemento div para contener el modal generado
      let modalContainer = document.createElement("div");
      // Agrega el HTML del modal al contenedor
      modalContainer.innerHTML = modalHtml;

      // Inserta el modal en el DOM
      document.getElementById("modalContainer").appendChild(modalContainer);

      // Muestra el modal
      let modalElement = modalContainer.querySelector(".modal");
      let modal = new bootstrap.Modal(modalElement);
      modal.show();
    });
  });