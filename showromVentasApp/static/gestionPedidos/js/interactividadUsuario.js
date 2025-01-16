function togglePassword() {
    let toggleButton = document.getElementById("togglePasswordButton");
    let passwordInput = document.getElementById("password");

    // Verificar si los elementos existen antes de agregar el evento
    if (toggleButton && passwordInput) {
        toggleButton.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                toggleButton.textContent = "Ocultar";
            } else {
                passwordInput.type = "password";
                toggleButton.textContent = "Mostrar";
            }
        });
    }
}

togglePassword();

function toggleRepeatPassword() {
    let toggleButton = document.getElementById("toggleRepeatPasswordButton");
    let passwordInput = document.getElementById("rep_clave");

    // Verificar si los elementos existen antes de agregar el evento
    if (toggleButton && passwordInput) {
        toggleButton.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                toggleButton.textContent = "Ocultar";
            } else {
                passwordInput.type = "password";
                toggleButton.textContent = "Mostrar";
            }
        });
    }
}

toggleRepeatPassword();


// archivo formularioReactivo.js

function cambiarLabel(razonSocialRadioName, nombreLabelId, apellidoInputId, apellidolabelId) {
    var razonSocialRadio = document.getElementsByName(razonSocialRadioName);
    var nombreLabel = document.getElementById(nombreLabelId);
    var apellidoInput = document.getElementById(apellidoInputId);
    var apellidolabel = document.getElementById(apellidolabelId);

    if (razonSocialRadio[0].checked) {
        nombreLabel.textContent = 'Nombre';
        apellidoInput.style.display = 'block'; //   Mostrar input de apellido
        apellidolabel.style.display = 'block'; // Mostrar label de apellido
    } else if (razonSocialRadio[1].checked) {
        nombreLabel.textContent = 'R. Social';
        apellidoInput.style.display = 'none'; // Ocultar input de apellido
        apellidolabel.style.display = 'none'; // Ocultar label de apellido
    }
}


function limpiarInformacionCliente() {
    // Limpia todos los campos relacionados con el cliente
    $('#inputCliente').val(''); 
    $('#numero_cotizacion').text('');
    $('#numero_cotizacion').removeAttr('data-docentry');
    $('#rutSN').val('').removeAttr('data-rut');
    $('#inputCliente').removeAttr('data-rut').removeAttr('data-codigoSN');
    $('#resultadosClientes').empty();
    $('#nombreSN').val('');
    $('#apellidoSN').val('');
    $('#rutSN').val('');
    $('#codigoSN').val('');
    $('#telefonoSN').val('');
    $('#emailSN').val('');
    $('#giroSN').val('');

    // Limpiar los datos de vendedor y sucursal
    $('#vendedor_data').text('');
    $('#vendedor_data').removeAttr('data-codeVen');
    $('#sucursal').text('');



    // Realizar una llamada AJAX para obtener los valores actualizados de vendedor y sucursal
    $.ajax({
        url: '/ventas/get_vendedor_sucursal/',  // URL de la vista que devuelve los datos en JSON
        method: 'GET',
        success: function(data) {
            if (data.nombreUser && data.codigoVendedor !== undefined) {
                $('#vendedor_data').text(data.nombreUser).attr('data-codeVen', data.codigoVendedor);
                $('#sucursal').text(data.sucursal);
            } else {
                console.error('No se pudieron obtener los datos del vendedor o la sucursal');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error al obtener los datos del vendedor y sucursal: ', error);
        }
    });

    // Quitar el disable en inputCliente
    $('#inputCliente').prop('disabled', false);

    // Restablecer los selects de contactos y direcciones
    $('#clientes').html('<option value="">Seleccione un contacto</option>');
    $('#direcciones_despacho').html('<option value="">Seleccione una dirección de despacho</option>');
    $('#direcciones_facturacion').html('<option value="">Seleccione una dirección de facturación</option>');

    console.log("Información del cliente limpia.");

    // Modificar la URL para eliminar el parámetro `docentry`
    const newUrl = window.location.origin + window.location.pathname; // Conserva solo el dominio y la ruta
    history.replaceState(null, '', newUrl); // Actualiza la URL sin recargar la página
}


const copiarODVButtons = document.querySelectorAll("#copiar-ODV, #copiar-ODV-1");

copiarODVButtons.forEach(button => {
    button.addEventListener('click', (event) => {
        console.log("Ejecutando...");
        event.preventDefault(); // Evitar comportamiento predeterminado del botón/enlace

        // Obtener el elemento que contiene el valor del número de cotización
        const docEntryElement = document.getElementById('numero_cotizacion').getAttribute("data-docentry");

        if (docEntryElement) {
            showLoadingOverlay(); // Mostrar un overlay de carga
            window.location.href = `/ventas/ordenesVentas/?documento_copiado=${docEntryElement}`; // Redirigir con el docEntry
        } else {
            hideLoadingOverlay(); // Ocultar el overlay si ocurre un error
            alert("No se pudo obtener el DocEntry de la orden."); // Mostrar alerta de error
        }
    });
});



const cerrarButton = document.getElementById("cerrar");

// Verificar si el elemento existe antes de agregar el evento
if (cerrarButton) {
    cerrarButton.addEventListener("click", function (event) {
        event.preventDefault();
        handleAction("cerrar");
    });
} else {
    //console.warn('El botón con ID "cerrar" no existe en el DOM.');
}

const cancelarButton = document.getElementById("cancelar");
if (cancelarButton) {
    cancelarButton.addEventListener("click", function (event) {
        event.preventDefault();
        handleAction("cancelar");
    });
} else {
    //console.warn('El botón con ID "cerrar" no existe en el DOM.');
}

const duplicarbutton = document.getElementById("duplicar-1");
if (duplicarbutton) {
    duplicarbutton.addEventListener("click", function (event) {
        limpiarInformacionCliente();
    });
}

function handleAction(action) {
    const numeroCotizacion = document.getElementById("numero_cotizacion").innerText;
    const estado = action === "cerrar" ? "Close" : "Cancel";

    // Crear objeto de datos a enviar
    const payload = {
        DocNum: numeroCotizacion,
        Estado: estado
    };

    // Limpiar mensajes previos antes de mostrar nuevos
    limpiarMensajes();

    // Realizar POST con los datos
    fetch('/ventas/cambiar_estado_cotizacion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => {
            if (response.ok) {
                return response.json(); // Continuar para procesar la respuesta del servidor
            } else {
                // Mostrar mensaje de error con el estado de la respuesta
                mostrarMensaje("Error en la solicitud. Estado: " + response.statusText, "error");
                throw new Error("Respuesta no exitosa del servidor.");
            }
        })
        .then(data => {
            if (data.success) { // Suponiendo que el servidor retorna un campo 'success'
                mostrarMensaje("Acción realizada con éxito.", "success");
            } else {
                mostrarMensaje(data.message || "Se produjo un error desconocido.", "error");
            }
        })
        .catch(error => {
            // Mostrar mensaje de error si falla el POST
            console.error("Error al realizar el POST:", error);
            mostrarMensaje("Error al procesar la solicitud: " + error.message, "error");
        });

}
