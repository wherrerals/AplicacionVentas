window.addEventListener('DOMContentLoaded', function() { document.getElementById('agregar_productos').addEventListener('click', function() {
    // Crear una nueva fila
    var newRow = document.createElement('table');

    // Definir el contenido de la fila
    newRow.innerHTML = `
    
      <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
        <div class="row">
          <div class="col-md-11 col-xxl-6" style="font-size: 14px;font-weight: bold;">
            <small>1)</small><small>&nbsp;&nbsp;</small><small style="font-weight: bold;">N10100256</small>
          </div>
          <div class="col-md-11 col-xxl-7" style="text-align: center;"><img src="https://ledstudiocl.vtexassets.com/arquivos/ids/166187-80-auto/label-0.jpg" width="50" height="50" style="width: 50px;height: 50px;"></div>
        </div>
      </td>
      <td style="font-size: 12px;background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
        <div class="row">
          <div class="col-sm-12 col-lg-12 col-xl-11 col-xxl-10"><select class="form-select" style="font-size: 11px;">
            <optgroup label="Bodega">
              <option value="12" selected="">GR</option>
              <option value="13">LC</option>
              <option value="14">PH</option>
              <option value="15">ME</option>
            </optgroup>
          </select></div>
          <div class="col" style="text-align: center;"><small style="font-size: 12px;">Stock: 5.314</small></div>
        </div>
      </td>
      <td style="background: transparent;border-style: none;padding-bottom: 0px;" rowspan="2">
        <div style="font-size: 12px;"><small>$1.964.900</small></div>
        <div style="font-size: 11px;"><small style="color: rgb(153,153,153);">Antes: $2.999.900</small></div>
        <div class="row" style="font-size: 11px;">
          <div class="col-sm-4 col-md-3 col-xl-2" style="padding-right: 0px;"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-arrow-right-circle-fill" style="font-size: 18px;">
            <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"></path>
          </svg></div>
          <div class="col-sm-7 col-md-8"><small style="color: rgb(255,0,0);">Max: 15%</small></div>
        </div>
      </td>
      <td style="font-size: 12px;background: transparent;border-style: none;">
        <div><input class="form-control" type="text" style="font-size: 12px;width: 40px;"></div>
      </td>
      <td style="font-size: 11px;background: transparent;font-weight: bold;border-style: none;text-align: center;">$1.964.900</td>
      <td style="font-size: 12px;background: transparent;border-style: none;"><input class="form-control" type="text" style="font-size: 12px;width: 65px;"></td>
      <td style="font-size: 11px;font-weight: bold;background: transparent;border-style: none;text-align: center;"><span>$1.964.900</span></td>
    `;
    
    // Agregar la fila a la tabla
    document.getElementById('productos').appendChild(newRow);
  });
});