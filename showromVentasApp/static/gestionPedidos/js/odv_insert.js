// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("saveButton").addEventListener("click", submitForm);
  
    function submitForm() {
      showLoadingOverlay();
  
      // Capturar los datos de la cebezera del documento
      const fechaSolo = new Date().toISOString().split("T")[0]; // Salida en formato YYYY-MM-DD
      const docNum = document.getElementById("numero_orden").textContent;
      const docEntry = document.getElementById("numero_orden").getAttribute("data-docEntry");
      const docTotal = document.getElementById("total_bruto").getAttribute("data-total-bruto");
      const docDate = fechaSolo;
      const fechaentrega = document.getElementById("fecha_entrega").value;
      const taxDate = fechaSolo;
      const rut = document.getElementById("inputCliente").getAttribute("data-codigoSN");
      const cardCode = rut;
      const pgc = -1;
      const referencia = document.getElementById("referencia").value;
      const observaciones = document.getElementById("Observaciones-1").value;
      const spcInt = document.getElementById("vendedor_data").getAttribute("data-codeVen");
      const spc = parseInt(spcInt, 10);
      const selectElement = document.getElementById("direcciones_despacho");
      const direccion2 = selectElement.value;
      const selectElement2 = document.getElementById("direcciones_facturacion");
      const direccion = selectElement2.value;
      const contactoCliente = document.getElementById("contactos_cliete");
      const contacto = contactoCliente.value;
      const trnasp = document.getElementById("tipoEntrega-1").value;
      const ulfen = 1;
      const tipoDocElement = document.querySelector("[name='tipoDocTributario']:checked");
  
      const horarioEntrega = document.getElementById("horario_entrega").value;
      console.log(horarioEntrega);
  
      if (!tipoDocElement) {
        console.error("No se seleccionó un tipo de documento tributario.");
        return;
      }
  
      // Captura las líneas del documento
      const ultd = tipoDocElement.value;
      const lines = [];
      const productRows = document.querySelectorAll(".product-row");
  
      productRows.forEach((row, index) => {
        const linenum = row.querySelector("#indixe_producto").getAttribute('data-linenum'); //listo
        const itemCode = row.querySelector("[name='sku_producto']").innerText;
        const quantity = row.querySelector("[name='cantidad']").value;
        const discount = row.querySelector("#agg_descuento").value;
        const fechaentregaLineas = row.querySelector("#fecha_entrega_lineas").value;
        const bodegaSelect = row.querySelector(".bodega-select");
        const warehouseCode = bodegaSelect ? bodegaSelect.value : null;
        const comentarios = row.querySelector("#comentarios-1").value;
        const tipoEntregaLineas = row.querySelector("#tipoEntrega").value;

        const docentryLinea = row.getAttribute('data-docentryLinea'); // "null" o el valor asignado

  // Selecciona el elemento <select> por su clase
        const selectElement = document.querySelector(".form-select.bodega-select");

        // Obtiene el <option> seleccionado
        const selectedOption = selectElement.options[selectElement.selectedIndex];

        // Obtiene el valor del atributo data-cantidadinicialsap
        const cantidadInicialSAP = selectedOption.getAttribute("data-cantidadinicialsap");

        console.log(cantidadInicialSAP); // Muestra el valor de data-cantidadinicialsap
        
        const costingCode = warehouseCode;
        const cogsCostingCode = warehouseCode;
        const costingCode2 = "AV";
        const cogsCostingCode2 = "AV";
  
        const line = {
          LineNum: linenum,
          DocEntry_line: docentryLinea,
          ItemCode: itemCode,
          Quantity: parseFloat(quantity),
          ShipDate: fechaentregaLineas,
          FreeText: comentarios,
          DiscountPercent: parseFloat(discount),
          WarehouseCode: warehouseCode,
          CostingCode: costingCode,
          ShippingMethod: tipoEntregaLineas,
          COGSCostingCode: cogsCostingCode,
          CostingCode2: costingCode2,
          COGSCostingCode2: cogsCostingCode2,
          CantidadInicialSAP: cantidadInicialSAP,
        };
        
        lines.push(line);
      });
  
      // Crea el objeto dcoumento final que será enviado en formato JSON
      const documentData = {
        DocNum: docNum,
        DocEntry: docEntry,
        DocDate: docDate,
        DocTotal: docTotal,
        NumAtCard: referencia,
        DocDueDate: fechaentrega,
        Comments: observaciones,
        TaxDate: taxDate,
        ContactPersonCode: contacto,
        Address: direccion, // direccion de facturacion
        Address2: direccion2, // direccion de  despacho
        CardCode: cardCode,
        PaymentGroupCode: pgc,
        SalesPersonCode: spc,
        TransportationCode: trnasp,
        U_LED_TIPDOC: ultd,
        U_LED_FORENV: ulfen,
        DocumentLines: lines,
      };
  
      // Convertir a JSON
      const jsonData = JSON.stringify(documentData);
  
// Enviar los datos al backend usando fetch
fetch("/ventas/crear_odv/", {
  method: "POST", // Método POST para enviar datos
  headers: {
    "Content-Type": "application/json", // Indica que el cuerpo es JSON
    "X-CSRFToken": getCSRFToken(), // Obtener el token CSRF si es necesario en Django
  },
  body: jsonData, // Datos en formato JSON
})
  .then((response) => {
    if (response.ok) {
      return response.json(); // Procesar respuesta si es exitosa
    } else {
      throw new Error("Error en la creación del documento");
    }
  })
  .then((data) => {
    console.log("Documento creado exitosamente:", data);

    const numeroCotizacion = document.getElementById("numero_orden");
    const esActualizacion =
      numeroCotizacion && numeroCotizacion.getAttribute("data-docentry");
    const vendedor = document.getElementById("vendedor_data");

    // Determinar si es creación o actualización
    const titulo = esActualizacion
      ? "Orden Venta actualizada"
      : "Orden Venta creada";
    const mensaje = esActualizacion
      ? `La Orden Venta fue actualizada exitosamente. N°: ${data.docNum}`
      : `La Orden Venta fue creada exitosamente. N°: ${data.docNum}`;

    if (data.success) {
      Swal.fire({
        icon: "success",
        title: titulo,
        text: mensaje,
        confirmButtonText: "Aceptar",
      }).then(() => {
        // Redirigir solo después de aceptar la alerta
        window.location.href = `/ventas/ordenesVentas/?docentry=${data.docEntry}`;
      });

      if (numeroCotizacion) {
        numeroCotizacion.textContent = `${data.docNum}`;
        numeroCotizacion.setAttribute("data-docEntry", `${data.docEntry}`);
      }

      if (data.salesPersonCode !== undefined) {
        vendedor.textContent = `${data.salesPersonName}`;
        vendedor.setAttribute("data-codeVen", `${data.salesPersonCode}`);
      }

      // 🔥 Nueva funcionalidad: Actualizar stock después de la ODV
      const productRows = document.querySelectorAll(".product-row");
      productRows.forEach((row) => {
        const productoCodigo = row.querySelector("[name='sku_producto']").innerText;
        const producto = new Producto(null, productoCodigo); // Crear instancia de Producto
        producto.actualizarStock(row); // Llamar la función para actualizar stock
        console.log("Stock actualizado para:", productoCodigo);
      });
    } else {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: `Error al crear la Orden Venta: ${data.error}`,
        confirmButtonText: "Aceptar",
      });
    }
  })
  .catch((error) => {
    console.error("Hubo un error al crear el documento:", error);
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Hubo un problema en el proceso. Inténtalo de nuevo.",
      confirmButtonText: "Aceptar",
    });
  })
  .finally(() => {
    // Ocultar el overlay en cualquier caso
    hideLoadingOverlay();
  });

// Función para obtener el token CSRF (si usas Django)
function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
    }
 
  });
  