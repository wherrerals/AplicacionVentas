document.addEventListener("DOMContentLoaded", function () {
    const cotizacionLink = document.getElementById("ordeveVentaLink");
    const filtroCotizacionLink = document.getElementById("FiltroOrdenVentaLink");
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
        const url = `/ventas/ordenesVentas/?rutSN=${encodeURIComponent(rutSN)}&grupoSN=${encodeURIComponent(grupoSN)}&nombreSN=${encodeURIComponent(nombreSN)}&apellidoSN=${encodeURIComponent(apellidoSN)}&giroSN=${encodeURIComponent(giroSN)}&telefonoSN=${encodeURIComponent(telefonoSN)}&emailSN=${encodeURIComponent(emailSN)}`;
        console.log("Redirigiendo a URL:", url);
        window.location.href = url;
      });
    }
  
    if (filtroCotizacionLink && rutInput) {
      filtroCotizacionLink.addEventListener("click", function (event) {
        event.preventDefault(); // Evita la redirección predeterminada
  
        // Capturar valores de los inputs
        let rutSN = rutInput.value.trim() || ""; // Si está vacío, se asigna una cadena vacía
        const nombreSN = document.getElementById("nombreSN")?.value.trim() || "";
        const apellidoSN = document.getElementById("apellidoSN")?.value.trim() || "";
        const nombreBuscar = nombreSN + " " + apellidoSN;
  
        // Redirigir con los datos como parámetros en la URL
        const url = `/ventas/lista_ovs/?rutSN=${encodeURIComponent(rutSN)}&nombreSN=${encodeURIComponent(nombreBuscar)}`;
        console.log("Redirigiendo a URL:", url);
        window.location.href = url;
      });
    }
  });
  