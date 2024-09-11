document.addEventListener("DOMContentLoaded", function() {
    // Define la URL base correctamente, utilizando la raíz del sitio
    const baseURL = '/ventas/listado_Cotizaciones/';
    
    const fetchAndDisplayInitialData = (params) => {
        // Asegúrate de que la URL base comience desde la raíz
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
            })
            .catch(error => console.error('Error fetching data:', error));
    };

    const applyFiltersAndFetchData = (filters) => {
        const filterData = {
            top: 20,
            skip: 0,
            ...filters
        };

        // Ajusta esta URL para que no se repita
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
            if (data && data.data && Array.isArray(data.data.value)) {
                displayQuotations(data.data.value);
                nextPageLink = data.data['odata.nextLink'] || null;
            } else {
                console.error('Error: Expected data.data.value to be an array');
                displayQuotations([]);
            }
        })
        .catch(error => console.error('Error applying filters:', error));
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
            console.log(quotation.DocEntry)
            let urlModel = `/ventas/generar_cotizacion/${quotation.DocEntry}/`;

            // Crear una fila de la tabla
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><a href="${urlModel}" data-doc-entry="${quotation.DocNum}" data-document-lines="${quotation.DocumentLines ? JSON.stringify(quotation.DocumentLines) : '[]'}">${quotation.DocEntry}</a></td>
                <td><a href="/cliente.html">${quotation.CardName || 'Cliente Desconocido'}</a></td>
                <td>${salesPerson.SalesEmployeeName || 'N/A'}</td>
                <td>${new Date(quotation.DocDate).toLocaleDateString()}</td>
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
            cardName: document.querySelector('[name="cardName"]').value // corregido 'cardNAme' a 'cardName'
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
