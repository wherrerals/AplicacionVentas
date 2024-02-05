$(document).ready(function () {
    $('CuentaForm').submit(function (event) {
      event.preventDefault();
  
      // Serializa los datos del formulario
      var formData = $(this).serialize();
  
      // Realiza una solicitud AJAX a la vista de Django
      $.ajax({
        type: 'POST',
        url: '/',
        data: formData,
        success: function (response) {
          // Oculta el formulario
          $('CuentaForm').hide();
  
          // Muestra el mensaje de éxito
          $('#mensajeExito').show();
        },
        error: function (error) {
          // Maneja errores si es necesario
          console.error('Error en la solicitud AJAX:', error);
        }
      });
    });
  });
  