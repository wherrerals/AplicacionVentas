const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const formularios = document.querySelectorAll('#forCrearPedidos, #forCrearCliente');

formularios.forEach(formulario => {
    formulario.addEventListener('submit', function (event) {
        event.preventDefault();
        showLoadingOverlay();

    const nombre = document.getElementById('nombreSN').value;
    const apellido = document.getElementById('apellidoSN').value;
    const rut = document.getElementById('rutSN').value;
    const tipo = document.querySelector('input[name="grupoSN"]:checked').value;
    const email = document.getElementById('emailSN').value;
    const telefono = document.getElementById('telefonoSN').value;
    const giro = document.getElementById('giroSN').value;

    /*     const formData = new FormData(this);
        console.log('Datos del formulario:', formData); */


    const lines = [];
    const contactos = [];


    // Selecciona todas las líneas de cada producto
    const productRows = document.querySelectorAll('.direcciones');

    productRows.forEach((row, index) => {
        const tipoDireccion = row.querySelector("#direccionSN")?.value || "";
        const nombreDireccion = row.querySelector("#nombreDireccionSN")?.value || "";
        const pais = row.querySelector("#paisSN")?.value || "";
        const region = row.querySelector("#regionSN")?.value || "";
        const comuna = row.querySelector("#comunaSN")?.value || "";
        const ciudad = row.querySelector("#ciudad")?.value || "";
        const direccion = row.querySelector("#direccion")?.value || "";

        // Crea un objeto con los datos de la línea
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

    // Captura los contactos
    const contactoRows = document.querySelectorAll('.contactos');
    contactoRows.forEach((row, index) => {
        const nombreContacto = row.querySelector("#nombreContacto")?.value || "";
        const apellidoContacto = row.querySelector("#apellidoContacto")?.value || "";
        const telefonoContacto = row.querySelector("#telefonoContacto")?.value || "";
        const celularContacto = row.querySelector("#celularContacto")?.value || "";
        const emailContacto = row.querySelector("#emailContacto")?.value || "";


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

    data = {
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

    dataSN = JSON.stringify(data);

    console.log('Datos del formulario:', dataSN);

    const submitButton = document.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    fetch('/ventas/agregar_editar_clientes/', {  // Verifica que esta ruta coincida con la vista del backend
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: dataSN
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
            console.log('RUT capturado:', rutCliente);

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

