document.addEventListener("DOMContentLoaded", function () {
    const baseURL = '/ventas/listado_Cotizaciones/';
    let currentPage = 1; // Controlar la página actual
    const recordsPerPage = 20; // Cantidad de registros por página
    let totalPages = null; // No conocemos el total de páginas inicialmente

    const getSkip = (page) => (page - 1) * recordsPerPage;

    const fetchAndDisplayInitialData = (params) => {
        showLoader();
        const url = `${window.location.origin}${baseURL}?top=${params.top}&skip=${params.skip}`;
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                console.log(data);
                displayQuotations(data.value || []);

                // Si el backend devuelve el número total de registros
                if (data.totalRecords) {
                    totalPages = Math.ceil(data.totalRecords / recordsPerPage);
                }

                hideLoader();
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                hideLoader();
            });
    };

    const applyFiltersAndFetchData = (filters) => {
        showLoader();
        const filterData = {
            top: 20,
            skip: 0,
            ...filters
        };

        fetch('/ventas/listado_Cotizaciones_filtrado/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filterData),
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            document.querySelector('#listadoCotizaciones').innerHTML = '';
            if (data && data.data && Array.isArray(data.data.value)) {
                displayQuotations(data.data.value);

                
                if (data.totalRecords) {
                    totalPages = Math.ceil(data.totalRecords / recordsPerPage);
                }

                hideLoader();
            } else {
                console.error('Error: Expected data.data.value to be an array');
                displayQuotations([]);
                hideLoader();
            }
        })
        .catch(error => {
            console.error('Error applying filters:', error);
            hideLoader();
        });
    };

    const displayQuotations = (quotations) => {
        const tbody = document.querySelector('#listadoCotizaciones');
        tbody.innerHTML = '';

        quotations.forEach(entry => {
            const quotation = entry.Quotations || {};
            const salesPerson = entry.SalesPersons || {};
            const vatSumFormatted = Number(quotation.DocTotalNeto).toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
            const docTotalFormatted = Number(quotation.DocTotal).toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
            const getStatus = (quotation) => {
                if (quotation.Cancelled === 'Y') return 'Cancelado';
                else if (quotation.DocumentStatus === 'O') return 'Abierto';
                else if (quotation.DocumentStatus === 'C') return 'Cerrado';
                else return 'Activo';
            };
            const status = getStatus(quotation);
            let urlModel = `/ventas/obtener_detalles_cotizacion/${quotation.DocEntry}/`;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><a href="${urlModel}">${quotation.DocNum}</a></td>
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

    const getFilterData = () => {
        return {
            fecha_inicio: document.querySelector('[name="fecha_inicio"]').value,
            fecha_fin: document.querySelector('[name="fecha_fin"]').value,
            fecha_doc: document.querySelector('[name="fecha_documento"]').value,
            docNum: document.querySelector('[name="docNum"]').value,
            cardNAme: document.querySelector('[name="cardNAme"]').value,
            salesEmployeeName: document.querySelector('[name="salesEmployeeName"]').value,
            DocumentStatus: document.querySelector('[name="DocumentStatus"]').value,
            docTotal: document.querySelector('[name="docTotal"]').value
        };
    };

    // Función para obtener los datos de la página actual
    const fetchAndDisplayData = (page = 1) => {
        const skip = getSkip(page);
        fetchAndDisplayInitialData({ top: recordsPerPage, skip });
        updatePagination(page);
        window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
    };

    const updatePagination = (page) => {
        const paginationContainer = document.querySelector('.pagination');
        paginationContainer.innerHTML = ''; // Limpiar la paginación actual

        // Botón "Anterior"
        const prevButton = document.createElement('li');
        prevButton.classList.add('page-item');
        prevButton.innerHTML = `
            <a class="page-link" aria-label="Previous" href="#" id="prevButton">
                <span aria-hidden="true">«</span>
            </a>
        `;
        if (page > 1) {
            prevButton.querySelector('a').addEventListener('click', (event) => {
                event.preventDefault();
                currentPage -= 1;
                fetchAndDisplayData(currentPage);
            });
        } else {
            prevButton.classList.add('disabled');
        }
        paginationContainer.appendChild(prevButton);

        // Mostrar al menos 3 números de página alrededor de la página actual
        let startPage = Math.max(1, page - 1);
        let endPage = Math.min(totalPages || page + 1, page + 1); // Mostrar máximo 3 números

        for (let i = startPage; i <= endPage; i++) {
            const pageItem = document.createElement('li');
            pageItem.classList.add('page-item');
            if (i === page) {
                pageItem.classList.add('active');
            }
            pageItem.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
            paginationContainer.appendChild(pageItem);
        }

        // Botón "Siguiente"
        const nextButton = document.createElement('li');
        nextButton.classList.add('page-item');
        nextButton.innerHTML = `
            <a class="page-link" aria-label="Next" href="#" id="nextButton">
                <span aria-hidden="true">»</span>
            </a>
        `;
        if (totalPages === null || page < totalPages) { // Si no sabemos el total de páginas o no es la última
            nextButton.querySelector('a').addEventListener('click', (event) => {
                event.preventDefault();
                currentPage += 1;
                fetchAndDisplayData(currentPage);
            });
        } else {
            nextButton.classList.add('disabled');
        }
        paginationContainer.appendChild(nextButton);
    };

    // Llamar a la función para cargar la primera página al inicio
    fetchAndDisplayData(currentPage);

    // Escuchar el evento 'keydown' para capturar "Enter" en cualquier campo de filtro
    const filterForm = document.querySelector('#filterForm');
    filterForm.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Evita que se envíe el formulario
            const filters = getFilterData();
            applyFiltersAndFetchData(filters); // Aplica los filtros cuando se presiona Enter
            window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
        }
    });
});
