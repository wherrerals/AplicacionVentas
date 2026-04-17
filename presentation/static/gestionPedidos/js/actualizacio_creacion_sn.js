const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const formularios = document.querySelectorAll('#forCrearPedidos, #forCrearCliente');

formularios.forEach(formulario => {
    formulario.addEventListener('submit', function (event) {
        event.preventDefault();

        const nombre   = document.getElementById('nombreSN').value;
        const apellido = document.getElementById('apellidoSN').value;
        const rut      = document.getElementById('rutSN').value;
        
        // Defensivo: el elemento puede no existir
        const inputClienteEl = document.getElementById('inputCliente');
        const cardCode = inputClienteEl ? inputClienteEl.getAttribute('data-codigosn') || null : null;
        
        const tipoEl = document.querySelector('input[name="grupoSN"]:checked');
        const tipo   = tipoEl ? tipoEl.value : null;
        
        const email    = document.getElementById('emailSN').value;
        const telefono = document.getElementById('telefonoSN').value;
        const giro     = document.getElementById('giroSN').value;
        const sucursal = document.getElementById('sucursal').textContent;

        let docentry = null;
        const cotizacionElement = document.getElementById("numero_cotizacion");
        if (cotizacionElement) {
            docentry = cotizacionElement.textContent;
        } else {
            const ordenElement = document.getElementById("numero_orden");
            if (ordenElement) docentry = ordenElement.textContent;
        }

        const lines = [];
        document.querySelectorAll('.direcciones').forEach((row, index) => {
            lines.push({
                direccionSN:      index,
                tipoDireccion:    row.querySelector("#direccionSN")?.value     || "",
                nombreDireccion:  row.querySelector("#nombreDireccionSN")?.value || "",
                pais:             row.querySelector("#paisSN")?.value           || "",
                region:           row.querySelector("#regionSN")?.value         || "",
                comuna:           row.querySelector("#comunaSN")?.value         || "",
                ciudad:           row.querySelector("#ciudad")?.value           || "",
                direccion:        row.querySelector("#direccion")?.value         || ""
            });
        });

        const contactos = [];
        document.querySelectorAll('.contactos').forEach((row, index) => {
            contactos.push({
                contactoSN:        index,
                nombreContacto:    row.querySelector("#nombreContacto")?.value    || "",
                apellidoContacto:  row.querySelector("#apellidoContacto")?.value  || "",
                telefonoContacto:  row.querySelector("#telefonoContacto")?.value  || "",
                puestoContacto:    row.querySelector("#celularContacto")?.value   || "",
                emailContacto:     row.querySelector("#emailContacto")?.value     || ""
            });
        });

        // Declaradas con const → sin riesgo de contaminación global
        const data = {
            sucursal, docentry,
            nombreSN:   nombre,
            apellidoSN: apellido,
            tipoSN:     tipo,
            rutSN:      rut,
            cardCodeSN: cardCode,
            emailSN:    email,
            telefonoSN: telefono,
            giroSN:     giro,
            direcciones: lines,
            contactos
        };
        const dataSN = JSON.stringify(data);
        console.log("Datos a enviar:", dataSN);

        const submitButton = document.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        showLoadingOverlay();

        fetch('/ventas/agregar_editar_clientes/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: dataSN
        })
        .then(response => {
            submitButton.disabled = false;
            hideLoadingOverlay();

            // Todos los casos leen el JSON del servidor
            if (!response.ok) {
                return response.json().then(errData => {
                    const msg = errData.message || errData.details || `Error ${response.status}`;
                    throw new Error(msg);
                }).catch(err => {
                    // Si el body no es JSON válido
                    throw new Error(err.message || `Error ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            limpiarMensajes();
            if (data.success === false || data.error) {
                mostrarMensaje(data.error || data.message || 'Ocurrió un error', 'error');
            } else {
                mostrarMensaje(data.message || 'Operación exitosa', 'success');

                const rutInput = document.getElementById('rutSN') || document.getElementById('inputCliente');
                const rutCliente = rutInput ? rutInput.value : '';
                if (rutCliente) {
                    $('#resultadosClientes').empty();
                    traerInformacionCliente(rutCliente);
                }

                const modalElement = document.getElementById('clienteModal');
                const modalInstance = bootstrap.Modal.getInstance(modalElement);
                if (modalInstance) modalInstance.hide();
            }
        })
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

