document.addEventListener("DOMContentLoaded", function () {
  // Función para obtener parámetros de la URL
  function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }

  const documentoCopiado = getQueryParam('documento_copiado');
  if (documentoCopiado) {
    const vendedorDataElement = document.getElementById("vendedor_data");
    const showroomElement = document.getElementById("sucursal");
    const estadoElement = document.getElementById('estado');

    if (vendedorDataElement) {
      vendedorDataElement.innerText = "Cargando...";
      showroomElement.innerText = "Cargando...";
      estadoElement.innerText = "Cargando...";
    }

    showLoadingOverlay();


    fetch(`/ventas/copiar_a_odv/?documento_copiado=${documentoCopiado}`)
      .then(response => {
        if (!response.ok) throw new Error('Error al obtener la información de la cotización');
        return response.json();
      })
      .then(data => {
        if (data.Cliente && data.Cliente.SalesPersons) {
          console.log("Datos de la cotización:", data);

          // Extracción de datos principales
          const salesEmployeeName = data.Cliente.SalesPersons.SalesEmployeeName;
          const sucursal = data.Cliente.SalesPersons.U_LED_SUCURS;
          const docDate = data.Cliente.Orders.DocDate;
          const canceled = data.Cliente.Orders.Cancelled;
          let cardCode = data.Cliente.Orders.CardCode;
          const DocumentStatus = data.Cliente.Orders.DocumentStatus;
          const referencia = data.Cliente.Orders.NumAtCard;
          const tipoentrega = data.Cliente.Orders.TransportationCode;
          const tipoFactura = data.Cliente.Orders.U_LED_TIPDOC;
          const comentarios = data.Cliente.Orders.Comments;




          if (referencia) {
            const referenciaInput = document.getElementById("referencia");
            if (referenciaInput) {
              referenciaInput.value = referencia; // Asigna el valor capturado al input
            } else {
              console.warn("No se encontró el elemento con id 'referencia'.");
            }
          }

          const tipoEntregaSelect = document.getElementById("tipoEntrega-1");

          // Verificar si el elemento existe
          if (tipoEntregaSelect) {
            // Ajustar el valor del select al tipo de entrega obtenido
            tipoEntregaSelect.value = tipoentrega;
          }

          const tipoDocRadios = document.getElementsByName("tipoDocTributario");

          // Iterar sobre los radios para seleccionar el correspondiente
          tipoDocRadios.forEach(radio => {
            if (radio.value === tipoFactura) {
              radio.checked = true; // Seleccionar el radio cuyo valor coincide con tipoFactura
            }
          });

          if (comentarios) {
            const comentariotxt = document.getElementById("Observaciones-1");
            if (comentariotxt) {
              comentariotxt.value = comentarios; // Asigna el valor capturado al input
            } else {
              console.warn("No se encontró el elemento con id 'comentariotxt'.");
            }
          }

          if (cardCode.endsWith("C")) {
            cardCode = cardCode.slice(0, -1);
          }

          const vendedorMatch = salesEmployeeName.match(/^[^-]+-\s*([^\s/]+.*?)\s*(\/|$)/);
          const vendedorLimpio = vendedorMatch ? vendedorMatch[1].trim() : "Vendedor desconocido";

          if (vendedorDataElement) {
            vendedorDataElement.innerText = vendedorLimpio;
          }

          const showroomElement = document.getElementById("sucursal");
          if (showroomElement) {
            showroomElement.innerText = sucursal;
          }

          const dueDateElement = document.getElementById("docDueDate");
          if (dueDateElement) {
            dueDateElement.textContent = `${docDate}`;
          }

          const estadoElement = document.querySelector('p strong[data-estado="bost_Open"]');
          if (estadoElement) {
            if (canceled === "N" && DocumentStatus === "O") {
              estadoElement.textContent = "Abierta";
            } else if (canceled === "N" && DocumentStatus === "C") {
              estadoElement.textContent = "Cerrado";
            } else if (canceled === "Y" && DocumentStatus === "C") {
              estadoElement.textContent = "Cancelado";
            } else {
              estadoElement.textContent = "Estado desconocido"; // Para casos no previstos
            }
          }

          traerInformacionCliente(cardCode);

          // Iteración sobre `DocumentLines` para añadir cada producto
          const documentLines = data.DocumentLines;
          documentLines.forEach((line) => {
            console.log("Producto: ", line)
            const productoCodigo = line.ItemCode;
            const nombre = line.ItemDescription;
            const imagen = line.imagen;
            const precioVenta = line.PriceAfterVAT;
            const stockTotal = 0;
            const precioLista = line.GrossPrice;
            const precioDescuento = line.DiscountPercent;
            const sucursal = line.WarehouseCode;
            const stockBodega = line.StockBodega;
            const comentario = line.FreeText;
            const precioCoti = precioVenta * line.Quantity;
            const cantidadCoti = line.Quantity;

            if (cantidadCoti > stockBodega) {
              cantidad = stockBodega;
            } else {
              cantidad = cantidadCoti;
            }
            

            console.log("Agregando producto con datos:", {
              productoCodigo,
              nombre,
              stockBodega
            });
            
            setTimeout(() => {
              document.querySelectorAll(".valorCotizacion").forEach((element) => {
                element.removeAttribute("hidden");
              });
            }, 100); // Espera 100ms para que los elementos se generen antes de ejecutarse
            
            agregarProducto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, line.Quantity, precioCoti);
          });
        }
        // Llamar a la función para inicializar el precio
        hideLoadingOverlay();
      })
      .catch(error => {
        console.error('Error en la solicitud AJAX:', error);
        if (vendedorDataElement) {
          vendedorDataElement.innerText = "Error al cargar datos";
        }
      });
  } else {
    console.log("No se ha proporcionado un DocEntry en la URL.");
  }

  // Manejo de rutSN
  const rutCliente = getQueryParam("rutSN");
  const nombreCliente = getQueryParam("nombreSN");
  let grupoSN = getQueryParam("grupoSN");
  const apellidoCliente = getQueryParam("apellidoSN");
  const giroCliente = getQueryParam("giroSN");
  const telefonoCliente = getQueryParam("telefonoSN");
  const emailCliente = getQueryParam("emailSN");



  if (rutCliente) {
    //console.log("RUT recibido en la página de destino:", rutCliente);
    //console.log("Nombre recibido en la página de destino:", nombreCliente);
    //console.log("Apellido recibido en la página de destino:", apellidoCliente);
    //console.log("Grupo recibido en la página de destino:", grupoSN);
    //console.log("Giro recibido en la página de destino:", giroCliente);
    //console.log("Teléfono recibido en la página de destino:", telefonoCliente);
    //console.log("Email recibido en la página de destino:", emailCliente);
    traerInformacionCliente(rutCliente); // Llama a la función con el RUT

    if (grupoSN) {
      document.querySelector(`input[name="grupoSN"][value="${grupoSN}"]`).checked = true;
    }
    if (nombreSN) {
      document.getElementById("nombreSN").value = nombreCliente;
    }
    if (apellidoSN) {
      document.getElementById("apellidoSN").value = apellidoCliente;
    }
    if (rutCliente) {
      document.getElementById("rutSN").value = rutCliente;
    }
    if (giroSN) {
      document.getElementById("giroSN").value = giroCliente;
    }
    if (telefonoSN) {
      document.getElementById("telefonoSN").value = telefonoCliente;
    }
    if (emailSN) {
      document.getElementById("emailSN").value = emailCliente;
    }
  } else {
    console.log("No se proporcionó un RUT válido en la URL.");
  }
});


