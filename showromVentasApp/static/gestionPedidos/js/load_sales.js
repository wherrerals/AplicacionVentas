document.addEventListener("DOMContentLoaded", function () {

    function getQueryParam(param) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
    }
  
    const docEntry = getQueryParam('docentry');
    if (docEntry) {
      const vendedorDataElement = document.getElementById("vendedor_data");
      const showroomElement = document.getElementById("sucursal");
      const estadoElement = document.getElementById('estado');
  
      if (vendedorDataElement) {
        vendedorDataElement.innerText = "Cargando...";
        showroomElement.innerText = "Cargando...";
        estadoElement.innerText = "Cargando...";
      }
  
      showLoadingOverlay();
  
      fetch(`/ventas/detalles-ventas/?docentry=${docEntry}`)
        .then(response => {
          if (!response.ok) throw new Error('Error al obtener la información de la cotización');
          return response.json();
        })
        .then(data => {
          console.log("Datos de la cotización:", data);

          if (data.Invoices) {
            console.log("Datos de la cotización:", data);
  
            const salesEmployeeName = data.Invoices.SalesEmployeeName;
            const salesPersonCode = data.Invoices.SalesEmployeeCode;
            const sucursal = data.Invoices.U_LED_SUCURS;
            const numCotizacion = data.Invoices.DocNum;
            const docDate = data.Invoices.DocDate;
            const canceled = data.Invoices.Cancelled;
            let cardCode = data.Invoices.CardCode;
            const DocumentStatus = data.Invoices.DocumentStatus;
            const docEntry = data.Invoices.DocEntry;
            const razonSocial = data.Invoices.CardName;
            const tipoentrega = data.Invoices.TransportationCode;
            const tipoFactura = data.Invoices.U_LED_TIPDOC;
            const referencia = data.Invoices.NumAtCard;
            const comentarios = data.Invoices.Comments;
            const contactos = data.Invoices.Contactos;
            const name_user = data.Invoices.CardName;
            const name_contact = data.Invoices.FirstName;
            const internal_code = data.Invoices.InternalCode;
  
            const name_user_element = document.getElementById("inputCliente");
            const contact_element = document.getElementById("idContact");

            if (contact_element) {
              contact_element.innerText = name_contact;
              contact_element.setAttribute("data-contacto", internal_code);
            }

            if (name_user_element) {
              name_user_element.innerText = name_user;
            } 
  
            console.log("Tipo de comentarios: ", referencia);
            console.log("Tipo de comentarios: ", comentarios);
            
  
            if (cardCode.endsWith("C") || cardCode.endsWith("c")) {
              cardCode = cardCode.slice(0, -1);
            }
  
            const vendedorMatch = salesEmployeeName
            console.log("Vendedor: ", vendedorMatch);
            const vendedorLimpio = vendedorMatch ? vendedorMatch : "Vendedor desconocido";
            console.log("Vendedor limpio: ", vendedorLimpio);
  
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
  
            const tipoEntregaSelect = document.getElementById("tipoEntrega-1");
  
            if (tipoEntregaSelect) {
              tipoEntregaSelect.innerText = tipoentrega;
            }
  
            const tipoDocRadios = document.getElementsByName("tipoDocTributario");
  
            tipoDocRadios.forEach(radio => {
              if (radio.value === tipoFactura) {
                radio.checked = true; // Seleccionar el radio cuyo valor coincide con tipoFactura
              }
            });
  
            const docEntryElement = document.getElementById("numero_cotizacion");
            if (docEntryElement) {
              docEntryElement.setAttribute("data-docEntry", docEntry);
            }
  
            const numeroCotizacionElement = document.getElementById("numero_cotizacion");
            if (numeroCotizacionElement) {
              numeroCotizacionElement.textContent = `${numCotizacion}`;
            }
  
            const dueDateElement = document.getElementById("docDueDate");
            if (dueDateElement) {
              dueDateElement.setAttribute = `${docDate}`;
  
              const date = new Date(docDate);
  
              date.setDate(date.getDate() + 10);
  
              const formattedDate = `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;
  
              dueDateElement.textContent = formattedDate;
  
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
  
            const documentLines = data.DocumentLines;
            console.log("Líneas de documento:", documentLines);
            
            documentLines.sort((a, b) => a.LineNum - b.LineNum);
  
            documentLines.forEach((line) => {
              console.log("Producto: ", line)
              const linea_documento = line.LineNum;
              const docEntry_linea = line.DocEntry;
              const productoCodigo = line.ItemCode;
              const nombre = line.ItemDescription;
              const imagen = line.imagen;
              const precioVenta = line.GrossPrice;
              const stockTotal = 0;
              const precioLista = line.GrossPrice;
              const precioDescuento = line.DiscountPercent;
              const descuentoAplcado = line.DiscountPercent;
              const sucursal = line.WarehouseCode;
              const comentario = line.FreeText;
  
              let linea_documento_real = parseInt(linea_documento);
              console.log("agg")
              console.log(
                "Línea de documento:", linea_documento, 
                "DocEntry línea:", docEntry_linea, 
                "Código de producto:", productoCodigo, 
                "Nombre:", nombre, 
                "Imagen:", imagen, 
                "Precio de venta:", precioVenta, 
                "Stock total:", stockTotal, 
                "Precio lista:", precioLista, 
                "Precio descuento:", precioDescuento, 
                "Cantidad:", line.Quantity, 
                "Sucursal:", sucursal, 
                "Comentario:", comentario, 
                "Descuento aplicado:", descuentoAplcado
              );
  
              agregarProducto(docEntry_linea, linea_documento_real, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, line.Quantity, sucursal, comentario, descuentoAplcado);
            });
          }
  
          hideLoadingOverlay();
        })
        
        .catch(error => {
          console.error('Error en la solicitud AJAX:', error);
          console.log("Error en la solicitud AJAX:", error);
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
      traerInformacionCliente(rutCliente); // Llama a la función con el RUT
  
      // Selecciona el radio correspondiente basado en `grupoSN`.
      const radioInput = document.querySelector(`input[name="grupoSN"][value="${grupoSN}"]`);
      if (radioInput) {
        radioInput.checked = true;
        console.log("Grupo seleccionado:", grupoSN);
        // Ejecuta la función cambiarLabel con la opción seleccionada.
        cambiarLabel('grupoSN', 'nombreLabel', 'apellidoSN', 'apellidorow');
      } else {
        console.warn("No se encontró el input con el valor:", grupoSN);
      }
  
      // Agregar evento onchange para que funcione dinámicamente al cambiar la selección.
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