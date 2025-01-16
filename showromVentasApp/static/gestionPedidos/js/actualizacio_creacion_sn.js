// Funcionalidades para la creación y actualización de clientes y pedidos en el sistema

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Obtener el token CSRF

const formularios = document.querySelectorAll('#forCrearPedidos, #forCrearCliente'); // Ajustar los IDs según el HTML

// Función para mostrar el overlay de carga
formularios.forEach(formulario => {
    formulario.addEventListener('submit', function (event) {
        event.preventDefault();

        // Obtener los datos del formulario
        const nombre = document.getElementById('nombreSN').value;
        const apellido = document.getElementById('apellidoSN').value;
        const rut = document.getElementById('rutSN').value;
        const tipo = document.querySelector('input[name="grupoSN"]:checked').value;
        const email = document.getElementById('emailSN').value;
        const telefono = document.getElementById('telefonoSN').value;
        const giro = document.getElementById('giroSN').value;
        const docentry = document.getElementById("numero_cotizacion").textContent;


        // Obtener las direcciones y contactos
        const lines = [];
        const contactos = [];

        // Obtener las filas de direcciones y contactos
        const productRows = document.querySelectorAll('.direcciones');
        productRows.forEach((row, index) => {
            const tipoDireccion = row.querySelector("#direccionSN")?.value || "";
            const nombreDireccion = row.querySelector("#nombreDireccionSN")?.value || "";
            const pais = row.querySelector("#paisSN")?.value || "";
            const region = row.querySelector("#regionSN")?.value || "";
            const comuna = row.querySelector("#comunaSN")?.value || "";
            const ciudad = row.querySelector("#ciudad")?.value || "";
            const direccion = row.querySelector("#direccion")?.value || "";

            // Crear un objeto con los datos de la fila de direcciones
            const line = {
                direccionSN: index,
                tipoDireccion: tipoDireccion,
                nombreDireccion: nombreDireccion,
                pais: pais,
                region: region,
                comuna: comuna,
                ciudad: ciudad,
                direccion: direccion
            };

            lines.push(line);
        });

        // Obtener las filas de contactos
        const contactoRows = document.querySelectorAll('.contactos');
        contactoRows.forEach((row, index) => {
            const nombreContacto = row.querySelector("#nombreContacto")?.value || "";
            const apellidoContacto = row.querySelector("#apellidoContacto")?.value || "";
            const telefonoContacto = row.querySelector("#telefonoContacto")?.value || "";
            const celularContacto = row.querySelector("#celularContacto")?.value || "";
            const emailContacto = row.querySelector("#emailContacto")?.value || "";

            // Crear un objeto con los datos de la fila de contactos
            const contactoData = {
                contactoSN: index,
                nombreContacto: nombreContacto,
                apellidoContacto: apellidoContacto,
                telefonoContacto: telefonoContacto,
                puestoContacto: celularContacto,
                emailContacto: emailContacto
            };

            contactos.push(contactoData);
        });

        // Crear un objeto con los datos del formulario
        data = {
            docentry: docentry,
            nombreSN: nombre,
            apellidoSN: apellido,
            tipoSN: tipo,
            rutSN: rut,
            emailSN: email,
            telefonoSN: telefono,
            giroSN: giro,
            direcciones: lines,
            contactos: contactos
        }

        // Convertir los datos a JSON
        dataSN = JSON.stringify(data);

        // Deshabilitar el botón de envío para evitar múltiples envíos
        const submitButton = document.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        showLoadingOverlay();

        // Enviar los datos del formulario
        fetch('/ventas/agregar_editar_clientes/', {  
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: dataSN
        })

        // Procesar la respuesta
        .then(response => {
            submitButton.disabled = false;

            if (!response.ok) {
                if (response.status === 400) {
                    hideLoadingOverlay();
                    return response.json().then(data => {
                        throw new Error(data.message || 'Error en los datos enviados');
                    });
                    
                } else if (response.status === 500) {
                    throw new Error('Error interno del servidor');
                } else {
                    throw new Error('Error desconocido');
                }
            }hideLoadingOverlay();

            // Obtener el RUT del cliente para buscar la información 
            const rutInput = document.getElementById('rutSN') || document.getElementById('inputCliente'); // Ajusta el ID según el HTML
            const rutCliente = rutInput ? rutInput.value : '';

            // Actualizar el campo de entrada con el RUT del cliente
            if (rutCliente) {
                const inputCliente = document.getElementById('rutSN') || document.getElementById('inputCliente');
                if (inputCliente) {
                    inputCliente.value = rutCliente;
                }

                $('#resultadosClientes').empty(); // Limpiar los resultados de la búsqueda 
                traerInformacionCliente(rutCliente); // Traer la información del cliente
            }

            return response.json(); // Devolver los datos de la respuesta
        })

        // Procesar los datos de la respuesta
        .then(data => {
            limpiarMensajes();

            if (data.success === false || data.error) {
                mostrarMensaje(data.error || data.message || 'Ocurrió un error', 'error');

            } else {
                mostrarMensaje(data.message || 'Operación exitosa', 'success');

                const modalElement = document.getElementById('clienteModal'); 
                const modalInstance = bootstrap.Modal.getInstance(modalElement);
                if (modalInstance) {
                    modalInstance.hide();
                }
            }
        })

        // Capturar errores en la solicitud
        .catch(error => {
            submitButton.disabled = false;
            console.error('Error en la solicitud:', error);
            mostrarMensaje(error.message || 'Ocurrió un error desconocido', 'error');
        });
    });
});

// Función para mostrar el overlay de carga
function limpiarMensajes() {
    const mensajes = Array.from(document.querySelectorAll('.mensaje'));
    mensajes.forEach(mensaje => mensaje.remove());
}

// Función para mostrar el overlay de carga
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

    // Agregar el mensaje al contenedor
    contenedorMensajes.appendChild(div);

    // Eliminar automáticamente el mensaje después de 5 segundos
    setTimeout(() => {
        div.classList.remove('show');  // Desvanecer el mensaje
        setTimeout(() => div.remove(), 150);  // Luego removerlo del DOM
    }, 5000);
}

