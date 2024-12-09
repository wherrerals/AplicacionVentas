function togglePassword() {
    let toggleButton = document.getElementById("togglePasswordButton");
    let passwordInput = document.getElementById("password");

    // Verificar si los elementos existen antes de agregar el evento
    if (toggleButton && passwordInput) {
        toggleButton.addEventListener("click", function() {
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
        toggleButton.addEventListener("click", function() {
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
        apellidoInput.style.display = 'block'; // Mostrar input de apellido
        apellidolabel.style.display = 'block'; // Mostrar label de apellido
    } else if (razonSocialRadio[1].checked) {
        nombreLabel.textContent = 'R. Social';
        apellidoInput.style.display = 'none'; // Ocultar input de apellido
        apellidolabel.style.display = 'none'; // Ocultar label de apellido
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const duplicarOpcion = document.getElementById('duplicar');

    if (duplicarOpcion) {
        duplicarOpcion.addEventListener('click', function (event) {
            event.preventDefault(); // Evitar acción predeterminada del enlace

            console.log('Evento click detectado en "Duplicar".');

            // Crear una nueva pestaña
            const nuevaVentana = window.open('', '_blank');
            if (nuevaVentana) {
                const docOriginal = document.documentElement.cloneNode(true);

                // Crear una estructura HTML completa en la nueva pestaña
                nuevaVentana.document.open();
                nuevaVentana.document.write(`
                    <!DOCTYPE html>
                    <html>
                        <head>
                            ${document.head.innerHTML} <!-- Clonar el contenido del <head> -->
                        </head>
                        <body>
                            ${document.body.innerHTML} <!-- Clonar el contenido del <body> -->
                        </body>
                    </html>
                `);
                nuevaVentana.document.close();
                console.log('Nueva pestaña creada con el contenido duplicado.');

                // Ejecutar la función global definida en ajax__clientes.js
                nuevaVentana.onload = function () {
                    if (typeof nuevaVentana.limpiarInformacionCliente === 'function') {
                        nuevaVentana.limpiarInformacionCliente();
                        console.log('Función limpiarInformacionCliente ejecutada en la nueva pestaña.');
                    } else {
                        console.error('La función limpiarInformacionCliente no está definida en la nueva pestaña.');
                    }
                };
            } else {
                alert('No se pudo abrir una nueva pestaña. Verifica bloqueadores de pop-ups.');
                return;
            }

            // Cerrar el menú desplegable
            const dropdownMenu = duplicarOpcion.closest('.dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.classList.remove('show');
            }

            // Asegúrate de cerrar también el botón de toggle
            const dropdownToggle = duplicarOpcion.closest('.dropdown').querySelector('.dropdown-toggle');
            if (dropdownToggle) {
                dropdownToggle.setAttribute('aria-expanded', 'false');
            }
        });
    } else {
        console.error('No se encontró el enlace "Duplicar". Verifica el id.');
    }
});
