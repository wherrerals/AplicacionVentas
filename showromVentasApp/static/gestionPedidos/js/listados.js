document.addEventListener("DOMContentLoaded", function() {
    // Define la URL base correctamente, utilizando la raíz del sitio
    const baseURL = '/ventas/listado_Cotizaciones/';

    const fetchAndDisplayInitialData = (params) => {
        showLoader(); // Invocación de la función para mostrar el loader

        const url = `${window.location.origin}${baseURL}?top=${params.top}&skip=${params.skip}`;
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                displayQuotations(data.value || []);
                nextPageLink = data['odata.nextLink'] || null;
                hideLoader(); // Ocultamos el loader cuando finaliza la carga
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                hideLoader(); // En caso de error, ocultamos el loader también
            });
    };

    const applyFiltersAndFetchData = (filters) => {
        showLoader(); // Invocación de la función para mostrar el loader

        const filterData = {
            top: 20,
            skip: 0,
            ...filters
        };

        const listado_Cotizaciones_filtrado = '/ventas/listado_Cotizaciones_filtrado/';
        
        fetch(listado_Cotizaciones_filtrado, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filterData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            
            document.querySelector('#listadoCotizaciones').innerHTML = '';

            if (data && data.data && Array.isArray(data.data.value)) {
                displayQuotations(data.data.value);
                nextPageLink = data.data['odata.nextLink'] || null;
            } else {
                console.error('Error: Expected data.data.value to be an array');
                displayQuotations([]);
            }
            hideLoader(); // Ocultamos el loader cuando los datos ya están cargados
        })
        .catch(error => {
            console.error('Error applying filters:', error);
            hideLoader(); // En caso de error, ocultamos el loader
        });
    };

    const displayQuotations = (quotations) => {
        const tbody = document.querySelector('#listadoCotizaciones');
        tbody.innerHTML = '';

        if (!Array.isArray(quotations)) {
            console.error('Error: Expected quotations to be an array');
            return;
        }

        quotations.forEach(entry => {
            const quotation = entry.Quotations || {};
            const salesPerson = entry.SalesPersons || {};

            // Formatear los valores monetarios
            const vatSumFormatted = Number(quotation.DocTotalNeto).toLocaleString('es-ES', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 2
            });

            const docTotalFormatted = Number(quotation.DocTotal).toLocaleString('es-ES', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 2
            });

            // Obtener el estado del documento
            const getStatus = (quotation) => {
                if (quotation.Cancelled === 'Y') {
                    return 'Cancelado';
                } else if (quotation.DocumentStatus === 'O') {
                    return 'Abierto';
                } else if (quotation.DocumentStatus === 'C') {
                    return 'Cerrado';
                } else {
                    return 'Activo';
                }
            };

            const status = getStatus(quotation);
            console.log(quotation.DocEntry);
            let urlModel = `/ventas/obtener_detalles_cotizacion/${quotation.DocEntry}/`;

            // Crear una fila de la tabla
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><a href="${urlModel}" data-doc-entry="${quotation.DocEntry}" data-doc-num="${quotation.DocNum}" data-document-lines="${quotation.DocumentLines ? JSON.stringify(quotation.DocumentLines) : '[]'}">${quotation.DocNum}</a></td>
                <td><a href="/cliente.html">${quotation.CardName || 'Cliente Desconocido'}</a></td>
                <td>${salesPerson.SalesEmployeeName || 'N/A'}</td>
                <td>${quotation.DocDate}</td>
                <td>${status}</td>
                <td style="text-align: right;">$ ${vatSumFormatted}</td>
                <td style="text-align: right;">$ ${docTotalFormatted}</td>
            `;
            tbody.appendChild(tr);
        });
    };

    // Obtener datos de los filtros
    const getFilterData = () => {
        return {
            fecha_inicio: document.querySelector('[name="fecha_inicio"]').value,
            fecha_fin: document.querySelector('[name="fecha_fin"]').value,
            docNum: document.querySelector('[name="docNum"]').value,
            cardNAme: document.querySelector('[name="cardNAme"]').value,
            salesEmployeeName: document.querySelector('[name="salesEmployeeName"]').value,
            //DocumentStatus: document.querySelector('[name="DocumentStatus"]').value,
            docTotal: document.querySelector('[name="docTotal"]').value
        };
    };

    // Cargar datos iniciales
    fetchAndDisplayInitialData({ top: 20, skip: 0 });

    // Manejar el botón de filtro
    const filterButton = document.querySelector('#filterButton');
    if (filterButton) {
        filterButton.addEventListener('click', () => {
            const filters = getFilterData();
            applyFiltersAndFetchData(filters);
        });
    }

    // Manejar el botón de siguiente página
    const nextButton = document.querySelector('#nextButton');
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (nextPageLink) {
                fetchAndDisplayInitialData({ top: 20, skip: 0, nextLink: nextPageLink });
            }
        });
    }
});
