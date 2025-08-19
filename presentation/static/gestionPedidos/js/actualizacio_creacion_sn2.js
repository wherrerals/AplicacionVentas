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
        const cardCode = document.getElementById('inputCliente').getAttribute('data-codigosn') || null;
        const email = document.getElementById('emailSN').value;
        const telefono = document.getElementById('telefonoSN').value;
        const giro = document.getElementById('giroSN').value;
        const sucursal = document.getElementById('sucursal').textContent;
        // docentry es el número de la cotización o numero_orden
        let docentry = null;

        // Intenta capturar el contenido de "numero_cotizacion"
        const cotizacionElement = document.getElementById("numero_cotizacion");
        
        console.log(cardCode);

        // Si no encuentra "numero_cotizacion", busca "numero_orden"
        if (cotizacionElement) {
            docentry = cotizacionElement.textContent;
            console.log(docentry);
        } else {
            const ordenElement = document.getElementById("numero_orden");
            if (ordenElement) {
                docentry = ordenElement.textContent;
            }
        }

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
            sucursal: sucursal,
            docentry: docentry,
            nombreSN: nombre,
            apellidoSN: apellido,
            tipoSN: tipo,
            rutSN: rut,
            cardCodeSN: cardCode,
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
        // En tu bloque .then()
        .then(response => {
            submitButton.disabled = false;

            if (!response.ok) {
                if (response.status === 400) {
                    hideLoadingOverlay();
                    return response.json().then(data => {
                        throw new Error(data.message || 'Error en los datos enviados');
                    });
                } else if (response.status === 500) {
                    hideLoadingOverlay();
                    throw new Error('Error interno del servidor');
                } else {
                    hideLoadingOverlay();
                    throw new Error('Error desconocido');
                }
            }
            hideLoadingOverlay();

            // Obtener el RUT del cliente para buscar la información 
            const rutInput = document.getElementById('rutSN') || document.getElementById('inputCliente');
            const rutCliente = rutInput ? rutInput.value : '';

            if (rutCliente) {
                console.log('RUT del cliente XXXX:', rutCliente);
                $('#resultadosClientes').empty(); // Limpiar los resultados de la búsqueda 

                // Llamar a traerInformacionCliente y luego actualizar los datos en el DOM
                traerInformacionCliente(rutCliente)
                actualizarDatosCliente(rutCliente, rutCliente);
            }

            return response.json();
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
            hideLoadingOverlay();
            mostrarMensaje(error.message || 'Ocurrió un error desconocido', 'error');
        });
    });
});

// Función para mostrar el overlay de carga
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

    // Agregar el mensaje al contenedor
    contenedorMensajes.appendChild(div);

    // Eliminar automáticamente el mensaje después de 5 segundos
    setTimeout(() => {
        div.classList.remove('show');  // Desvanecer el mensaje
        setTimeout(() => div.remove(), 150);  // Luego removerlo del DOM
    }, 5000);
}


function actualizarDatosCliente(clienteId, codigoSN) {
    // Actualizar valores en el DOM
    console.log("Cliente seleccionado, trayendo información del cliente...");
    $('#inputCliente').attr('data-rut', clienteId);
    $('#rutSN').val(clienteId);
    $('#rutSN').attr('data-rut', clienteId); // Actualiza el atributo data-rut
    $('#inputCliente').attr('data-codigoSN', codigoSN);

    // Limpiar los resultados
    $('#resultadosClientes').empty();

    // Formatear y actualizar el RUT en la vista


    // Llamar a las funciones de carga
    cargarDirecciones();
    cargarContactos();
}