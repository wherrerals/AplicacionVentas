document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    const recordsPerPage = 15;
    let totalPages = null;
    let activeFilters = {};

    const getSkip = (page) => (page - 1) * recordsPerPage;

    const vendedorSelect = document.querySelector('#filtro_vendedor');
    const defaultVendedorValue = vendedorSelect.value;
    activeFilters['salesEmployeeName'] = defaultVendedorValue;

    const hasFilters = (filters) => {
        return Object.values(filters).some(value => value !== null && value !== undefined && value.toString().trim() !== '');
    };

    const applyFiltersAndFetchData = (filters, page = 1) => {
        if (!hasFilters(filters)) {
            hideLoader();
            console.log('No se aplicaron filtros. No se realiza la consulta.');
            document.querySelector('#listSales').innerHTML = '<tr><td colspan="9" class="text-center">Ingresa al menos un filtro para ver resultados.</td></tr>';
            return;
        }

        showLoadingOverlay();
        const skip = getSkip(page);
        const filterData = {
            top: recordsPerPage,
            skip,
            ...filters
        };

        activeFilters = filters;

        fetch('/ventas/obtener-ventas/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filterData),
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            document.querySelector('#listSales').innerHTML = '';
            if (data && data.data && Array.isArray(data.data.value)) {
                displayQuotations(data.data.value);
                if (data.totalRecords) {
                    totalPages = Math.ceil(data.totalRecords / recordsPerPage);
                }
                updatePagination(page);
                hideLoader();
            } else {
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
        const tbody = document.querySelector('#listSales');
        tbody.innerHTML = '';
        showLoadingOverlay();

        quotations.forEach(entry => {
            const quotation = entry.Invoices || {};
            const salesPerson = entry.SalesPersons || {};

            function formatCurrency(value) {
                const integerValue = Math.floor(value);
                let formattedValue = integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
                if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
                    formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
                }
                return `$ ${formattedValue}`;
            }

            const vatSumFormatted = formatCurrency(quotation.DocTotalNeto);
            const docTotalFormatted = formatCurrency(quotation.DocTotal);

            const getStatus = (quotation) => {
                if (quotation.Cancelled === 'Y') return 'Cancelado';
                else if (quotation.DocumentStatus === 'O') return 'Abierto';
                else if (quotation.DocumentStatus === 'C') return 'Cerrado';
                else return 'Activo';
            };
            const status = getStatus(quotation);

            let urlModel = `/ventas/detalles_cotizacion/?docentry=${quotation.DocEntry}`;
            let date = quotation.DocDate;
            let partesFecha = date.split("-");
            let fechaFormateada = `${partesFecha[2]}/${partesFecha[1]}/${partesFecha[0]}`;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="fw-bold text-center" style="font-size: 12px;"><a href="#" class="docentry-link" data-docentry="${quotation.DocEntry}">${quotation.DocNum}</a></td>
                <td class="text-start" style="font-size: 12px;">${salesPerson.SalesEmployeeName || 'N/A'}</td>
                <td class="text-start" style="font-size: 12px;">${salesPerson.SalesEmployeeName || 'N/A'}</td>
                <td class="fw-bold text-start" style="font-size: 12px;"><a href="#" class="cliente-link" data-cadcode="${quotation.CardCode}">${quotation.CardCode} - ${quotation.CardName || 'Cliente Desconocido'}</a></td>
                <td class="text-start" style="font-size: 12px;">${salesPerson.SalesEmployeeName || 'N/A'}</td>
                <td class="text-center" style="font-size: 12px;">${fechaFormateada}</td>
                <td class="text-center" style="font-size: 12px;">${status}</td>
                <td class="text-end" style="font-size: 12px;">${vatSumFormatted}</td>
                <td class="text-end" style="font-size: 12px;">${docTotalFormatted}</td>
            `;
            tbody.appendChild(tr);
        });

        document.querySelectorAll('.docentry-link').forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const docEntry = event.target.getAttribute('data-docentry');
                if (docEntry) {
                    showLoadingOverlay();
                    window.location.href = `/ventas/generar_cotizacion/?docentry=${docEntry}`;
                } else {
                    hideLoadingOverlay();
                    alert("No se pudo obtener el DocEntry de la cotización.");
                }
            });
        });

        document.querySelectorAll('.cliente-link').forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                let cadCode = event.target.getAttribute('data-cadcode');
                if (cadCode && (cadCode.endsWith("C") || cadCode.endsWith("c"))) {
                    cadCode = cadCode.slice(0, -1);
                }
                if (cadCode) {
                    showLoadingOverlay();
                    fetch(`/ventas/informacion_cliente/?rut=${cadCode}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log('Cliente:', data);
                            window.location.href = `/ventas/creacion_clientes/?rut=${cadCode}`;
                        })
                        .catch(error => {
                            hideLoadingOverlay();
                            console.error('Error al obtener cliente:', error);
                        });
                } else {
                    hideLoadingOverlay();
                    alert("No se pudo obtener el RUT del cliente.");
                }
            });
        });

        hideLoadingOverlay();
    };

    const getFilterData = () => {
        return {
            docNum: document.querySelector('[name="docNum"]').value,
            carData: document.querySelector('[name="cardName"]').value,
        };
    };

    const updatePagination = (page) => {
        const paginationContainers = document.querySelectorAll('.pagination');
        paginationContainers.forEach(paginationContainer => {
            paginationContainer.innerHTML = '';
            const prevButton = document.createElement('li');
            prevButton.classList.add('page-item');
            prevButton.innerHTML = `<a class="page-link" href="#"><span aria-hidden="true">«</span></a>`;
            if (page > 1) {
                prevButton.querySelector('a').addEventListener('click', (e) => {
                    e.preventDefault();
                    currentPage -= 1;
                    fetchAndDisplayData(currentPage);
                });
            } else {
                prevButton.classList.add('disabled');
            }
            paginationContainer.appendChild(prevButton);

            let startPage = Math.max(1, page - 1);
            let endPage = Math.min(totalPages || page + 1, page + 1);
            for (let i = startPage; i <= endPage; i++) {
                const pageItem = document.createElement('li');
                pageItem.classList.add('page-item');
                if (i === page) pageItem.classList.add('active');
                pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                pageItem.querySelector('a').addEventListener('click', (e) => {
                    e.preventDefault();
                    currentPage = i;
                    fetchAndDisplayData(currentPage);
                });
                paginationContainer.appendChild(pageItem);
            }

            const nextButton = document.createElement('li');
            nextButton.classList.add('page-item');
            nextButton.innerHTML = `<a class="page-link" href="#"><span aria-hidden="true">»</span></a>`;
            if (totalPages === null || page < totalPages) {
                nextButton.querySelector('a').addEventListener('click', (e) => {
                    e.preventDefault();
                    currentPage += 1;
                    fetchAndDisplayData(currentPage);
                });
            } else {
                nextButton.classList.add('disabled');
            }
            paginationContainer.appendChild(nextButton);
        });
    };

    const fetchAndDisplayData = (page = 1) => {
        const filters = getFilterData();
        applyFiltersAndFetchData(filters, page);
        window.scrollTo(0, 0);
    };

    const filterForm = document.querySelector('#filterForm');
    filterForm.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            const filters = getFilterData();
            applyFiltersAndFetchData(filters);
            window.scrollTo(0, 0);
        }
    });

    const selects = document.querySelectorAll('select');
    selects.forEach(select => {
        select.addEventListener('change', () => {
            const filters = getFilterData();
            applyFiltersAndFetchData(filters);
        });
    });

    const attachClearEventListeners = () => {
        const filterInputs = document.querySelectorAll('#filterForm input');
        filterInputs.forEach(input => {
            input.addEventListener('input', () => {
                if (input.value === '') {
                    const filters = getFilterData();
                    applyFiltersAndFetchData(filters);
                }
            });
        });
    };
    attachClearEventListeners();

    const inputBruto = document.getElementById('buscar_bruto');
    const inputNeto = document.getElementById('buscar_neto');
    inputBruto.addEventListener('input', function() {
        const brutoValue = parseFloat(inputBruto.value) || 0;
        const netoValue = brutoValue * 0.84;
        inputNeto.value = netoValue;
    });

    const urlParams = new URLSearchParams(window.location.search);
    const rutSN = urlParams.get("rutSN") || "";
    const nombreSN = urlParams.get("nombreSN") || "";

    if (rutSN || nombreSN) {
        if (rutSN) document.querySelector('[name="cardName"]').value = rutSN;
        if (nombreSN) document.querySelector('[name="cardName"]').value = nombreSN;
        const filters = getFilterData();
        applyFiltersAndFetchData(filters);
    }
});
