document.addEventListener("DOMContentLoaded", function () {
    // Función para obtener el valor de un parámetro de la URL
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    // Obtén el RUT de la URL
    const rut = getQueryParam('rut');

    if (rut) {
        // Realiza la solicitud AJAX para obtener la información del cliente
        fetch(`/ventas/informacion_cliente/?rut=${rut}`)
            .then(response => {
                if (!response.ok) throw new Error('Error al obtener la información del cliente');
                return response.json();
            })
            .then(data => {
                console.log('Información del cliente:', data);

                // Muestra los datos en los campos del formulario
                document.getElementById("nombreSN").value = data[0].nombre || '';
                document.getElementById("apellidoSN").value = data[0].apellido || '';
                document.getElementById("rutSN").value = data[0].rut || '';
                document.getElementById("giroSN").value = data[0].giro || '';
                document.getElementById("telefonoSN").value = data[0].telefono || '';
                document.getElementById("emailSN").value = data[0].email || '';

                
                document.getElementById("rutSN").readOnly = true;
            })
            .catch(error => {
                console.error('Error en la solicitud AJAX:', error);
            });
    } else {
        console.error("No se proporcionó un RUT en la URL");
    }
});
