// Ensure CSRF token is available
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

document.getElementById('forCrearCliente').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const submitButton = document.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    fetch('/ventas/agregar_editar_clientes/', {
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

    // Usar clases de Bootstrap para los mensajes
    div.className = `mensaje alert alert-${tipo === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    div.setAttribute('role', 'alert');
    div.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    

    contenedorMensajes.appendChild(div);

    // Eliminar automáticamente el mensaje después de 5 segundos
    setTimeout(() => {
        div.classList.remove('show');  // Desvanecer el mensaje
        setTimeout(() => div.remove(), 150);  // Luego removerlo del DOM
    }, 5000);
}

