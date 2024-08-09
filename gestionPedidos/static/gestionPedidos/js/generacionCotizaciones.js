// Función para obtener el valor de un parámetro de la URL
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[[\]]/g, '\\$&');
    const regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// Función para generar un número de cotización único
function generarNumeroCotizacion() {
    let currentCotizacionNumber = localStorage.getItem('cotizacionNumber') || 0;
    currentCotizacionNumber++;
    localStorage.setItem('cotizacionNumber', currentCotizacionNumber);
    return currentCotizacionNumber;
}

// Función para mostrar el número de cotización en la página
function mostrarNumeroCotizacion() {
    const cotizacionNumero = getParameterByName('cotizacion_numero') || generarNumeroCotizacion();
    document.getElementById('numero_cotizacion').textContent = 'Nº ' + cotizacionNumero;
}

// Llamar a la función para mostrar el número de cotización al cargar la página
window.onload = mostrarNumeroCotizacion;