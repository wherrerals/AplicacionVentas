document.querySelectorAll("#duplicar-ODV, #duplicar-Cotizacion").forEach((button) => {
    button.addEventListener("click", function (event) {
        const botonPresionado = event.target.id; // "duplicar-ODV" o "duplicar-Cotizacion"

        const lines = [];

        const productRows = document.querySelectorAll(".product-row");

        productRows.forEach((row) => {
            const itemCode = row.querySelector("[name='sku_producto']")?.innerText;
            const ItemDescription = row.querySelector("[name='nombre_producto']")?.innerText;
            const quantity = row.querySelector("[name='cantidad']")?.value;
            const discount = row.querySelector("#agg_descuento")?.value;
            const comentarios = row.querySelector("#comentarios-1")?.value;
            const warehouseSelect = row.querySelector(".bodega-select");
            const warehouseCode = warehouseSelect ? warehouseSelect.value : null;
            const docentryLinea = row.getAttribute("data-docentryLinea");

            const docDueDate = new Date().toISOString().split("T")[0];
            const trnasp = "retiro"; // o cambiar dinámicamente si hace falta

            const line = {
                ItemCode: itemCode,
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
            };

            lines.push(line);
        });

        console.log("Líneas a enviar:", lines);

        // Puedes usar esta variable si el backend necesita saber qué botón se presionó
        const tipoDocumento = botonPresionado === "duplicar-ODV" ? "ODV" : "Cotizacion";

        fetch("/ventas/duplicar-documento/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                DocumentLine: { value: lines },
                tipo: tipoDocumento, // lo mandas si el backend lo necesita
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Respuesta del backend:", data);
                console.log(data.lineas);
                if (data.status === "ok") {
                    sessionStorage.setItem("documentLines", JSON.stringify(data.lineas));
                    if (botonPresionado === "duplicar-ODV") {
                        sessionStorage.setItem("tipoDocumento", "ODV");
                        window.location.href = `/ventas/ordenesVentas/`;
                    }
                    if (botonPresionado === "duplicar-Cotizacion") {
                        sessionStorage.setItem("tipoDocumento", "Cotizacion");
                        window.location.href = `/ventas/generar_cotizacion/`;
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
