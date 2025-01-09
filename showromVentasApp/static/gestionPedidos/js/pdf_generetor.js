document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("generarPDF").addEventListener("click", crearPDF);

    function crearPDF() {
        showLoadingOverlay();

        console.log("Generando PDF...");

        // Obtener valores iniciales
        const fechaSolo = new Date().toISOString().split('T')[0];
        console.log("Fecha actual (ISO):", fechaSolo);

        const rut = document.getElementById("inputCliente").getAttribute("data-rut");
        console.log("RUT del cliente:", rut);

        const docNum = document.getElementById("numero_cotizacion").textContent.trim();
        console.log("Número de cotización:", docNum);

        const docDate = fechaSolo;
        console.log("Fecha del documento:", docDate);

        const docDueDate = document.getElementById("docDueDate").textContent.trim();
        console.log("Fecha de vencimiento:", docDueDate);

        const codigoVendedor = document.getElementById("vendedor_data").getAttribute("data-codeVen");
        console.log("Código del vendedor:", codigoVendedor);

        // Construir líneas del documento
        const lines = [];
        const productRows = document.querySelectorAll('.product-row');
        console.log("Número de filas de productos:", productRows.length);

        productRows.forEach((row, index) => {
            const itemCode = row.querySelector("[name='sku_producto']").innerText.trim();
            const name = row.querySelector("[name='nombre_producto']").innerText.trim();
            const quantity = row.querySelector("[name='cantidad']").value.trim();
            const porcentaje_descuento = row.querySelector("#agg_descuento").value.trim();
            const discount = row.querySelector("#Precio_Descuento").value.trim();
            const total = row.querySelector("[name='total']").innerText.trim();

            console.log(`Producto ${index + 1} - SKU:`, itemCode);
            console.log(`Producto ${index + 1} - Nombre:`, name);
            console.log(`Producto ${index + 1} - Cantidad:`, quantity);
            console.log(`Producto ${index + 1} - Descuento %:`, porcentaje_descuento);
            console.log(`Producto ${index + 1} - Descuento $:`, discount);
            console.log(`Producto ${index + 1} - Subtotal Neto:`, total);

            const line = {
                "LineNum": index,
                "sku": itemCode,
                "descripcion": name,
                "cantidad": parseFloat(quantity),
                "porcentaje_descuento": parseFloat(porcentaje_descuento),
                "descuento": parseFloat(discount),
                "subtotal_neto": parseFloat(total),
            };
            lines.push(line);
        });

        const documentData = {
            "numero": docNum,
            "fecha": docDate,
            "valido_hasta": docDueDate,
            "rut": rut,
            "vendedor": codigoVendedor,
            "DocumentLines": lines
        };

        console.log("Datos del documento:", documentData);

        // Convertir a JSON
        const jsonData = JSON.stringify(documentData);
        console.log("JSON generado:", jsonData);

        const id = 1; // Ajusta según tu lógica para el ID de cotización

        fetch(`/ventas/cotizacion/${id}/pdf/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Asegúrate de tener configurado CSRF correctamente
            },
            body: jsonData
        })


            .then(response => {
                console.log("Respuesta del servidor:", response);
                if (response.ok) return response.blob(); // PDF como blob
                throw new Error('Error al generar el PDF');
            })
            .then(blob => {
                // Crear un enlace para descargar el PDF
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `cotizacion_${docNum}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                hideLoadingOverlay();
                console.log("PDF generado y descargado con éxito.");
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoadingOverlay();
                alert('Hubo un error al generar el PDF.');
            });

        console.log("URL de la solicitud:", `/ventas/cotizacion/${id}/pdf/`);

    }
});
