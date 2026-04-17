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

        // Defensivo: el elemento puede no existir
        const inputClienteEl = document.getElementById('inputCliente');
        const cardCode = inputClienteEl ? inputClienteEl.getAttribute('data-codigosn') || null : null;

        const tipoEl = document.querySelector('input[name="grupoSN"]:checked');
        const tipo = tipoEl ? tipoEl.value : null;

        const email = document.getElementById('emailSN').value;
        const telefono = document.getElementById('telefonoSN').value;
        const giro = document.getElementById('giroSN').value;
        const sucursal = document.getElementById('sucursal').textContent;

        // docentry es el número de la cotización o numero_orden
        let docentry = null;
        const cotizacionElement = document.getElementById("numero_cotizacion");      
        if (cotizacionElement) {
            docentry = cotizacionElement.textContent;
        } else {
            const ordenElement = document.getElementById("numero_orden");
            if (ordenElement) docentry = ordenElement.textContent;
        }

        // Obtener las direcciones y contactos
        const lines = [];
        document.querySelectorAll('.direcciones').forEach((row, index) => {
            // Crear un objeto con los datos de la fila de direcciones
             lines.push({
                direccionSN: index,
                tipoDireccion: row.querySelector("#direccionSN")?.value || "",
                nombreDireccion: row.querySelector("#nombreDireccionSN")?.value || "",
                pais: row.querySelector("#paisSN")?.value || "",
                region: row.querySelector("#regionSN")?.value || "",
                comuna: row.querySelector("#comunaSN")?.value || "",
                ciudad: row.querySelector("#ciudad")?.value || "",
                direccion: row.querySelector("#direccion")?.value || ""
            });
        });

                
        const contactos = [];
        document.querySelectorAll('.contactos').forEach((row, index) => {

            // Crear un objeto con los datos de la fila de contactos
            contactos.push({
                contactoSN: index,
                nombreContacto: row.querySelector("#nombreContacto")?.value || "",
                apellidoContacto: row.querySelector("#apellidoContacto")?.value || "",
                telefonoContacto: row.querySelector("#telefonoContacto")?.value || "",
                puestoContacto: row.querySelector("#puestoContacto")?.value || "",
                emailContacto: row.querySelector("#emailContacto")?.value || ""
            });
        });

        // Crear un objeto con los datos del formulario
        const data = {
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
        const dataSN = JSON.stringify(data);
        const submitButton = document.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        showLoadingOverlay();

        // Enviar los datos del formulario
        fetch('/ventas/agregar_editar_clientes/', {  
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: dataSN
        })

        .then(response => {
            submitButton.disabled = false;
            hideLoadingOverlay();

            if (!response.ok) {
                return response.json().then(errData => {
                    const msg = errData.message || errData.details || `Error ${response.status}`;
                    throw new Error(msg);
                }).catch(err => {
                    // Si el body no es JSON válido
                    throw new Error(err.message || `Error ${response.status}`);
                });
            }

            const rutInput = document.getElementById('rutSN') || document.getElementById('inputCliente');
            const rutCliente = rutInput ? rutInput.value : '';

            if (rutCliente) {
                $('#resultadosClientes').empty();  
                traerInformacionCliente(rutCliente)
                actualizarDatosCliente(rutCliente, rutCliente);
            }

            return response.json();
        })

        .then(data => {
            limpiarMensajes();

            if (data.success === false || data.error) {
                mostrarMensaje(data.error || data.message || 'Ocurrió un error', 'error');

            } else {
                mostrarMensaje(data.message || 'Operación exitosa', 'success');

                const modalElement = document.getElementById('clienteModal'); 
                const modalInstance = bootstrap.Modal.getInstance(modalElement);
                if (modalInstance) modalInstance.hide();
            }
        })

        // Capturar errores en la solicitud
        .catch(error => {
            submitButton.disabled = false;
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