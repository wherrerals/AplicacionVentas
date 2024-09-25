document.getElementById('forCrearPedidos').addEventListener('submit', function(event) {
    event.preventDefault();

    // Obtener los datos del formulario
    const formData = new FormData(this);

    // Deshabilitar el botón de envío mientras se procesa la solicitud
    const submitButton = this.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    fetch('/ventas/agregar_editar_clientes/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: formData
    })
    .then(response => {
        // Habilitar el botón nuevamente después de la respuesta
        submitButton.disabled = false;

        if (!response.ok) {
            // Manejar errores del servidor
            return response.json().then(data => {
                throw new Error(data.error || 'Error desconocido');
            });
        }
        return response.json();
    })
    .then(data => {
        // Limpiar mensajes previos
        limpiarMensajes();

        if (data.error) {
            mostrarMensaje(data.error, 'error');
        } else {
            mostrarMensaje(data.success || 'Operación exitosa', 'success');
            // Redirigir o actualizar la página si es necesario
            // window.location.href = '/ruta-exitosa/';
        }
    })
    .catch(error => {
        // Habilitar el botón en caso de error
        submitButton.disabled = false;
        console.error('Error en la solicitud:', error);
        mostrarMensaje(error.message || 'Ocurrió un error desconocido', 'error');
    });
});

function limpiarMensajes() {
    const mensajes = document.getElementsByClassName('mensaje');
    while (mensajes[0]) {
        mensajes[0].parentNode.removeChild(mensajes[0]);
    }
}

function mostrarMensaje(mensaje, tipo) {
    const div = document.createElement('div');
    div.className = `mensaje ${tipo}`;
    div.textContent = mensaje;
    document.body.appendChild(div);

    // Hacer que el mensaje desaparezca después de 5 segundos
    setTimeout(() => {
        div.remove();
    }, 5000);
}

    