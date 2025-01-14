// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function() {

  // Asignar el evento 'click' a ambos botones
  document.getElementById("saveButton").addEventListener("click", submitForm);
  document.getElementById("saveButton2").addEventListener("click", submitForm);
  
function submitForm() {
    showLoadingOverlay();
    // Capturar los datos del documento
    const fechaSolo = new Date().toISOString().split('T')[0]; // Salida en formato YYYY-MM-DD


    const docNum = document.getElementById("numero_cotizacion").textContent; //listo
    const docEntry = document.getElementById("numero_cotizacion").getAttribute("data-docEntry")
    const docDate = fechaSolo; //listo 
    const docDueDate = document.getElementById("docDueDate").textContent; //listo
    const taxDate = fechaSolo; // listo
    const rut = document.getElementById("inputCliente").getAttribute("data-codigoSN"); //listo
    const cardCode = rut;//listo
    const pgc = -1; //listo
    const spcInt  = document.getElementById("vendedor_data").getAttribute("data-codeVen"); //listo
    const spc  = parseInt(spcInt, 10); //listo Convertir a entero con base 10
    const trnasp = document.getElementById("tipoEntrega-1").value; //listo
    const direccion2 = document.getElementById("direcciones_despacho").value;
    const direccion = document.getElementById("direcciones_despacho").value;
    const ulfen = 1; //document.getElementById("uledforenv").value;
    const referencia = document.getElementById("referencia").value; //listo
    const observaciones = document.getElementById("Observaciones-1").value; //selecionando observaciones por fila de producto por medio de id


    const tipoDocElement = document.querySelector("[name='tipoDocTributario']:checked");
    if (!tipoDocElement) {
        console.error("No se seleccionó un tipo de documento tributario.");
        return;
    }
    const ultd = tipoDocElement.value; //listo

    console.log('Fecha del documento:', docDate);
    console.log('Fecha de vencimiento del documento:', docDueDate);
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
        const warehouseCode = bodegaSelect ? bodegaSelect.value : null;

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
            "ShipDate": docDueDate, //shipDate,
            "FreeText": comentarios,
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
        "NumAtCard": referencia,
        "DocDueDate": docDueDate,
        "Comments": observaciones,
        "TaxDate": taxDate,
        "Address": direccion,
        "Address2": direccion2,
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
        fetch('/ventas/crear_cotizacion/', {
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
                const numeroCotizacion = document.getElementById('numero_cotizacion');
                const esActualizacion = numeroCotizacion && numeroCotizacion.getAttribute('data-docentry');
        
                // Determinar si es creación o actualización
                const titulo = esActualizacion ? 'Cotización actualizada' : 'Cotización creada';
                const mensaje = esActualizacion 
                    ? `La cotización fue actualizada exitosamente. N°: ${data.docNum}` 
                    : `La cotización fue creada exitosamente. N°: ${data.docNum}`;
        
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

    