document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    const recordsPerPage = 15;
    let totalPages = null;
    let activeFilters = {};
    let allSales = []; // Store all sales data for pagination
    const fechaDoc = document.getElementById('fecha_doc');
    const filtroEstado = document.getElementById('filtro_estado');
    const buscarBruto  = document.getElementById('buscar_bruto');

    function toggleFields(enabled) {
        if (fechaDoc) fechaDoc.disabled = !enabled;
        if (filtroEstado) filtroEstado.disabled = !enabled;
        if (buscarBruto) buscarBruto.disabled = !enabled;
    }

    const getSkip = (page) => (page - 1) * recordsPerPage;

    [fechaDoc, filtroEstado, buscarBruto].forEach(input => {
        if (input) {
            input.addEventListener('input', () => {
                const allEmpty = !fechaDoc.value.trim() && !filtroEstado.value.trim() && !buscarBruto.value.trim();
                if (allEmpty) {
                    toggleFields(false);
                }
            });
        }
    });    

    const buscarCliente = document.getElementById('buscar_cliente');
    if (buscarCliente) {
        buscarCliente.addEventListener('input', () => {
            const allEmpty =
                !buscarCliente.value.trim() &&
                !fechaDoc.value.trim() &&
                !filtroEstado.value.trim() &&
                !buscarBruto.value.trim();
    
            if (allEmpty) {
                toggleFields(false);
            }
        });
    }

    const vendedorSelect = document.querySelector('#filtro_vendedor');
    if (vendedorSelect) {
        const defaultVendedorValue = vendedorSelect.value;
        activeFilters['salesEmployeeName'] = defaultVendedorValue;
    }

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
            console.log('Data completa recibida:', data);
            
            // Reset the allSales array
            allSales = [];
            
            // Handle the nested data structure from your backend
            if (data && data.data) {
                // Handle nested data.data array
                if (Array.isArray(data.data)) {
                    allSales = data.data;
                } else if (data.data && typeof data.data === 'object') {
                    // Single object response
                    allSales = [data.data];
                }
            } else if (Array.isArray(data)) {
                // Direct array response
                allSales = data;
            } else if (data && typeof data === 'object' && data.DocNum) {
                // Single object response
                allSales = [data];
            }
            
            // If we still have no data, check for empty response
            if (allSales.length === 0) {
                document.querySelector('#listSales').innerHTML = '<tr><td colspan="9" class="text-center">No se encontraron resultados.</td></tr>';
                toggleFields(false); // Deshabilita si no hay resultados
                hideLoader();
                return;
            }


            // Calculate total pages based on all results
            totalPages = Math.ceil(allSales.length / recordsPerPage);
            
            // Display current page
            const startIndex = (page - 1) * recordsPerPage;
            const endIndex = Math.min(startIndex + recordsPerPage, allSales.length);
            const currentPageData = allSales.slice(startIndex, endIndex);
            
            displaySales(currentPageData);
            updatePagination(page);
            
            hideLoader();
        })
        .catch(error => {
            console.error('Error applying filters:', error);
            document.querySelector('#listSales').innerHTML = '<tr><td colspan="9" class="text-center">Error al cargar los datos. Por favor intente nuevamente.</td></tr>';
            hideLoader();
        });        
    };

    const displaySales = (sales) => {
        const tbody = document.querySelector('#listSales');
        if (!tbody) {
            console.error('Element #listSales not found');
            hideLoadingOverlay();
            return;
        }
        
        tbody.innerHTML = '';
        showLoadingOverlay();

        // Handle empty sales array
        if (!sales || !Array.isArray(sales) || sales.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No se encontraron resultados.</td></tr>';
            hideLoadingOverlay();
            return;
        }

        // Log the first sale for debugging
        if (sales.length > 0) {
            console.log('First sale item:', sales[0]);
        }

        sales.forEach(entry => {
            if (!entry) return; // Skip if entry is null or undefined
            
            // Debug: Log the entry to see its structure
            console.log('Processing entry:', entry);
            
            // Get the DocNum to check if this is a valid entry
            const docNum = entry.DocNum || (entry.data && entry.data.DocNum);
            
            if (!docNum) {
                console.log('Skipping invalid entry without DocNum:', entry);
                return; // Skip this entry if it doesn't have DocNum
            }
            
            function formatCurrency(value) {
                if (value === undefined || value === null) return '$ 0';
                
                const integerValue = Math.floor(value);
                let formattedValue = integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
                if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
                    formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
                }
                return `$ ${formattedValue}`;
            }

            // Use data property if it exists, otherwise use the entry directly
            const saleData = entry.data || entry;
            
            const vatSumFormatted = formatCurrency(saleData.NetTotal);
            const docTotalFormatted = formatCurrency(saleData.DocTotal);

            const getStatus = (data) => {
                if (!data) return 'Desconocido';
                if (data.Cancelled === 'Y') return 'Cancelado';
                else if (data.DocumentStatus === 'O') return 'Abierto';
                else if (data.DocumentStatus === 'C') return 'Cerrado';
                else return 'Activo';
            };
            const status = getStatus(saleData);

            let date = saleData.DocDate || '';
            let fechaFormateada = '';
            if (date) {         
                if (typeof date === 'string' && date.includes('-')) {
                    let partesFecha = date.split("-");
                    if (partesFecha.length === 3) {
                        fechaFormateada = `${partesFecha[2]}/${partesFecha[1]}/${partesFecha[0]}`;
                    } else {
                        fechaFormateada = date;
                    }
                } else {
                    fechaFormateada = date.toString();
                }
            }

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="fw-bold text-center" style="font-size: 12px;"><a href="#" class="docentry-link" data-docentry="${saleData.DocEntry}">${saleData.DocNum}</a></td>
                <td class="fw-bold text-start" style="font-size: 12px;">${saleData.documenttype || 'N/A'}</td>
                <td class="text-center" style="font-size: 12px;">${saleData.FolioNumber || 'N/A'}</td>
                <td class="fw-bold text-start" style="font-size: 12px;"><a href="#" class="cliente-link" data-cadcode="${saleData.CardCode}">${saleData.CardCode || 'N/A'} - ${saleData.CardName || 'Cliente Desconocido'}</a></td>
                <td class="text-start" style="font-size: 12px;">${saleData.SalesEmployeeName || 'N/A'}</td>
                <td class="text-center" style="font-size: 12px;">${fechaFormateada}</td>
                <td class="text-center" style="font-size: 12px;">${status}</td>
                <td class="text-end" style="font-size: 12px;">${vatSumFormatted}</td>
                <td class="text-end" style="font-size: 12px;">${docTotalFormatted}</td>
            `;
            tbody.appendChild(tr);
        });

        // If no valid entries were added, show empty message
        if (!tbody.hasChildNodes()) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No se encontraron resultados válidos.</td></tr>';
            hideLoadingOverlay();
            return;
        }

        document.querySelectorAll('.docentry-link').forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const docEntry = event.target.getAttribute('data-docentry');
                if (docEntry) {
                    showLoadingOverlay();
                    window.location.href = `/ventas/consulta-ventas/?docentry=${docEntry}`;
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
                        .then(response => {
                            if (!response.ok) throw new Error('Network response was not ok');
                            return response.json();
                        })
                        .then(data => {
                            console.log('Cliente:', data);
                            window.location.href = `/ventas/creacion_clientes/?rut=${cadCode}`;
                        })
                        .catch(error => {
                            hideLoadingOverlay();
                            console.error('Error al obtener cliente:', error);
                            alert("Error al obtener la información del cliente. Por favor intente nuevamente.");
                        });
                } else {
                    hideLoadingOverlay();
                    alert("No se pudo obtener el RUT del cliente.");
                }
            });
        });

        hideLoadingOverlay();
    };

    // Utility functions for loading overlay
    function showLoadingOverlay() {
        // Check if loading overlay exists
        let loadingOverlay = document.getElementById('loading-overlay');
        if (!loadingOverlay) {
            // Create loading overlay if it doesn't exist
            loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'loading-overlay';
            loadingOverlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); z-index: 9999; display: flex; justify-content: center; align-items: center;';
            
            const spinner = document.createElement('div');
            spinner.classList.add('spinner-border', 'text-light');
            spinner.setAttribute('role', 'status');
            
            const srOnly = document.createElement('span');
            srOnly.classList.add('visually-hidden');
            srOnly.textContent = 'Cargando...';
            
            spinner.appendChild(srOnly);
            loadingOverlay.appendChild(spinner);
            document.body.appendChild(loadingOverlay);
        } else {
            loadingOverlay.style.display = 'flex';
        }
    }

    function hideLoadingOverlay() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }

    function hideLoader() {
        hideLoadingOverlay();
    }


    const getFilterData = () => {
        return {
            fecha_doc: document.querySelector('[name="fecha_documento"]').value,
            docNum: document.querySelector('[name="docNum"]').value,
            carData: document.querySelector('[name="cardName"]').value,
            salesEmployeeName: document.querySelector('#filtro_vendedor').value,
            DocumentStatus: document.querySelector('[name="DocumentStatus"]').value,
            docTotal: document.querySelector('[name="docTotal"]').value,
            folio_number: document.getElementById('search_folio').value,
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

            // If we don't have pages or data is empty
            if (!totalPages || totalPages === 0) {
                // Just add current page
                const pageItem = document.createElement('li');
                pageItem.classList.add('page-item', 'active');
                pageItem.innerHTML = `<a class="page-link" href="#">1</a>`;
                paginationContainer.appendChild(pageItem);
            } else {
                // Add pagination with pages
                let startPage = Math.max(1, page - 1);
                let endPage = Math.min(totalPages, page + 1);
                
                // Always show at least 3 pages if available
                if (endPage - startPage < 2 && totalPages > endPage) {
                    endPage = Math.min(totalPages, endPage + 1);
                }
                if (endPage - startPage < 2 && startPage > 1) {
                    startPage = Math.max(1, startPage - 1);
                }
                
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
            }

            const nextButton = document.createElement('li');
            nextButton.classList.add('page-item');
            nextButton.innerHTML = `<a class="page-link" href="#"><span aria-hidden="true">»</span></a>`;
            if (totalPages && page < totalPages) {
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
    if (filterForm) {
        filterForm.addEventListener('keydown', function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                currentPage = 1; // Reset to first page on new search
                const filters = getFilterData();
                applyFiltersAndFetchData(filters);
                window.scrollTo(0, 0);
            }
        });
    }

    const selects = document.querySelectorAll('select');
    selects.forEach(select => {
        select.addEventListener('change', () => {
            currentPage = 1; // Reset to first page on filter change
            const filters = getFilterData();
            applyFiltersAndFetchData(filters);
        });
    });

    const attachClearEventListeners = () => {
        const filterInputs = document.querySelectorAll('#filterForm input');
        filterInputs.forEach(input => {
            input.addEventListener('input', () => {
                if (input.value === '') {
                    currentPage = 1; // Reset to first page on filter clear
                    const filters = getFilterData();
                    applyFiltersAndFetchData(filters);
                }
            });
        });
    };
    attachClearEventListeners();

    const inputBruto = document.getElementById('buscar_bruto');
    const inputNeto = document.getElementById('buscar_neto');
    if (inputBruto && inputNeto) {
        inputBruto.addEventListener('input', function() {
            const brutoValue = parseFloat(inputBruto.value) || 0;
            const netoValue = brutoValue * 0.84;
            inputNeto.value = netoValue.toFixed(2);
        });
    }

    // Check for URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const rutSN = urlParams.get("rutSN") || "";
    const nombreSN = urlParams.get("nombreSN") || "";

    if (rutSN || nombreSN) {
        const cardNameInput = document.querySelector('[name="cardName"]');
        if (cardNameInput) {
            if (rutSN) cardNameInput.value = rutSN;
            if (nombreSN) cardNameInput.value = nombreSN;
            const filters = getFilterData();
            applyFiltersAndFetchData(filters);
        }
    }
    toggleFields(false);
});