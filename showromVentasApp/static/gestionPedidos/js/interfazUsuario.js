document.addEventListener('DOMContentLoaded', function() {
    function formatNumber(num) {
      return num < 10 ? '0' + num : num;
    }
  
    function sumarTresDias() {
      let hoy = new Date();
      let tresDiasDespues = new Date(hoy.getTime() + (3 * 24 * 60 * 60 * 1000));
  
      let dia = formatNumber(tresDiasDespues.getDate());
      let mes = formatNumber(tresDiasDespues.getMonth() + 1);
      let año = tresDiasDespues.getFullYear();
  
      let fechaFormateada = año + '-' + mes + '-' + dia;
  
      let diasVencidosLabel = document.getElementById('docDueDate');
      if (diasVencidosLabel) {
        diasVencidosLabel.textContent = fechaFormateada;
      } else {
        //console.error('Elemento con ID "docDueDate" no encontrado.');
      }
    }
  
    sumarTresDias();
  });
  

  //Oculta el boton de acciones si no hay numero de cotizacion
  document.addEventListener('DOMContentLoaded', function () {
    const numeroCotizacion = document.getElementById('numero_cotizacion');
    const botonAcciones = document.querySelector('.btn.btn-primary.dropdown-toggle');


    function checkNumeroCotizacion() {
        if (!numeroCotizacion.textContent.trim()) {
            botonAcciones.style.display = 'none'; 
        } else {
            botonAcciones.style.display = 'inline-block';
        }
    }

    checkNumeroCotizacion();

    const observer = new MutationObserver(checkNumeroCotizacion);
    observer.observe(numeroCotizacion, { childList: true, subtree: true });
});
