document.addEventListener("DOMContentLoaded", function() {
    // Define la URL base correctamente, utilizando la raíz del sitio
    let baseURL = '/ventas/listado_Cotizaciones/';
    
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
            .catch(error => console.error('Error:', error));
    };

    const applyFiltersAndFetchData = (filters) => {
        const filterData = {
            top: 20,
            skip: 0,
            ...filters
        };

        // Ajusta esta URL para que no se repita
        let listado_Cotizaciones_filtrado = '/ventas/listado_Cotizaciones_filtrado/';
        
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
        .catch(error => console.error('Error:', error));
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

            const vatSumFormatted = quotation.DocTotalNeto.toLocaleString('es-ES', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 2
            });

            const docTotalFormatted = quotation.DocTotal.toLocaleString('es-ES', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 2
            });

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

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><a href="/ventas/generar_cotizacion?docNum=${quotation.DocEntry}" data-doc-entry="${quotation.DocNum}" data-document-lines="[]">${quotation.DocEntry}</a></td>
                <td><a href="/cliente.html">${quotation.CardName}</a></td>
                <td>${salesPerson.SalesEmployeeName || ''}</td>
                <td>${quotation.DocDate}</td>
                <td>${status}</td>
                <td style="text-align: right;">$ ${vatSumFormatted}</td>
                <td style="text-align: right;">$ ${docTotalFormatted}</td>
            `;
            tbody.appendChild(tr);
        });
    };

    const getFilterData = () => {
        return {
            fecha_inicio: document.querySelector('[name="fecha_inicio"]').value,
            fecha_fin: document.querySelector('[name="fecha_fin"]').value,
            docNum: document.querySelector('[name="docNum"]').value,
            cardNAme: document.querySelector('[name="cardNAme"]').value
        };
    };

    fetchAndDisplayInitialData({ top: 20, skip: 0 });

    const filterButton = document.querySelector('#filterButton');
    if (filterButton) {
        filterButton.addEventListener('click', () => {
            const filters = getFilterData();
            applyFiltersAndFetchData(filters);
        });
    }

    const nextButton = document.querySelector('#nextButton');
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (nextPageLink) {
                fetchAndDisplayInitialData({ top: 20, skip: 0, nextLink: nextPageLink });
            }
        });
    }
});
