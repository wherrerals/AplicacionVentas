$(document).ready(function () {
  // Función principal que se ejecuta al escribir o interactuar con los inputs
  $("#inputCliente, #rutSN").on("input", function () {
    let inputValue = $(this).val().trim(); // Captura el valor ingresado y elimina espacios en blanco

    // Si el campo está vacío, limpia la información del cliente
    if (inputValue === "") {
      limpiarInformacionCliente();
      return; // Salimos de la función
    }

    // Solo realizar la búsqueda si el valor tiene al menos 3 caracteres
    if (inputValue.length >= 3) {
      ejecutarBusqueda(inputValue);
    } else {
      // Si el valor es menor a 3 caracteres, vacía los resultados
      $("#resultadosClientes").empty();
    }
  });

  // Delegamos el evento click al contenedor para elementos creados dinámicamente
  $("#resultadosClientes").on("click", ".suggestion-item", function () {
    let nombre = $(this).attr("data-nombre");
    let apellido = $(this).attr("data-apellido");
    let clienteId = $(this).attr("data-rut");
    let codigoSN = $(this).attr("data-codigoSN");

    // Actualizar valores en el DOM
    $("#inputCliente").val(`${codigoSN} - ${nombre} ${apellido}`);
    $("#inputCliente").attr("data-rut", clienteId);
    $("#rutSN").val(clienteId);
    $("#rutSN").attr("data-rut", clienteId); // Actualiza el atributo data-rut
    $("#inputCliente").attr("data-codigoSN", codigoSN);

    // Limpiar los resultados
    $("#resultadosClientes").empty();

    traerInformacionCliente(clienteId);

    const rutDisplayParagraph = document.querySelector("#rut-display p");

    actualizarPreciosPorCliente(codigoSN);


    rutDisplayParagraph.textContent = codigoSN;
    

    // Llamar a las funciones cargarContactos y cargarDirecciones
    cargarDirecciones();
    cargarContactos();

    // cargar precios servidor 


  });

  $(document).ready(function () {
    // Función para actualizar el valor de inputCliente al presionar el botón
    $("#grabar-btn").on("click", function () {
      // Obtener valores de los inputs
      let rutSN = $("#rutSN").val().replace(/\./g, ""); // Eliminar puntos

      // Eliminar todo lo que venga después del guion, incluido el guion
      let nuevoTexto = rutSN.split("-")[0];

      // Actualizar el valor de inputCliente
      $("#inputCliente").val(nuevoTexto);

      $("rutSN").val(nuevoTexto);

      // Mostrar en consola para verificar
      console.log("Nuevo valor en inputCliente:", nuevoTexto);
    });
  });

  // Función para realizar la búsqueda
  function ejecutarBusqueda(inputValue) {
    let buscarClientesUrl = "/ventas/buscar_clientes/";
    let parametros = {};

    // Limpiar la "C" al final del valor si existe
    if (inputValue.endsWith("C") || inputValue.endsWith("c")) {
      inputValue = inputValue.slice(0, -1); // Remueve la última letra "C"
    }

    // Detectamos si el valor contiene solo números y puntos
    if (/^[0-9.]+$/.test(inputValue)) {
      parametros = { numero: inputValue, nombre: "" }; // Buscar por número
    } else {
      parametros = { numero: "", nombre: inputValue }; // Buscar por nombre
    }

    $.ajax({
      url: buscarClientesUrl,
      data: parametros, // Enviamos los parámetros adecuados
      dataType: "json",
      success: function (data) {
        $("#resultadosClientes").empty();
        if (data.resultadosClientes && data.resultadosClientes.length > 0) {
          data.resultadosClientes.forEach(function (resultado) {
            let clientesElemento = $("<p></p>");
            clientesElemento.addClass("suggestion-item");
            clientesElemento.attr("data-nombre", resultado.nombre);
            clientesElemento.attr("data-apellido", resultado.apellido);
            clientesElemento.attr("data-codigoSN", resultado.codigoSN);
            clientesElemento.attr("data-rut", resultado.rut);
            clientesElemento.text(
              `${resultado.codigoSN} - ${resultado.nombre} ${resultado.apellido}`
            );

            $("#resultadosClientes").append(clientesElemento);
          });
        } else {
          const cardcode = (inputValue || "")
            .toString()
            .trim()
            .replace(/\./g, "")
            .split("-")[0];
          const rut = inputValue;

          $("#resultadosClientes").html("No se encontraron resultados");

          const moduloClientes = document.querySelector("#crearClientes");

          if (moduloClientes) {
            $("#resultadosClientes").append(
              '<br><a href="#" class="cliente-link" data-cadcode="' +
                cardcode +
                '">Crear desde SAP</a>'
            );
          } else {
            $("#resultadosClientes").append(
              '<br><a href="#" class="cliente-link-carga" data-rut="' +
              cardcode +
                '">Crear desde SAP</a>'
            );
          }
        }

        // Agrega el evento click a todos los enlaces de clientes después de añadir las filas
        document.querySelectorAll(".cliente-link").forEach((link) => {
          link.addEventListener("click", (event) => {
            event.preventDefault();
            let cadCode = event.target.getAttribute("data-cadcode");

            // Eliminar la "C" final si está presente
            if (cadCode && cadCode.endsWith("C") || cadCode && cadCode.endsWith("c")) {
              cadCode = cadCode.slice(0, -1);
            }

            if (cadCode) {
              showLoadingOverlay();
              // Realiza la solicitud AJAX al backend para obtener la información del cliente
              fetch(`/ventas/informacion_cliente/?rut=${cadCode}`)
                .then((response) => {
                  if (!response.ok) {
                    if (response.status === 404) {
                      // Si el servidor devuelve un 404, muestra una alerta específica
                      alert(
                        "El cliente no existe en el sistema. Por favor, ingrese los datos manualmente."
                      );
                      hideLoadingOverlay();
                      return; // Detiene la ejecución adicional
                    } else {
                      throw new Error(
                        "Error al obtener la información del cliente"
                      );
                    }
                  }
                  alert(
                    "Cliente encontrado en SAP. Presione Ok para verlo en el sistema..."
                  );
                  return response.json();
                })
                .then((data) => {
                  console.log("Información del cliente:", data);
                  // Redirige a la página de creación de cliente después de obtener los datos
                  window.location.href = `/ventas/creacion_clientes/?rut=${cadCode}`;
                })
                .catch((error) => {
                  hideLoadingOverlay();
                  console.error("Error en la solicitud AJAX:", error);
                });
            } else {
              hideLoadingOverlay();
              alert("No se pudo obtener el RUT del cliente.");
            }
          });
        });

        // Función para obtener el valor de la cookie CSRF
        function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Busca la cookie que comienza con el nombre proporcionado
              if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
                );
                break;
              }
            }
          }
          return cookieValue;
        }

        // Obtén el token CSRF
        const csrftoken = getCookie("csrftoken");

        document.querySelectorAll(".cliente-link-carga").forEach((link) => {
          link.addEventListener("click", (event) => {
            event.preventDefault();
            let cadCode = event.target.getAttribute("data-rut");

            // Eliminar la "C" final si está presente
            if (cadCode && cadCode.endsWith("C") || cadCode && cadCode.endsWith("c")) {
              cadCode = cadCode.slice(0, -1);
            }

            if (cadCode) {
              showLoadingOverlay();

              // Realiza la solicitud AJAX al backend para obtener la información del cliente
              fetch(`/ventas/informacion_cliente/?rut=${cadCode}`)
                .then((response) => {
                  if (!response.ok)
                    throw new Error(
                      "Error al obtener la información del cliente"
                    );
                  return response.json();
                })
                .then((data) => {
                  console.log("Información del cliente:", data);
                  $("#resultadosClientes").empty(); // Limpiar los resultados de la búsqueda
                  traerInformacionCliente(cadCode); // Llama a la función para traer la información del cliente
                  hideLoadingOverlay();
                })
                .catch((error) => {
                  hideLoadingOverlay();
                  console.error("Error en la solicitud AJAX:", error);
                  alert(
                    "Este cliente no está en SAP. Por favor, regístralo para continuar."
                  );
                });
            } else {
              hideLoadingOverlay();
              alert("No se pudo obtener el RUT del cliente.");
            }
          });
        });
      },
      error: function (xhr, status, error) {
        console.error("Error en la solicitud AJAX:", error);
      },
    });
  }

  function limpiarInformacionCliente() {
    $("#inputCliente").val(""); // Limpia el campo de entrada
    $("#rutSN").val(""); // Limpia el campo de RUT
    $("#rutSN").removeAttr("data-rut"); // Limpia el atributo data-rut
    $("#inputCliente").removeAttr("data-rut").removeAttr("data-codigoSN"); // Elimina los atributos
    $("#resultadosClientes").empty(); // Vacía el contenedor de resultados
    $("#nombreSN").val("");
    $("#apellidoSN").val("");
    $("#rutSN").val("");
    $("#codigoSN").val("");
    $("#telefonoSN").val("");
    $("#emailSN").val("");
    $("#giroSN").val("");
    $('#rutSN').prop('readonly', false);


    // Restablece el select de contactos con la opción predeterminada
    $("#clientes").html(`<option value="">Seleccione un contacto</option>`);

    // Restablece los selects de direcciones con opciones predeterminadas
    $("#direcciones_despacho").html(
      '<option value="">Seleccione una dirección de despacho</option>'
    );
    $("#direcciones_facturacion").html(
      '<option value="">Seleccione una dirección de facturación</option>'
    );

    console.log("Información del cliente limpia.");
  }
});
