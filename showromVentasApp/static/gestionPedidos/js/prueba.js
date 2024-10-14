// Ensure CSRF token is available
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

document.getElementById('forCrearPedidos').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const submitButton = this.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    fetch('/ventas/agregar_editar_clientes/', {  // Verifica que esta ruta coincida con la vista del backend
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => {
        submitButton.disabled = false;
        
        if (!response.ok) {
            if (response.status === 400) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Error en los datos enviados');
                });
            } else if (response.status === 500) {
                throw new Error('Error interno del servidor');
            } else {
                throw new Error('Error desconocido');
            }
        }
        return response.json();
    })
    .then(data => {
        limpiarMensajes();

        if (data.success === false || data.error) {
            mostrarMensaje(data.error || data.message || 'Ocurrió un error', 'error');
        } else {
            mostrarMensaje(data.message || 'Operación exitosa', 'success');
            
            // Descomenta la siguiente línea si quieres redirigir después de la creación exitosa
            // window.location.href = '/ruta-exitosa/';
        }
    })
    .catch(error => {
        submitButton.disabled = false;
        console.error('Error en la solicitud:', error);
        mostrarMensaje(error.message || 'Ocurrió un error desconocido', 'error');
    });
});

function limpiarMensajes() {
    const mensajes = Array.from(document.querySelectorAll('.mensaje'));
    mensajes.forEach(mensaje => mensaje.remove());
}

function mostrarMensaje(mensaje, tipo) {
    const contenedorMensajes = document.getElementById('contenedor-mensajes') || document.body;
    const div = document.createElement('div');
    div.className = `mensaje ${tipo}`;
    div.textContent = mensaje;
    contenedorMensajes.appendChild(div);

    setTimeout(() => {
        div.remove();
    }, 5000);
}

