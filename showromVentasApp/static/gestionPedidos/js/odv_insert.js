// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("saveButton").addEventListener("click", submitForm);
    
    function submitForm() {
        // Capturar los datos del documento
        const fechaSolo = new Date().toISOString().split('T')[0]; // Salida en formato YYYY-MM-DD
    
    
        const docNum = document.getElementById("numero_orden").textContent; //listo
        const docEntry = document.getElementById("numero_orden").getAttribute("data-docEntry")
        const docDate = fechaSolo; //listo 
        const fechaentrega = document.getElementById("fecha_entrega").value; //listo
        const taxDate = fechaSolo; // listo
        const rut = document.getElementById("inputCliente").getAttribute("data-codigoSN"); //listo
        const cardCode = rut;//listo
        const pgc = -1; //listo
        //const spcInt  = document.getElementById("vendedor_data").getAttribute("data-codeVen"); //listo
        //const spc  = parseInt(spcInt, 10); //listo Convertir a entero con base 10
        const trnasp = document.getElementById("tipoEntrega-1").value; //listo
        const ulfen = 1; //document.getElementById("uledforenv").value;
    
        const tipoDocElement = document.querySelector("[name='tipoDocTributario']:checked");
        if (!tipoDocElement) {
            console.error("No se seleccionó un tipo de documento tributario.");
            return;
        }
        const ultd = tipoDocElement.value; //listo
    
        // Captura las líneas del documento
        const lines = [];
    
        // Selecciona todas las líneas de cada producto
        const productRows = document.querySelectorAll('.product-row');
        
        productRows.forEach((row, index) => {
            const itemCode = row.querySelector("[name='sku_producto']").innerText;
            const quantity = row.querySelector("[name='cantidad']").value;
            //const shipDate = row.querySelector("[name='fecha_envio']").value;
            const discount = row.querySelector("#agg_descuento").value;

            const bodegaSelect = row.querySelector(".bodega-select"); // Selecciona el <select> dentro de la fila
            const warehouseCode = bodegaSelect ? bodegaSelect.value : null;

            const costingCode = warehouseCode; //capturar bodega
            const cogsCostingCode = warehouseCode; //capturar bodega
            const costingCode2 = "AV"; 
            const cogsCostingCode2 = "AV"; 
            
            
    
            // Crea un objeto con los datos de la línea
            const line = {
                "LineNum": index,
                "ItemCode": itemCode,
                "Quantity": parseFloat(quantity),
                "ShipDate": fechaentrega, //shipDate,
                "DiscountPercent": parseFloat(discount),//pendiente porcentaje de descuento
                "WarehouseCode": warehouseCode, //pendiente bodega
                "CostingCode": costingCode, // Pendiente código de sucursal, lc, Ph, gr, rs
                "ShippingMethod": trnasp, // entrega en tienda, retiro en tienda, despacho a domicilio
                "COGSCostingCode": cogsCostingCode, //pendiente 
                "CostingCode2": costingCode2, // Pendiente código de sucursal, lc, Ph, gr, rs
                "COGSCostingCode2": cogsCostingCode2,
            };
            lines.push(line);
        });
    
        // Crea el objeto final que será enviado en formato JSON
        const documentData = {
            "DocNum": docNum,
            "DocEntry": docEntry, 
            "DocDate": docDate,
            "DocDueDate": fechaentrega,
            "TaxDate": taxDate,
            "CardCode": cardCode,
            "PaymentGroupCode": pgc,  
            "SalesPersonCode": 20,
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
                if (data.success) {
                    // Mostrar el número de documento y el mensaje de éxito en un popup bonito
                    Swal.fire({
                        icon: 'success',
                        title: 'Orden de Venta creada',
                        text: `Número de documento: ${data.docNum}`,
                        confirmButtonText: 'Aceptar'
                    });
    
                    const numeroCotizacion = document.getElementById('numero_cotizacion');
                    
                    if (numeroCotizacion) {
                        numeroCotizacion.textContent = `${data.docNum}`;
                    }
    
                    bloquearCampos();
    
                } else {
                    // Mostrar el mensaje de error en un popup
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: `Error al crear la cotización: ${data.error}`,
                        confirmButtonText: 'Aceptar'
                    });
                }
            })
    
    
            .catch(error => {
                console.error('Hubo un error al crear el documento:', error);
            });
        }
    
        // Función para obtener el token CSRF (si usas Django)
        function getCSRFToken() {
            return document.querySelector('[name=csrfmiddlewaretoken]').value;
        }
    });
    
        