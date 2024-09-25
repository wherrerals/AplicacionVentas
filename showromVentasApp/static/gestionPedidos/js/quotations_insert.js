// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function() {

document.getElementById("saveButton").addEventListener("click", submitForm);

function submitForm() {
    // Capturar los datos del documento
    const fechaSolo = new Date().toISOString().split('T')[0]; // Salida en formato YYYY-MM-DD

    const docDate = fechaSolo;
    const docDueDate = document.getElementById("docDueDate").value;
    const taxDate = fechaSolo;
    const cardCode = document.getElementById("cardCode").value;
    const pgc = document.getElementById("paymentGroupCode").value;
    const spc = document.getElementById("salesPersonCode").value;
    const trnasp = document.getElementById("transportationCode").value;
    const ultv = document.getElementById("uledtipoventa").value;
    const ultd = document.getElementById("uledtipodoc").value;
    const ulfen = document.getElementById("uledforenv").value;


    // Captura las líneas del documento
    const lines = [];

    // Selecciona todas las líneas de cada producto
    const productRows = document.querySelectorAll('.product-row');
    
    productRows.forEach((row, index) => {
        const itemCode = row.querySelector("[name='sku_producto']").innerText;
        const quantity = row.querySelector("[name='cantidad']").value;
        const shipDate = row.querySelector("[name='fecha_envio']").value;
        const discount = row.querySelector("[name='precio_lista']").value;
        const warehouseCode = row.querySelector("[name='Bodega']").value;
        const costingCode = row.querySelector("[name='costingCode']").value;
        const shippingMethod = row.querySelector("[name='shippingMethod']").value;
        const cogsCostingCode = row.querySelector("[name='cogsCostingCode']").value;
        const costingCode2 = row.querySelector("[name='costingCode2']").value;
        const cogsCostingCode2 = row.querySelector("[name='cogsCostingCode2']").value;
        const unitPrice = row.querySelector("[name='precio_venta']").value;

        // Crea un objeto con los datos de la línea
        const line = {
            "LineNum": index,
            "ItemCode": itemCode,
            "Quantity": parseFloat(quantity),
            "ShipDate": shipDate,
            "DiscountPercent": parseFloat(discount),
            "WarehouseCode": warehouseCode,
            "CostingCode": costingCode,
            "ShippingMethod": shippingMethod,
            "COGSCostingCode": cogsCostingCode,
            "CostingCode2": costingCode2,
            "COGSCostingCode2": cogsCostingCode2,
            "UnitPrice": parseFloat(unitPrice),
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
    
    // Aquí se hara la solicitud de envío al backend o API
    console.log(jsonData);
}
});
