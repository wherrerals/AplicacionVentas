document.addEventListener("DOMContentLoaded", function () {
  const cotizacionLink = document.getElementById("cotizacionLink");
  const rutInput = document.getElementById("rutSN");

  if (cotizacionLink && rutInput) {
    cotizacionLink.addEventListener("click", function (event) {
      event.preventDefault(); // Evita la redirección predeterminada

      // Capturar valores de los inputs
      let rutSN = rutInput.value.trim() || ""; // Si está vacío, se asigna una cadena vacía
      const grupoSN = document.querySelector('input[name="grupoSN"]:checked')?.value || "";
      const nombreSN = document.getElementById("nombreSN")?.value.trim() || "";
      const apellidoSN = document.getElementById("apellidoSN")?.value.trim() || "";
      const giroSN = document.getElementById("giroSN")?.value.trim() || "";
      const telefonoSN = document.getElementById("telefonoSN")?.value.trim() || "";
      const emailSN = document.getElementById("emailSN")?.value.trim() || "";

      // Redirigir con los datos como parámetros en la URL
      const url = `/ventas/generar_cotizacion/?rutSN=${encodeURIComponent(rutSN)}&grupoSN=${encodeURIComponent(grupoSN)}&nombreSN=${encodeURIComponent(nombreSN)}&apellidoSN=${encodeURIComponent(apellidoSN)}&giroSN=${encodeURIComponent(giroSN)}&telefonoSN=${encodeURIComponent(telefonoSN)}&emailSN=${encodeURIComponent(emailSN)}`;
      console.log("Redirigiendo a URL:", url);
      window.location.href = url;
    });
  } else {
    // Redirigir sin parámetros si los elementos necesarios no existen
    console.warn("No se encontraron los elementos necesarios para la redirección.");
    window.location.href = "/ventas/generar_cotizacion/";
  }
});
