// Ensure CSRF token is available
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

document.getElementById('forCrearCliente').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const submitButton = document.querySelector('button[type="submit"]');
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
            hideLoadingOverlay();

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
            // Capturar el RUT directamente desde el campo #rutSN
            const rutSNInput = document.getElementById('rutSN');
            const rutCliente = rutSNInput.value;

            if (rutCliente) {
                // Actualizar el valor en el #inputCliente
                const inputCliente = document.getElementById('inputCliente');
                inputCliente.value = rutCliente;
                console.log('Nuevo valor en inputCliente:', rutCliente);

                // Ejecutar la búsqueda con el RUT
                $('#resultadosClientes').empty(); // Vacía el contenedor de resultados
                traerInformacionCliente(rutCliente);
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

                const modalElement = document.getElementById('clienteModal'); // ID de tu modal
                const modalInstance = bootstrap.Modal.getInstance(modalElement);
                if (modalInstance) {
                    modalInstance.hide();
                }
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
    // Buscar los contenedores donde se mostrarán los mensajes
    const contenedorMensajes1 = document.getElementById('contenedor-mensajes') || document.body;
    const contenedorMensajes3 = document.getElementById('contenedor-mensajes-3') || document.body;

    // Crear el mensaje
    const div = document.createElement('div');

    // Usar clases de Bootstrap para los mensajes
    div.className = `mensaje alert alert-${tipo === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    div.setAttribute('role', 'alert');
    div.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Agregar el mensaje al contenedor principal
    contenedorMensajes1.appendChild(div);

    // Si existe el contenedor adicional, clonar el mensaje y agregarlo
    if (contenedorMensajes3 !== document.body) {
        const divClone = div.cloneNode(true);
        contenedorMensajes3.appendChild(divClone);

        // Programar eliminación del mensaje clonado
        setTimeout(() => {
            divClone.classList.remove('show');  // Desvanecer el mensaje
            setTimeout(() => divClone.remove(), 150);  // Removerlo del DOM
        }, 5000);
    }

    // Programar eliminación del mensaje original
    setTimeout(() => {
        div.classList.remove('show');  // Desvanecer el mensaje
        setTimeout(() => div.remove(), 150);  // Removerlo del DOM
    }, 5000);
}

