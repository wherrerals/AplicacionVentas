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

        const docNum = document.getElementById("numero_orden").textContent.trim();
        console.log("Número de cotización:", docNum);

        const docDate = fechaSolo;
        console.log("Fecha del documento:", docDate);

        const codigoVendedor = document.getElementById("vendedor_data").getAttribute("data-codeVen");
        console.log("Código del vendedor:", codigoVendedor);

        const totalNeto = document.querySelector("#total_neto").textContent;
        const ivaGeneral = document.querySelector("#iva").textContent;
        const totalbruto = document.querySelector("#total_bruto").textContent;

        const selectElement = document.getElementById("direcciones_despacho");
        const direccion2 = selectElement.value;

        const contactoCliente = document.getElementById("contactos_cliete");
        const contacto = contactoCliente.value;
        const sucursal = document.getElementById("sucursal").textContent.trim();
        const observaciones = document.getElementById("Observaciones-1").value;

        // Construir líneas del documento
        const lines = [];
        const productRows = document.querySelectorAll('.product-row');
        console.log("Número de filas de productos:", productRows.length);

        productRows.forEach((row, index) => {
            const itemCode = row.querySelector("[name='sku_producto']").innerText.trim();
            const name = row.querySelector("[name='nombre_producto']").innerText.trim();
            const quantity = row.querySelector("[name='cantidad']").value.trim();
            const price = row.querySelector("[name='precio_venta']").textContent;
            const porcentaje_descuento = row.querySelector("#agg_descuento").value.trim();
            const discountspan = row.querySelector("#Precio_Descuento").textContent;
            const totalspan = row.querySelector("#precio_Venta").textContent;
            const comentarios = row.querySelector("#comentarios-1").value;
            const img = row.querySelector("#img_productox").src;

            const total = totalspan;
            const discount = discountspan;

            const line = {
                "LineNum": index,
                "sku": itemCode,
                "imagen": img,
                "comentarios": comentarios,
                "descripcion": name,
                "cantidad": quantity,
                "porcentaje_descuento": porcentaje_descuento,
                "descuento": discount,
                "precio_unitario": price,
                "subtotal_neto": total,
            };

            console.log("Línea de producto:", line);
            lines.push(line);
        });

        const documentData = {
            "numero": docNum,
            "fecha": docDate,
            "valido_hasta": docDate,
            "rut": rut,
            "vendedor": codigoVendedor,
            "DocumentLines": lines,
            "totalbruto": totalbruto,
            "iva": ivaGeneral,
            "totalNeto": totalNeto,
            "direccion": direccion2,
            "contacto": contacto,
            "sucursal": sucursal,
            "observaciones": observaciones,
        };

        console.log("Datos del documento:", documentData);

        // Convertir a JSON
        const jsonData = JSON.stringify(documentData);
        console.log("JSON generado:", jsonData);

        const id = 1; // Ajusta según tu lógica para el ID de cotización

        fetch(`/ventas/generar_cotizacion_pdf/${id}/pdf/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(documentData)
        })
        .then(response => response.json())
        .then(data => {
            const taskId = data.task_id;
            console.log("Tarea lanzada. ID de la tarea:", taskId);

            const interval = setInterval(() => {
                fetch(`/ventas/verificar_estado_pdf/${taskId}/`)
                    .then(response => {
                        // Comprobar el tipo de contenido antes de procesar la respuesta
                        const contentType = response.headers.get("content-type");
                        if (contentType && contentType.includes("application/pdf")) {
                            // Es un PDF, detener el intervalo y procesarlo
                            clearInterval(interval);
                            hideLoadingOverlay();
                            return response.blob();
                        } else if (contentType && contentType.includes("application/json")) {
                            // Es un JSON, procesarlo como antes
                            return response.json();
                        } else {
                            // Tipo de contenido desconocido, intentar como JSON primero
                            return response.json().catch(() => response.blob());
                        }
                    })
                    .then(data => {
                        if (data instanceof Blob) {
                            // Es un PDF, proceder a la descarga
                            const url = window.URL.createObjectURL(data);
                            const a = document.createElement("a");
                            a.href = url;
                            a.download = `cotizacion_${docNum}.pdf`;
                            document.body.appendChild(a);
                            a.click();
                            a.remove();
                            clearInterval(interval);
                            hideLoadingOverlay();
                            console.log("PDF generado y descargado con éxito.");
                        } else if (data.status === 'pending') {
                            // Tarea aún en proceso
                            console.log("PDF aún en proceso...");
                        } else if (data.status === 'failed') {
                            // La tarea falló
                            clearInterval(interval);
                            hideLoadingOverlay();
                            console.error("Error en la generación del PDF:", data.error);
                            alert('Hubo un error al generar el PDF: ' + data.error);
                        } else {
                            // Otro estado, posiblemente completado pero no es un PDF directo
                            console.log("Estado de la tarea:", data.status);
                        }
                    })
                    .catch(error => {
                        console.error('Error al verificar el estado o descargar el PDF:', error);
                        clearInterval(interval);
                        hideLoadingOverlay();
                        alert('Hubo un error al procesar la respuesta del servidor.');
                    });
            }, 2000);
        })
        .catch(error => {
            console.error('Error al lanzar la tarea:', error);
            hideLoadingOverlay();
            alert('Hubo un error al generar el PDF.');
        });
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
});