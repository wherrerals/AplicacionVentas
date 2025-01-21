// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("saveButton").addEventListener("click", submitForm);

    function submitForm() {
        showLoadingOverlay();

        // Capturar los datos del documento
        const fechaSolo = new Date().toISOString().split('T')[0]; // Salida en formato YYYY-MM-DD


        const docNum = document.getElementById("numero_orden").textContent;
        const docEntry = document.getElementById("numero_orden").getAttribute("data-docEntry")
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
        console.log("Valor seleccionado:", direccion);
        const contactoCliente = document.getElementById("contactos_cliete");
        const contacto = contactoCliente.value;
        const trnasp = document.getElementById("tipoEntrega-1").value; 
        const ulfen = 1;
        const tipoDocElement = document.querySelector("[name='tipoDocTributario']:checked");
        if (!tipoDocElement) {
            console.error("No se seleccionó un tipo de documento tributario.");
            return;
        }

        // Captura las líneas del documento
        const ultd = tipoDocElement.value; 
        const lines = [];
        const productRows = document.querySelectorAll('.product-row');

        productRows.forEach((row, index) => {
            const itemCode = row.querySelector("[name='sku_producto']").innerText;
            const quantity = row.querySelector("[name='cantidad']").value;
            const discount = row.querySelector("#agg_descuento").value;
            const fechaentregaLineas = row.querySelector("#fecha_entrega_lineas").value;
            const bodegaSelect = row.querySelector(".bodega-select");
            const warehouseCode = bodegaSelect ? bodegaSelect.value : null;
            const comentarios = row.querySelector("#comentarios-1").value;
            const costingCode = warehouseCode;
            const cogsCostingCode = warehouseCode;
            const costingCode2 = "AV";
            const cogsCostingCode2 = "AV";

            const line = {
                "LineNum": index,
                "ItemCode": itemCode,
                "Quantity": parseFloat(quantity),
                "ShipDate": fechaentregaLineas,
                "FreeText": comentarios,
                "DiscountPercent": parseFloat(discount),
                "WarehouseCode": warehouseCode,
                "CostingCode": costingCode,
                "ShippingMethod": trnasp,
                "COGSCostingCode": cogsCostingCode,
                "CostingCode2": costingCode2,
                "COGSCostingCode2": cogsCostingCode2,
            };
            lines.push(line);
        });

        // Crea el objeto final que será enviado en formato JSON
        const documentData = {
            "DocNum": docNum,
            "DocEntry": docEntry,
            "DocDate": docDate,
            "NumAtCard": referencia,
            "DocDueDate": fechaentrega,
            "Comments": observaciones,
            "TaxDate": taxDate,
            "ContactPersonCode": contacto,
            "Address": direccion, // direccion de facturacion
            "Address2": direccion2, // direccion de  despacho
            "CardCode": cardCode,
            "PaymentGroupCode": pgc,
            "SalesPersonCode": spc,
            "TransportationCode": trnasp,
            "U_LED_TIPDOC": ultd,
            "U_LED_FORENV": ulfen,
            "DocumentLines": lines
        };

        // Convertir a JSON
        const jsonData = JSON.stringify(documentData);

        // Enviar los datos al backend usando fetch
        fetch('/ventas/crear_odv/', {
            method: 'POST', // Método POST para enviar datos
            headers: {
                'Content-Type': 'application/json', // Indica que el cuerpo es JSON
                'X-CSRFToken': getCSRFToken() // Obtener el token CSRF si es necesario en Django
            },
            body: jsonData // Datos en formato JSON
        })

            .then(response => {
                if (response.ok) {
                    return response.json(); // Procesar respuesta si es exitosa
                } else {
                    throw new Error('Error en la creación del documento');
                }
            })
            .then(data => {
                console.log('Documento creado exitosamente:', data);
                // Puedes hacer algo aquí como redirigir al usuario o mostrar un mensaje de éxito

                const numeroCotizacion = document.getElementById('numero_orden');
                const esActualizacion = numeroCotizacion && numeroCotizacion.getAttribute('data-docentry');

                // Determinar si es creación o actualización
                const titulo = esActualizacion ? 'Orden Venta actualizada' : 'Orden Venta creada';
                const mensaje = esActualizacion
                    ? `La Orden Venta fue actualizada exitosamente. N°: ${data.docNum}`
                    : `La Orden Venta fue creada exitosamente. N°: ${data.docNum}`;

                if (data.success) {
                    // Mostrar el número de documento y el mensaje de éxito en un popup bonito
                    Swal.fire({
                        icon: 'success',
                        title: titulo,
                        text: mensaje,
                        confirmButtonText: 'Aceptar'
                    });


                    if (numeroCotizacion) {
                        numeroCotizacion.textContent = `${data.docNum}`;
                        numeroCotizacion.setAttribute('data-docEntry', `${data.docEntry}`);
                    }

                    bloquearCampos();

                } else {
                    // Mostrar el mensaje de error en un popup
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: `Error al crear la Orden Venta: ${data.error}`,
                        confirmButtonText: 'Aceptar'
                    });
                }
            })


            .catch(error => {
                console.error('Hubo un error al crear el documento:', error);

            })

            .finally(() => {
                // Ocultar el overlay en cualquier caso
                hideLoadingOverlay();
            });
    }


    // Función para obtener el token CSRF (si usas Django)
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});

