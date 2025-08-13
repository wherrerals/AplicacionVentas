document.addEventListener("DOMContentLoaded", function () {
    function getQueryParam(param) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
    }
  
    const docEntry = getQueryParam('docentry');
    if (docEntry) {
      const vendedorDataElement = document.querySelector("#vendedor_data");
      const showroomElement = document.getElementById("sucursal");
      const estadoElement = document.getElementById('estado');
  
      if (vendedorDataElement) {
        vendedorDataElement.innerText = "Cargando...";
        showroomElement.innerText = "Cargando...";
        estadoElement.innerText = "Cargando...";
      }
  
      showLoadingOverlay();
  
  
      fetch(`/ventas/detalles_devolucion/?docentry=${docEntry}`)
        .then(response => {
          if (!response.ok) throw new Error('Error al obtener la información de la cotización');
          return response.json();
        })
        .then(data => {
          if (data.Cliente && data.Cliente.SalesPersons) {
  
            const salesEmployeeName = data.Cliente.SalesPersons.SalesEmployeeName;
            const folio = data.Cliente.ReturnRequest.U_VK_Folio;
            const salesPersonCode = data.Cliente.SalesPersons.SalesEmployeeCode;
            const sucursal = data.Cliente.SalesPersons.U_LED_SUCURS;
            const numCotizacion = data.Cliente.ReturnRequest.DocNum;
            const docDate = data.Cliente.ReturnRequest.DocDate;
            const canceled = data.Cliente.ReturnRequest.Cancelled;
            let cardCode = data.Cliente.ReturnRequest.CardCode;
            const DocumentStatus = data.Cliente.ReturnRequest.DocumentStatus;
            const docEntry = data.Cliente.ReturnRequest.DocEntry;
            const tipo_devolucion = data.Cliente.ReturnRequest.U_LED_TIPDEV;
            const tipoFactura = data.Cliente.ReturnRequest.U_LED_TIPDOC;
            const referencia = data.Cliente.ReturnRequest.NumAtCard;
            const comentarios = data.Cliente.ReturnRequest.Comments;

            const folio_element = document.getElementById("folio_referencia");

            if (folio_element) {
              folio_element.value = folio;
            }
            
            if (cardCode.endsWith("C") || cardCode.endsWith("c")) {
              cardCode = cardCode.slice(0, -1);
            }
  
            const vendedorMatch = salesEmployeeName.match(/^[^-]+-\s*([^\s/]+.*?)\s*(\/|$)/);
            const vendedorLimpio = vendedorMatch ? vendedorMatch[1].trim() : "Vendedor desconocido";
  
            if (vendedorDataElement) {
              vendedorDataElement.innerText = vendedorLimpio;
              vendedorDataElement.setAttribute("data-codeven", salesPersonCode);
            }
  
            const showroomElement = document.getElementById("sucursal");
            if (showroomElement) {
              showroomElement.innerText = sucursal;
            }
    
            if (referencia) {
              const referenciaInput = document.getElementById("referencia");
              if (referenciaInput) {
                referenciaInput.value = referencia; // Asigna el valor capturado al input
              } else {
                console.warn("No se encontró el elemento con id 'referencia'.");
              }
            }
    
            if (comentarios) {
              const comentariotxt = document.getElementById("Observaciones-1");
              if (comentariotxt) {
                comentariotxt.value = comentarios; // Asigna el valor capturado al input
              } else {
                console.warn("No se encontró el elemento con id 'comentariotxt'.");
              }
            }
  
            const tipo_devolucionSelect = document.getElementById("tipoEntrega-1");
            if (tipo_devolucionSelect) {
              tipo_devolucionSelect.value = tipo_devolucion;
            }
  
            const tipoDocRadios = document.getElementsByName("tipoDocTributario");
            tipoDocRadios.forEach(radio => {
              if (radio.value === tipoFactura) {
                radio.checked = true;
              }
            });
  
            const docEntryElement = document.getElementById("numero_orden");
            if (docEntryElement) {
              docEntryElement.setAttribute("data-docEntry", docEntry);
            }
  
            const numeroCotizacionElement = document.getElementById("numero_orden");
            if (numeroCotizacionElement) {
              numeroCotizacionElement.textContent = `${numCotizacion}`;
            }
  
            const dueDateElement = document.getElementById("fecha_entrega");
            if (dueDateElement) {
              dueDateElement.value = `${docDate}`;
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
                estadoElement.textContent = "Estado desconocido";
              }
            }
  
            traerInformacionCliente(cardCode);
            const documentLines = data.DocumentLines;
            documentLines.sort((a, b) => a.LineNum - b.LineNum);

            documentLines.forEach((line) => {

                const linea_documento = line.LineNum;
                const docEntry_linea = line.DocEntry;
                const productoCodigo = line.ItemCode;
                const nombre = line.ItemDescription;
                const imagen = line.imagen;
                const precioVenta = line.GrossPrice;
                const stockTotal = 0;
                const precioLista = line.GrossPrice;
                const precioDescuento = line.DiscountPercent;
                const sucursal = line.WarehouseCode;
                const comentario = line.FreeText;
                const tipo_devolucion2 = line.ShippingMethod;
                const fechaEntrega = line.ShipDate;

                let linea_documento_real = parseInt(linea_documento);



              console.log("comentario: ", comentario);
  
              console.log("Agregando producto con datos:", {
                productoCodigo,
                nombre,
                imagen,
                precioVenta,
                stockTotal,
                precioLista,
                precioDescuento,
                sucursal,
                comentario
              });
              agregarProducto(docEntry_linea, linea_documento_real, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, line.Quantity, line.Quantity, sucursal, comentario, precioDescuento, checked=1);
            });
          }
  
          hideLoadingOverlay();
        })
        
        .catch(error => {
          console.error('Error en la solicitud AJAX:', error);
          if (vendedorDataElement) {
            vendedorDataElement.innerText = "Error al cargar datos";
          }
          hideLoadingOverlay();
  
        });
    } else {
      console.log("No se ha proporcionado un DocEntry en la URL.");
      hideLoadingOverlay();
    }
  
    const rutCliente = getQueryParam("rutSN");
    const nombreCliente = getQueryParam("nombreSN");
    let grupoSN = getQueryParam("grupoSN");
    const apellidoCliente = getQueryParam("apellidoSN");
    const giroCliente = getQueryParam("giroSN");
    const telefonoCliente = getQueryParam("telefonoSN");
    const emailCliente = getQueryParam("emailSN");
  
  
  
    if (rutCliente) {
      traerInformacionCliente(rutCliente);
  
      const radioInput = document.querySelector(`input[name="grupoSN"][value="${grupoSN}"]`);
      if (radioInput) {
        radioInput.checked = true;
        cambiarLabel('grupoSN', 'nombreLabel', 'apellidoSN', 'apellidorow');
      } else {
        console.warn("No se encontró el input con el valor:", grupoSN);
      }
  
      document.getElementsByName('grupoSN').forEach(radio => {
        radio.addEventListener('change', () => {
          cambiarLabel('grupoSN', 'nombreLabel', 'apellidoSN', 'apellidorow');
        });
      });
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