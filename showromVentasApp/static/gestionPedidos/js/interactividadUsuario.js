function togglePassword() {
    let toggleButton = document.getElementById("togglePasswordButton");
    let passwordInput = document.getElementById("password");
  
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
  
  togglePassword();


function toggleRepeatPassword() {
    let toggleButton = document.getElementById("toggleRepeatPasswordButton");
    let passwordInput = document.getElementById("rep_clave");
  
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

  toggleRepeatPassword();


