class DireccionManager {
    constructor() {
      this.contdir = 0;
      this.init();
    }
  
    // Inicializa los eventos y configuraciones
    init() {
      window.addEventListener('DOMContentLoaded', () => {
        const botonAgregarDirecciones = document.getElementById('agregar_dir');
        if (botonAgregarDirecciones) {
          botonAgregarDirecciones.addEventListener('click', () => this.agregarDireccion());
        }
      });
    }
  
    // Agrega una nueva dirección
    agregarDireccion() {
      const newRow = document.createElement('div');
      this.contdir++;
      newRow.className = "col-sm-1";
      newRow.style = "padding: 0px;width: 280px";
  
      newRow.innerHTML = `
        <div class="col-sm-12" style="width: 100%;height: 10px;"><span>&nbsp;</span></div>
        <div class="col-sm-5" style="font-size: 12px;background: #f0f2f5;width: 250px;">
          <div class="row">
            <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span></div>
            <div class="col" style="text-align: center;">
              <span style="font-weight: bold;">Dirección Nº ${this.contdir}</span></div>
            <div class="col-sm-12" style="height: 5px;background: transparent;"><span>&nbsp;</span></div>
          </div>
  
          <div class="row">
            <div class="col-sm-9"><span></span></div>
            <div class="col-sm-1" style="padding-right: 10px;padding-left: 0px;">
              <a class="navbar-brand d-flex align-items-center" href="lista_cotizaciones.html" style="width: 32px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-pencil-square" style="font-size: 24px;">
                  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"></path>
                  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"></path>
                </svg>
              </a>
            </div>
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
              <label class="col-form-label" style="font-size: 13px;">Nombre Dirección</label> 
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
              <label class="col-form-label" style="font-size: 13px;">Dirección</label>
            </div>
            <div class="col">
              <input class="form-control" type="text" name="direccion[]" id="direccion" style="border-color: rgb(159,168,175);font-size: 12px;">
            </div>
          </div>

          <div class="row">
            <div class="col-sm-12" style="height: 15px;background: transparent;"><span>&nbsp;</span></div>
          </div>
        </div>
        <div class="col-sm-1" style="padding: 0px;width: 20px;"><span></span></div>
      `;
  
      const tab1 = document.getElementById('dir');
      tab1.style.display = "flex";
      tab1.style.flexDirection = "row";
      tab1.style.overflowX = "auto";
      tab1.style.maxWidth = "100%";
  
      tab1.appendChild(newRow);
      newRow.querySelector('#eliminar_dir').addEventListener('click', () => newRow.remove());
    }
  }
  
  // Crear una instancia de DireccionManager al cargar la página
  document.addEventListener('DOMContentLoaded', () => new DireccionManager());
  