document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("generarPDF").addEventListener("click", crearPDF);

    function crearPDF() {
        showLoadingOverlay();

        console.log("Generando PDF...");

        // Obtener valores iniciales
        const fechaSolo = new Date().toISOString().split('T')[0];
        console.log("Fecha actual (ISO):", fechaSolo);

        const rut = document.getElementById("inputCliente").getAttribute("data-codigosn");
        console.log("RUT del cliente:", rut);

        const docNum = document.getElementById("numero_cotizacion").textContent.trim();
        console.log("Número de cotización:", docNum);

        const docDate = fechaSolo;
        console.log("Fecha del documento:", docDate);

        const docDueDate = document.getElementById("docDueDate").textContent.trim();
        console.log("Fecha de vencimiento:", docDueDate);

        const codigoVendedor = document.getElementById("vendedor_data").getAttribute("data-codeVen");
        console.log("Código del vendedor:", codigoVendedor);

        const totalNeto = document.querySelector("#total_neto").textContent;


        const ivaGeneral = document.querySelector("#iva").textContent;


        const totalbruto = document.querySelector("#total_bruto").textContent;


        

        // Construir líneas del documento
        const lines = [];
        const productRows = document.querySelectorAll('.product-row');
        console.log("Número de filas de productos:", productRows.length);

        productRows.forEach((row, index) => {
            const itemCode = row.querySelector("[name='sku_producto']").innerText.trim();
            const name = row.querySelector("[name='nombre_producto']").innerText.trim();
            const quantity = row.querySelector("[name='cantidad']").value.trim();
            const porcentaje_descuento = row.querySelector("#agg_descuento").value.trim();
            const discountspan = row.querySelector("#Precio_Descuento").textContent;
            const totalspan = row.querySelector("#precio_Venta").textContent;
            // capturar imagen de etiqueta imagen con id img_productox
            const img = row.querySelector("#img_productox").src;

            const total = parseFloat(totalspan);
            const discount = parseFloat(discountspan);

            const line = {
                "LineNum": index,
                "sku": itemCode,
                "imagen": img,
                "descripcion": name,
                "cantidad": quantity,
                "porcentaje_descuento": porcentaje_descuento,
                "descuento": discount,
                "subtotal_neto": total,
            };

            console.log("Línea de producto:", line);
            lines.push(line);
        });

        const documentData = {
            "numero": docNum,
            "fecha": docDate,
            "valido_hasta": docDueDate,
            "rut": rut,
            "vendedor": codigoVendedor,
            "DocumentLines": lines,
            "totalbruto": totalbruto,
            "iva": ivaGeneral,
            "totalNeto": totalNeto
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

    // Función para obtener el token CSRF (si usas Django)
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});


