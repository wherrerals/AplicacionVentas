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
  
      let fechaFormateada = dia + '-' + mes + '-' + año;
  
      let diasVencidosLabel = document.getElementById('docDueDate');
      if (diasVencidosLabel) {
        diasVencidosLabel.textContent = fechaFormateada;
      } else {
        console.error('Elemento con ID "docDueDate" no encontrado.');
      }
    }
  
    sumarTresDias();
  });
  