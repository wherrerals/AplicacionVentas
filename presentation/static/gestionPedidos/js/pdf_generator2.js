document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("generarPDF").addEventListener("click", crearPDF);

    function crearPDF() {
        showLoadingOverlay();

        console.log("Generando PDF...");

        // Obtener valores iniciales
        const fechaSolo = new Date().toISOString().split('T')[0];
        const fechaObj = new Date(fechaSolo);
        fechaObj.setDate(fechaObj.getDate() + 9);
        const valido_hasta = fechaObj.toISOString().split('T')[0];
        const rut = document.getElementById("inputCliente").getAttribute("data-codigosn");
        const docNum = document.getElementById("numero_orden").textContent.trim();
        const docDate = fechaSolo;
        const codigoVendedor = document.getElementById("vendedor_data").getAttribute("data-codeVen");
        const totalNeto = document.querySelector("#total_neto").textContent;
        const ivaGeneral = document.querySelector("#iva").textContent;
        const totalbruto = document.querySelector("#total_bruto").textContent;
        const selectElement = document.getElementById("direcciones_despacho");
        const direccion2 = selectElement.value;
        const contactoCliente = document.getElementById("contactos_cliete");
        const contacto = contactoCliente.value;
        const sucursal = document.getElementById("sucursal").textContent.trim();
        const observaciones = document.getElementById("Observaciones-1").value;
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

            lines.push(line);
        });

        const documentData = {
            "tipo_documento": "S. Devolución",
            "numero": docNum,
            "fecha": docDate,
            "valido_hasta": valido_hasta,
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

        const id = docNum;
        ; // Ajusta según tu lógica para el ID de cotización

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


