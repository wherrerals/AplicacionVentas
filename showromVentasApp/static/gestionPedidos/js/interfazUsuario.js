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

// Oculta el botón de acciones si no hay número de cotización y deshabilita campos relacionados
document.addEventListener('DOMContentLoaded', function () {
  const numeroCotizacion = document.getElementById('numero_cotizacion');
  const botonAcciones = document.querySelector('.btn.btn-primary.dropdown-toggle');

  // Campos que se deben deshabilitar
  const camposADeshabilitar = [
      document.getElementById('inputCliente'),
      document.getElementById('contactos_cliete'),
      document.getElementById('direcciones_despacho'),
      document.getElementById('tipoEntrega-1'),
      document.getElementById('direcciones_facturacion')
  ];

  function checkNumeroCotizacion() {
      const tieneTexto = numeroCotizacion.textContent.trim() !== '';

      // Ocultar o mostrar el botón de acciones
      botonAcciones.style.display = tieneTexto ? 'inline-block' : 'none';

      // Deshabilitar o habilitar campos
      camposADeshabilitar.forEach(campo => {
          if (campo) {
              campo.disabled = tieneTexto;
          }
      });
  }

  // Verificar el estado inicial
  checkNumeroCotizacion();

  // Observar cambios en el contenido del número de cotización
  const observer = new MutationObserver(checkNumeroCotizacion);
  observer.observe(numeroCotizacion, { childList: true, subtree: true });
});
