function duplicarCotizacion() {
    // Obtener el elemento de la cotización a duplicar (ajusta el selector según tu estructura HTML)
    var cotizacion = document.getElementById("forCrearPedidos");

    // Clonar el elemento
    var nuevaCotizacion = cotizacion.cloneNode(true);

    // Limpiar los datos del cliente (ajusta los selectores según tu estructura HTML)
    nuevaCotizacion.querySelector("#inputCliente").value = "";
    // ... otros campos a limpiar

    // Insertar la nueva cotización después de la original (ajusta según tu estructura HTML)
    cotizacion.parentNode.insertBefore(nuevaCotizacion, cotizacion.nextSibling);
}