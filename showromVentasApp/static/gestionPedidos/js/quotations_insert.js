// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function() {

document.getElementById("saveButton").addEventListener("click", submitForm);

function submitForm() {
    // Capturar los datos del documento
    const fechaSolo = new Date().toISOString().split('T')[0]; // Salida en formato YYYY-MM-DD

    const docDate = fechaSolo;
    const docDueDate = document.getElementById("docDueDate").textContent;
    const taxDate = fechaSolo;
    const rut = document.getElementById("inputCliente").getAttribute("data-rut");
    const cardCode = rut + "C";
    const pgc = -1;
    const spc = 41; //document.getElementById("salesPersonCode").value;
    const trnasp = 1; //document.getElementById("transportationCode").value;
    const ultv = 1; //document.getElementById("uledtipoventa").value;
    const ultd = "RESE"; //document.getElementById("uledtipodoc").value;
    const ulfen = 1; //document.getElementById("uledforenv").value;

    console.log('Fecha del documento:', docDate);
    console.log('Fecha de vencimiento del documento:', docDueDate);

    // Captura las líneas del documento
    const lines = [];

    // Selecciona todas las líneas de cada producto
    const productRows = document.querySelectorAll('.product-row');
    
    productRows.forEach((row, index) => {
        const itemCode = row.querySelector("[name='sku_producto']").innerText;
        const quantity = row.querySelector("[name='cantidad']").value;
        //const shipDate = row.querySelector("[name='fecha_envio']").value;
        const discount = row.querySelector("[name='precio_lista']").value;
        const warehouseCode = "GR"; //row.querySelector("[name='Bodega']").value;
        const costingCode = "LC"; //row.querySelector("[name='costingCode']").value;
        const shippingMethod = 2; //row.querySelector("[name='shippingMethod']").value;
        const cogsCostingCode = "LC";//row.querySelector("[name='cogsCostingCode']").value;
        const costingCode2 = "AV";//row.querySelector("[name='costingCode2']").value;
        const cogsCostingCode2 = "AV"; //row.querySelector("[name='cogsCostingCode2']").value;

        // Crea un objeto con los datos de la línea
        const line = {
            "LineNum": index,
            "ItemCode": itemCode,
            "Quantity": parseFloat(quantity),
            "ShipDate": docDueDate, //shipDate,
            "DiscountPercent": parseFloat(discount),
            "WarehouseCode": warehouseCode,
            "CostingCode": costingCode,
            "ShippingMethod": shippingMethod,
            "COGSCostingCode": cogsCostingCode,
            "CostingCode2": costingCode2,
            "COGSCostingCode2": cogsCostingCode2,
        };
        lines.push(line);
    });

    // Crea el objeto final que será enviado en formato JSON
    const documentData = {
        "DocDate": docDate,
        "DocDueDate": docDueDate,
        "TaxDate": taxDate,
        "CardCode": cardCode,
        "PaymentGroupCode": pgc,  
        "SalesPersonCode": spc,
        "TransportationCode": trnasp,
        "U_LED_TIPVTA": ultv,
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
            console.log('Documento creado exitosamente:', data);
            // Puedes hacer algo aquí como redirigir al usuario o mostrar un mensaje de éxito
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