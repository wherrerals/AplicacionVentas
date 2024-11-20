document.addEventListener("DOMContentLoaded", function () {
  const cotizacionLink = document.getElementById("cotizacionLink");
  const rutInput = document.getElementById("rutSN");

  if (cotizacionLink && rutInput) {
    cotizacionLink.addEventListener("click", function (event) {
      event.preventDefault(); // Evita la redirección predeterminada

      // Capturar valores de los inputs
      let rutSN = rutInput.value.trim();
      const grupoSN = document.querySelector('input[name="grupoSN"]:checked').value;
      const nombreSN = document.getElementById("nombreSN").value.trim();
      const apellidoSN = document.getElementById("apellidoSN").value.trim();
      const giroSN = document.getElementById("giroSN").value.trim();
      const telefonoSN = document.getElementById("telefonoSN").value.trim();
      const emailSN = document.getElementById("emailSN").value.trim();

      // Validar si el RUT está vacío
      if (!rutSN) {
        alert("El RUT no puede estar vacío.");
        return;
      }

      // Redirigir con los datos como parámetros en la URL
      const url = `/ventas/generar_cotizacion/?rutSN=${encodeURIComponent(rutSN)}&grupoSN=${encodeURIComponent(grupoSN)}&nombreSN=${encodeURIComponent(nombreSN)}&apellidoSN=${encodeURIComponent(apellidoSN)}&giroSN=${encodeURIComponent(giroSN)}&telefonoSN=${encodeURIComponent(telefonoSN)}&emailSN=${encodeURIComponent(emailSN)}`;
      console.log("Redirigiendo a URL:", url);
      window.location.href = url;
    });
  } else {
    alert("No se encontraron los elementos necesarios para la redirección.");
  }
});
