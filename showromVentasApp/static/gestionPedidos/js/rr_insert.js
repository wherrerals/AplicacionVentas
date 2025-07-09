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
        const docTotal_base = document.getElementById("total_bruto").getAttribute("data-brutobase");
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

            const docEntryLinea = row.dataset.docentrylinea;

            const itemCode = row.querySelector("[name='sku_producto']").innerText;
            const line_num = row.querySelector("#indixe_producto").getAttribute("data-linenum");
            const quantity = row.querySelector("[name='cantidad']").value;
            const quantity2 = row.querySelector("[name='cantidad']").getAttribute("data-cantOriginal");
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
            const checkbox = row.querySelector("#switchCheckDefault");

            console.log("checkbox:", checkbox);
            const checkboxEstado = checkbox?.checked ? 1 : 0;
            console.log("checkboxEstado:", checkboxEstado);

            const line = {
                "LineNum": line_num,
                "ItemCode": itemCode,
                "DocEntry_line": docEntryLinea,
                "Quantity": parseFloat(quantity),
                "Quantity2": parseFloat(quantity2),
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
            "docTotal_base": docTotal_base,
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

        const jsonData = JSON.stringify(documentData);

        fetch('/ventas/crear_devolucion/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: jsonData
        })

            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error en la creación del documento');
                }
            })
            .then(data => {
                console.log('Operación exitosa:', data);
                if (data.success) {
                    const numeroCotizacion = document.getElementById('numero_orden');
                    const vendedor= document.getElementById("vendedor_data")

                    let existe_documento = data.id_solicitud
                    if (existe_documento && existe_documento !== '') {

                        const id_documento = document.getElementById("id_documento");
                        id_documento.textContent = `Borrador: ${data.id_solicitud}`; 
                        id_documento.setAttribute("data-id", data.id_solicitud);
                    }
                    
                    Swal.fire({
                        icon: 'success',
                        title: data.title,
                        text: data.message,
                        confirmButtonText: 'Aceptar'
                    })
                    
                    .then(() => {
                        const baseUrl = `/ventas/solicitudes_devolucion/`;

                        if (data.docEntry){
                            const url = `${baseUrl}?docentry=${data.docEntry}`;
                            window.location.href = url;
                        }
                        else {
                            const url = `${baseUrl}?id=${data.id_solicitud}`;
                            window.location.href = url;
                        }
                    })
                    ;

                    if (numeroCotizacion) {
                        numeroCotizacion.textContent = `${data.docNum}`;
                        numeroCotizacion.setAttribute('data-docEntry', `${data.docEntry}`);
                    }


                    const vendedorData = data.salesPersonCode;

                    if (vendedorData != undefined) {
                        vendedor.textContent = `${data.salesPersonName}`;
                        vendedor.setAttribute('data-codeVen', `${data.salesPersonCode}`);

                        const id_documento = document.getElementById("id_documento");

                        id_documento.textContent = "";
                        id_documento.setAttribute("data-id", "");

                    }

                    bloquearCampos();

                } else {
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
                hideLoadingOverlay();
            });
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});

