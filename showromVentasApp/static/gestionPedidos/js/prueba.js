document.getElementById('forCrearPedidos').addEventListener('submit', function(event) {
        event.preventDefault();
    
        // Obtener los datos del formulario
        const formData = new FormData(this);
    
        fetch('/ventas/agregar_editar_clientes/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: formData
        })
        .then(response => {
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
                // Aquí puedes redirigir o actualizar la página si es necesario
                // window.location.href = '/ruta-exitosa/';
            }
        })
        .catch(error => {
            mostrarMensaje(error.message, 'error');
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
    }
    