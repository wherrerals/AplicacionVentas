document.querySelectorAll("#duplicar-ODV, #duplicar-Cotizacion, #duplicar-Solicitud").forEach((button) => {
    button.addEventListener("click", function (event) {
        const botonPresionado = event.target.id; // "duplicar-ODV", "duplicar-Cotizacion", o "duplicar-Solicitud"
        const folio_element = document.getElementById("folio_cotizacion");
        const numero_cotizacion = document.getElementById("numero_cotizacion");
        let folio = 0
        let docEntry = 0;

        if (numero_cotizacion) {
            // Obtener el valor del atributo data-docentry
            docEntry = numero_cotizacion.getAttribute("data-docentry");
            console.log("DocEntry obtenido:", docEntry);
        } else {
            console.error("No se encontró el elemento con id 'numero_cotizacion'. Asegúrate de que exista en el DOM.");
        }

        if (folio_element){
            folio = folio_element.textContent.trim(); // Obtener el texto del elemento y eliminar espacios

            console.log("Folio obtenido:", folio);
        }else{
            console.error("No se encontró el elemento con id 'folio_cotizacion'. Asegúrate de que exista en el DOM.");
        }

        const lines = [];

        const productRows = document.querySelectorAll(".product-row");

        productRows.forEach((row) => {
            const itemCode = row.querySelector("[name='sku_producto']")?.innerText;
            const line_num = row.querySelector("#indixe_producto").getAttribute("data-linenum");
            const ItemDescription = row.querySelector("[name='nombre_producto']")?.innerText;
            const quantity = row.querySelector("[name='cantidad']")?.value;
            const discount = row.querySelector("#agg_descuento")?.value;
            const comentarios = row.querySelector("#comentarios-1")?.value;
            const warehouseSelect = row.querySelector(".bodega-select");
            const warehouseCode = warehouseSelect ? warehouseSelect.value : null;
            const docentryLinea = row.getAttribute("data-docentryLinea");
            const price = row.querySelector("[name='precio_venta']")?.innerText;

            const docDueDate = new Date().toISOString().split("T")[0];
            const trnasp = "retiro"; // o cambiar dinámicamente si hace falta

            const line = {
                ItemCode: itemCode,
                LineNum: line_num,
                ItemDescription: ItemDescription,
                Quantity: parseFloat(quantity),
                DocEntry_line: docentryLinea,
                ShipDate: docDueDate,
                FreeText: comentarios,
                DiscountPercent: parseFloat(discount),
                WarehouseCode: warehouseCode,
                CostingCode: warehouseCode,
                ShippingMethod: trnasp,
                COGSCostingCode: warehouseCode,
                Price: price,
            };

            lines.push(line);
        });

        console.log("Líneas a enviar:", lines);

        // Determina el tipo de documento
        let tipoDocumento = "";
        if (botonPresionado === "duplicar-ODV") tipoDocumento = "ODV";
        else if (botonPresionado === "duplicar-Cotizacion") tipoDocumento = "Cotizacion";
        else if (botonPresionado === "duplicar-Solicitud") tipoDocumento = "Solicitud";

        fetch("/ventas/duplicar-documento/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                DocumentLine: { value: lines },
                tipo: tipoDocumento,
                folio: folio,
                docEntry: docEntry,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Respuesta del backend:", data);
                console.log(data.lineas);
                if (data.status === "ok") {
                    sessionStorage.setItem("documentLines", JSON.stringify(data.lineas));
                    sessionStorage.setItem("tipoDocumento", tipoDocumento);

                    if (tipoDocumento === "ODV") {
                        window.location.href = `/ventas/ordenesVentas/`;
                    } else if (tipoDocumento === "Cotizacion") {
                        window.location.href = `/ventas/generar_cotizacion/`;
                    } else if (tipoDocumento === "Solicitud") {
                        const clienteElement = document.getElementById("inputCliente");
                        const fullText = clienteElement?.innerText || "";
                        const cardCode = fullText.split("C")[0].trim();  // Esto captura "76820314C"
                        
                        const folio_element = document.getElementById("folio_cotizacion");
                        const folio = folio_element ? folio_element.textContent.trim() : "";

                        // obtener tambien el data-docentry 

                        const docentry_in_folio = document.getElementById("numero_cotizacion").getAttribute("data-docentry");
                        sessionStorage.setItem("docentry_in_folio", docentry_in_folio);
                        // Puedes guardar solo esto si no necesitas más
                        sessionStorage.setItem("cardCode", cardCode);
                        sessionStorage.setItem("folio", folio);

                        // Redirigir a la siguiente vista
                        window.location.href = `/ventas/solicitudes_devolucion/`;
                    }
                } else {
                    alert("Error al duplicar el documento: " + data.message);
                }
            })
            .catch((error) => {
                console.error("Error al enviar datos:", error);
            });
    });
});


// Función CSRF sin cambios
function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + "=")) {
            return decodeURIComponent(trimmed.substring(name.length + 1));
        }
    }
    return null;
}
