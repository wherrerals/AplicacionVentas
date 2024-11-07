document.addEventListener("DOMContentLoaded", function () {
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    const docEntry = getQueryParam('docentry');

    if (docEntry) {
        const vendedorDataElement = document.getElementById("vendedor_data");

        // Mostrar "Cargando..." antes de la solicitud
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
                    const salesEmployeeName = data.Cliente.SalesPersons.SalesEmployeeName;
                    const sucursal = data.Cliente.SalesPersons.U_LED_SUCURS;
                    const numCotizacion = data.Cliente.Quotations.DocNum;
                    const docDate = data.Cliente.Quotations.DocDate;
                    const canceled = data.Cliente.Quotations.Canceled;
                    const cardCode = data.Cliente.Quotations.CardCode;

                    console.log("Valor original de SalesEmployeeName:", salesEmployeeName);
                    console.log("Valor original de U_LED_SUCURS (Sucursal):", sucursal);
                    console.log("Número de cotización:", numCotizacion);
                    console.log("Fecha de la cotización:", docDate);

                    // Extraer el nombre limpio del vendedor
                    // Extraer el nombre limpio del vendedor eliminando todo después del primer guion "-"
                    const vendedorMatch = salesEmployeeName.match(/^[^-]+-\s*(.*?)\s*$/);
                    const vendedorLimpio = vendedorMatch ? vendedorMatch[1] : "Vendedor desconocido";

                    console.log("Nombre del vendedor limpio:", vendedorLimpio);


                    // Mostrar el nombre del vendedor después de cargar
                    if (vendedorDataElement) {
                        vendedorDataElement.innerText = "Cargando...";
                        setTimeout(() => {
                            vendedorDataElement.innerText = vendedorLimpio;
                        }, 0);
                    }

                    // Supongamos que 'sucursal' tiene el valor que deseas mostrar
                    const showroomElement =  document.getElementById("sucursal")

                    if (showroomElement) {
                        console.log("Contenido previo de showroom:", showroomElement.innerText);
                        showroomElement.innerText = sucursal;  // Actualiza el texto con el valor de sucursal
                        console.log("Contenido actualizado de showroom:", showroomElement.innerText);
                    } else {
                        console.warn("No se encontró el elemento showroom en el DOM.");
                    }



                    if (numCotizacion) {
                        const numeroCotizacionElement = document.getElementById("numero_cotizacion");
                        if (numeroCotizacionElement) {
                            numeroCotizacionElement.textContent = `${numCotizacion}`;
                        }
                    }

                    if (docDate) {
                        const dueDateElement = document.getElementById("docDueDate");
                        if (dueDateElement) {
                            dueDateElement.textContent = `${docDate}`;
                        }
                    }

                    const estadoElement = document.querySelector('p strong[data-estado="bost_Open"]');
                    if (estadoElement) {

                        estadoElement.textContent = (canceled === "N") ? "Abierta" : "Cancelada";
                    }


                }
            })
            .catch(error => {
                console.error('Error en la solicitud AJAX:', error);

                // Si hay un error, mostrar un mensaje alternativo
                if (vendedorDataElement) {
                    vendedorDataElement.innerText = "Error al cargar datos";
                }
            });
    } else {
        console.log("No se ha proporcionado un DocEntry en la URL.");
    }
});
