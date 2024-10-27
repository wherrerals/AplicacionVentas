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



