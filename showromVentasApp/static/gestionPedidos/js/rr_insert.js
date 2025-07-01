document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("saveButton").addEventListener("click", submitForm);
    document.getElementById("saveButton2").addEventListener("click", submitForm);

    let approve = 0;

    document.getElementById("aprobar-1").addEventListener("click", function (e) {
        e.preventDefault();
        approve = 1;
        submitForm();
    });

    function submitForm() {
        showLoadingOverlay();
        const fechaSolo = new Date().toISOString().split('T')[0];
        const docNum = document.getElementById("numero_orden").textContent;
        let id_documento = document.getElementById("id_documento").getAttribute("data-id");

        if (id_documento === "None") {
            id_documento = null;
        } else {
            id_documento = id_documento;
        }

        const docEntry = document.getElementById("numero_orden").getAttribute("data-docEntry")        
        const docTotal = document.getElementById("total_bruto").getAttribute("data-total-bruto");
        const docDate = fechaSolo;
        const fechaentrega = document.getElementById("fecha_entrega").value;
        const folio_number = document.getElementById("folio_referencia").value;
        const refereciaDocentry = document.getElementById("folio_referencia").getAttribute("data-refDocEntr");
        const taxDate = fechaSolo;
        const rut = document.getElementById("inputCliente").getAttribute("data-codigoSN");
        const cardCode = rut;
        const pgc = -1;
        const spcInt = document.getElementById("vendedor_data").getAttribute("data-codeVen");
        const spc = parseInt(spcInt, 10);
        const trnasp = document.getElementById("tipoEntrega-1").value;
        const ulfen = 1;
        const referencia = document.getElementById("referencia").value; 
        const observaciones = document.getElementById("Observaciones-1").value;

        // Obtener el elemento <select>
        const selectElement = document.getElementById("direcciones_despacho");
        const direccion2 = selectElement.value;
        const selectElement2 = document.getElementById("direcciones_facturacion");
        const direccion = selectElement2.value;
        const contactoCliente = document.getElementById("contactos_cliete");
        const contacto = contactoCliente.value;

        const tipoDocElement = document.querySelector("[name='tipoDocTributario']:checked");
        if (!tipoDocElement) {
            console.error("No se seleccionó un tipo de documento tributario.");
            return;
        }
        const ultd = tipoDocElement.value;

        const lines = [];

        const productRows = document.querySelectorAll('.product-row');

        productRows.forEach((row, index) => {
            const itemCode = row.querySelector("[name='sku_producto']").innerText;
            const quantity = row.querySelector("[name='cantidad']").value;
            const discount = row.querySelector("#agg_descuento").value;
            const bodegaSelect = row.querySelector(".bodega-select");
            const comentarios = row.querySelector("#comentarios-1").value;
            const inputPrecioVenta = row.querySelector('#precio_venta2'); 
            const warehouseCode = bodegaSelect ? bodegaSelect.value : null;
            const unitPrice = row.querySelector("#precio_venta2").value;
            const price_line = row.querySelector("#precio_Venta").textContent.trim();
            const costingCode = warehouseCode;
            const cogsCostingCode = warehouseCode;
            const costingCode2 = "AV";
            const cogsCostingCode2 = "AV";
            const checkbox = row.querySelector(".estado-checkbox");  // Asegúrate que esta clase esté en cada checkbox
            const checkboxEstado = checkbox && checkbox.checked ? 1 : 0;

            const line = {
                "LineNum": index,
                "ItemCode": itemCode,
                "Quantity": parseFloat(quantity),
                "UnitePrice": parseFloat(unitPrice),
                "ShipDate": fechaentrega,
                "line_price": price_line,
                "FreeText": comentarios,
                "DiscountPercent": parseFloat(discount),
                "WarehouseCode": warehouseCode,
                "CostingCode": costingCode,
                "ShippingMethod": trnasp,
                "COGSCostingCode": cogsCostingCode,
                "CostingCode2": costingCode2,
                "COGSCostingCode2": cogsCostingCode2,
                "Price": parseFloat(inputPrecioVenta.value),
                "EstadoCheck": checkboxEstado
            };
            lines.push(line);
        });

        const documentData = {
            "DocNum": docNum,
            "id_documento": id_documento,
            "DocEntry": docEntry,
            "Folio": folio_number,
            "DocDate": docDate,
            'DocTotal': docTotal,
            "NumAtCard": referencia,
            "Comments": observaciones,
            "TaxDate": taxDate,
            "ContactPersonCode": contacto,
            "Address": direccion,
            "Address2": direccion2,
            "CardCode": cardCode,
            "PaymentGroupCode": pgc,
            "SalesPersonCode": spc,
            "U_LED_TIPDEV": trnasp,
            "U_LED_TIPDOC": ultd,
            "U_LED_FORENV": ulfen,
            "Approve": approve,
            "RefDocEntr": refereciaDocentry,
            "DocumentLines": lines
        };

        // Convertir a JSON
        const jsonData = JSON.stringify(documentData);

        // Enviar los datos al backend usando fetch
        fetch('/ventas/crear_devolucion/', {
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
                console.log('Operación exitosa:', data);
                // Puedes hacer algo aquí como redirigir al usuario o mostrar un mensaje de éxito
                if (data.success) {
                    const numeroCotizacion = document.getElementById('numero_orden');
                    const esActualizacion = numeroCotizacion && numeroCotizacion.getAttribute('data-docentry');
                    const vendedor= document.getElementById("vendedor_data")

                    // Determinar si es creación o actualización
                    const titulo = esActualizacion ? 'Devolución actualizada' : 'Devolución creada';
                    const mensaje = esActualizacion
                        ? `La Devolución fue actualizada exitosamente. N°: ${data.docNum}`
                        : `Solicitud Creada Pendiente por Aprobar. N°: ${data.id_solicitud}`; // Cambiar el mensaje según sea necesario
                        //: `La Devolución fue creada exitosamente. N°: ${data.docNum}`;
                    
                    let existe_documento = data.id_solicitud
                    // Actualizar el ID del documento si es necesario
                    if (existe_documento && existe_documento !== '') {

                        const id_documento = document.getElementById("id_documento");
                        id_documento.textContent = `Borrador: ${data.id_solicitud}`; // Actualizar el ID del documento
                        id_documento.setAttribute("data-id", data.id_solicitud); // Actualizar el atributo data-id
                    }
                    
                    // Mostrar el mensaje dinámico en el popup
                    Swal.fire({
                        icon: 'success',
                        title: data.title,
                        text: data.message,
                        confirmButtonText: 'Aceptar'
                    });

                    if (numeroCotizacion) {
                        numeroCotizacion.textContent = `${data.docNum}`;
                        numeroCotizacion.setAttribute('data-docEntry', `${data.docEntry}`);
                    }

                    // actualizar los datos del vendedor 

                    const vendedorData = data.salesPersonCode;

                    if (vendedorData != undefined) {
                        vendedor.textContent = `${data.salesPersonName}`;
                        vendedor.setAttribute('data-codeVen', `${data.salesPersonCode}`);

                        const id_documento = document.getElementById("id_documento");

                        id_documento.textContent = ""; // Actualizar el ID del documento
                        id_documento.setAttribute("data-id", ""); // Actualizar el atributo data-id

                    }

                    console.log("Numero de cotizacion:", data.docNum);
                    console.log("Numero de docEntry:", data.docEntry);

                    bloquearCampos();

                } else {
                    // Mostrar el mensaje de error en un popup
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: `Error al realizar la operación: ${data.error}`,
                        confirmButtonText: 'Aceptar'
                    });
                }
            })
            .catch(error => {
                console.error('Hubo un error durante la operación:', error);
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

