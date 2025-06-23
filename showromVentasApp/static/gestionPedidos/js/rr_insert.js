// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function () {

    // Asignar el evento 'click' a ambos botones
    document.getElementById("saveButton").addEventListener("click", submitForm);
    document.getElementById("saveButton2").addEventListener("click", submitForm);

    function submitForm() {
        showLoadingOverlay();
        // Capturar los datos del documento
        const fechaSolo = new Date().toISOString().split('T')[0]; // Salida en formato YYYY-MM-DD


        const docNum = document.getElementById("numero_orden").textContent; //listo

        let id_documento = document.getElementById("id_documento").textContent

        // enviar null si el documento no tiene un id 

        if (id_documento === "None") {
            id_documento = null;
        } else {
            id_documento = id_documento;
        }

        const docEntry = document.getElementById("numero_orden").getAttribute("data-docEntry")
        const docTotal = document.getElementById("total_bruto").getAttribute("data-total-bruto");
        const docDate = fechaSolo; //listo 
        const fechaentrega = document.getElementById("fecha_entrega").value;
        const taxDate = fechaSolo; // listo
        const rut = document.getElementById("inputCliente").getAttribute("data-codigoSN"); //listo
        const cardCode = rut;//listo
        const pgc = -1; //listo
        const spcInt = document.getElementById("vendedor_data").getAttribute("data-codeVen"); //listo
        const spc = parseInt(spcInt, 10); //listo Convertir a entero con base 10
        const trnasp = document.getElementById("tipoEntrega-1").value; //listo
        const ulfen = 1; //document.getElementById("uledforenv").value;
        const referencia = document.getElementById("referencia").value; //listo
        const observaciones = document.getElementById("Observaciones-1").value; //selecionando observaciones por fila de producto por medio de id

        // Obtener el elemento <select>
        const selectElement = document.getElementById("direcciones_despacho");
        const direccion2 = selectElement.value;

        console.log("Valor seleccionado:", direccion2);

        const selectElement2 = document.getElementById("direcciones_facturacion");
        const direccion = selectElement2.value;
        console.log("Valor seleccionado:", direccion);

        const contactoCliente = document.getElementById("contactos_cliete");
        const contacto = contactoCliente.value;

        console.log('contacto seleccionado:', contacto);



        const tipoDocElement = document.querySelector("[name='tipoDocTributario']:checked");
        if (!tipoDocElement) {
            console.error("No se seleccionó un tipo de documento tributario.");
            return;
        }
        const ultd = tipoDocElement.value; //listo

        console.log('Fecha del documento:', docDate);
        console.log('tipo de entrega:', trnasp);
        // Captura las líneas del documento
        const lines = [];

        // Selecciona todas las líneas de cada producto
        const productRows = document.querySelectorAll('.product-row');

        productRows.forEach((row, index) => {
            const itemCode = row.querySelector("[name='sku_producto']").innerText;
            const quantity = row.querySelector("[name='cantidad']").value;
            //const shipDate = row.querySelector("[name='fecha_envio']").value;
            const discount = row.querySelector("#agg_descuento").value;
            // Capturar el valor seleccionado en el select de bodega
            const bodegaSelect = row.querySelector(".bodega-select"); // Selecciona el <select> dentro de la fila
            const comentarios = row.querySelector("#comentarios-1").value; //selecionando comentarios por fila de producto por medio de id
            const inputPrecioVenta = row.querySelector('#precio_venta2'); 

            const warehouseCode = bodegaSelect ? bodegaSelect.value : null;
            const unitPrice = row.querySelector("#precio_venta2").value; // Capturar el precio de venta del producto
            const price_line = row.querySelector("#precio_Venta").textContent.trim();

            const costingCode = warehouseCode; //capturar bodega
            const cogsCostingCode = warehouseCode;
            const costingCode2 = "AV";
            const cogsCostingCode2 = "AV";

            console.log('warehouseCode:', warehouseCode);




            // Crea un objeto con los datos de la línea
            const line = {
                "LineNum": index,
                "ItemCode": itemCode,
                "Quantity": parseFloat(quantity),
                "UnitePrice": parseFloat(unitPrice),
                "ShipDate": fechaentrega, //shipDate,
                "line_price": price_line, // precio de venta
                "FreeText": comentarios,
                "DiscountPercent": parseFloat(discount),//pendiente porcentaje de descuento
                "WarehouseCode": warehouseCode, //pendiente bodega
                "CostingCode": costingCode, // Pendiente código de sucursal, lc, Ph, gr, rs
                "ShippingMethod": trnasp, // entrega en tienda, retiro en tienda, despacho a domicilio
                "COGSCostingCode": cogsCostingCode, //pendiente 
                "CostingCode2": costingCode2, // Pendiente código de sucursal, lc, Ph, gr, rs
                "COGSCostingCode2": cogsCostingCode2,
                "Price": parseFloat(inputPrecioVenta.value)
            };
            lines.push(line);
        });

        // Crea el objeto final que será enviado en formato JSON
        const documentData = {
            "DocNum": docNum,
            "id_documento": id_documento, // ID del documento
            "DocEntry": docEntry,
            "DocDate": docDate,
            'DocTotal': docTotal,
            "NumAtCard": referencia,
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

                    const id_documento = document.getElementById("id_documento");
                    // Actualizar el ID del documento si es necesario
                    if (id_documento) {
                        id_documento.textContent = data.id_solicitud; // Actualizar el ID del documento
                    }
                    
                    // Mostrar el mensaje dinámico en el popup
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

                    // actualizar los datos del vendedor 

                    const vendedorData = data.salesPersonCode;

                    if (vendedorData != undefined) {
                        vendedor.textContent = `${data.salesPersonName}`;
                        vendedor.setAttribute('data-codeVen', `${data.salesPersonCode}`);
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

