document.addEventListener("DOMContentLoaded", function () {
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    const docEntry = getQueryParam('docentry');

    if (docEntry) {
        const vendedorDataElement = document.getElementById("vendedor_data");

        if (vendedorDataElement) {
            vendedorDataElement.innerText = "Cargando...";
        }

        fetch(`/ventas/detalles_cotizacion/?docentry=${docEntry}`)
            .then(response => {
                if (!response.ok) throw new Error('Error al obtener la información de la cotización');
                return response.json();
            })
            .then(data => {
                if (data.Cliente && data.Cliente.SalesPersons) {
                    console.log("Datos de la cotización:", data);

                    // Extracción de datos principales
                    const salesEmployeeName = data.Cliente.SalesPersons.SalesEmployeeName;
                    const sucursal = data.Cliente.SalesPersons.U_LED_SUCURS;
                    const numCotizacion = data.Cliente.Quotations.DocNum;
                    const docDate = data.Cliente.Quotations.DocDate;
                    const canceled = data.Cliente.Quotations.Canceled;
                    let cardCode = data.Cliente.Quotations.CardCode;

                    if (cardCode.endsWith("C")) {
                        cardCode = cardCode.slice(0, -1);
                        console.log("Código de cliente corregido:", cardCode);
                    }

                    const vendedorMatch = salesEmployeeName.match(/^[^-]+-\s*([^\s/]+.*?)\s*(\/|$)/);
                    const vendedorLimpio = vendedorMatch ? vendedorMatch[1].trim() : "Vendedor desconocido";
                    if (vendedorDataElement) {
                        vendedorDataElement.innerText = vendedorLimpio;
                    }

                    const showroomElement = document.getElementById("sucursal");
                    if (showroomElement) {
                        showroomElement.innerText = sucursal;
                    } else {
                        console.warn("No se encontró el elemento showroom en el DOM.");
                    }

                    const numeroCotizacionElement = document.getElementById("numero_cotizacion");
                    if (numeroCotizacionElement) {
                        numeroCotizacionElement.textContent = `${numCotizacion}`;
                    }
                    const dueDateElement = document.getElementById("docDueDate");
                    if (dueDateElement) {
                        dueDateElement.textContent = `${docDate}`;
                    }

                    const estadoElement = document.querySelector('p strong[data-estado="bost_Open"]');
                    if (estadoElement) {
                        estadoElement.textContent = (canceled === "N") ? "Abierta" : "Cancelada";
                    }

                    traerInformacionCliente(cardCode);

                    // Iteración sobre `DocumentLines` para añadir cada producto
                    const documentLines = data.DocumentLines;
                    documentLines.forEach((line) => {
                        const productoCodigo = line.ItemCode;
                        const nombre = line.ItemDescription;
                        const imagen = 'ruta_a_la_imagen.jpg';
                        const precioVenta = line.PriceAfterVAT;
                        const stockTotal = 0;
                        const precioLista = line.GrossPrice;
                        const precioDescuento = line.DiscountPercent;

                        // Debugging: Verificar datos del producto antes de agregarlo
                        console.log("Agregando producto con datos:", {
                            productoCodigo,
                            nombre,
                            imagen,
                            precioVenta,
                            stockTotal,
                            precioLista,
                            precioDescuento
                        });

                        agregarProducto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento);

                        // Selección de la última fila añadida
                        const productoRows = document.querySelectorAll('.product-row');
                        const newRow = productoRows[productoRows.length - 1];
                        if (!newRow) {
                            console.error("Error: No se encontró la nueva fila del producto en el DOM.");
                            return;
                        }


                    });
                }
            })
            .catch(error => {
                console.error('Error en la solicitud AJAX:', error);
                if (vendedorDataElement) {
                    vendedorDataElement.innerText = "Error al cargar datos";
                }
            });
    } else {
        console.log("No se ha proporcionado un DocEntry en la URL.");
    }
});
