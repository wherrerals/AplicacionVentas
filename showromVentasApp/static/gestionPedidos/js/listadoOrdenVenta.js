document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1; // Controlar la página actual
    const recordsPerPage = 20; // Cantidad de registros por página
    let totalPages = null; // No conocemos el total de páginas inicialmente
    let activeFilters = {}; // Variable para almacenar los filtros aplicados

    const getSkip = (page) => (page - 1) * recordsPerPage;

    const applyFiltersAndFetchData = (filters, page = 1) => {
        //console.log("Applying filters:", filters, "Page:", page);
        showLoader();
        const skip = getSkip(page); // Calcular el número de registros a omitir
        const filterData = {
            top: recordsPerPage,
            skip,
            ...filters
        };

        // Guardar los filtros activos para que funcionen con la paginación
        activeFilters = filters;

        console.log("Fetching data with payload:", filterData);

        fetch('/ventas/listado_odv/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filterData),
        })
        .then(response => {
            console.log("Fetch response status:", response.status);
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log("Data received from backend:", data);

            document.querySelector('tbody').innerHTML = '';
            if (data && data.data && Array.isArray(data.data.value)) {
                displayOrders(data.data.value);

                // Si el backend devuelve el número total de registros
                if (data.totalRecords) {
                    totalPages = Math.ceil(data.totalRecords / recordsPerPage);
                }
                console.log("Total pages calculated:", totalPages);

                updatePagination(page); // Actualizar la paginación
                hideLoader();
            } else {
                console.error('Error: Expected data.data.value to be an array');
                displayOrders([]);
                hideLoader();
            }
        })
        .catch(error => {
            console.error('Error applying filters:', error);
            hideLoader();
        });
    };

    const applyGeneralSearch = () => {
        const searchText = document.getElementById("buscar").value.trim();
        const filters = getFilterData(); // Obtén los filtros actuales

        // Identificar el campo donde escribir el valor ingresado
        if (!isNaN(searchText)) {
            filters.docNum = searchText;
            document.getElementById("buscar_num_sap").value = searchText;
        } else if (searchText.toLowerCase() === "míos" || searchText.toLowerCase() === "todos") {
            const vendedorMap = {
                "míos": "12",
                "todos": ""
            };
            filters.salesEmployeeName = vendedorMap[searchText.toLowerCase()];
            document.getElementById("filtro_vendedor").value = vendedorMap[searchText.toLowerCase()];
        } else if (/^\d{4}-\d{2}-\d{2}$/.test(searchText)) {
            filters.fecha_doc = searchText;
        } else if (["abierto", "cerrado", "cancelado", "Abierto", "Cerrado", "Cancelado"].includes(searchText)) {
            const estadoMap = {
                "abierto": "O",
                "cerrado": "C",
                "cancelado": "Y",
                "Abierto": "O",
                "Cerrado": "C",
                "Cancelado": "Y"
            };
            filters.DocumentStatus = estadoMap[searchText.toLowerCase()];
            document.getElementById("filtro_estado").value = estadoMap[searchText.toLowerCase()];
        } else if (/^\d+(\.\d{1,2})?$/.test(searchText)) {
            filters.docTotal = searchText;
            document.getElementById("buscar_bruto").value = searchText;
        } else {
            filters.cardName = searchText;
            document.getElementById("buscar_cliente").value = searchText;
        }

        document.getElementById("buscar").value = "";
        
        // Actualizar los filtros en el backend
        applyFiltersAndFetchData(filters);
    };



    // Evento para capturar "Enter" en el campo de búsqueda
    document.getElementById("buscar").addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            applyGeneralSearch();
        }
    });

    // Evento para aplicar el filtro al hacer clic en la lupa
    document.getElementById("lupa-busqueda").addEventListener("click", function () {
        applyGeneralSearch();
    });
    

    const displayOrders = (orders) => {
        console.log("Displaying orders:", orders);
        const tbody = document.querySelector('tbody');
        tbody.innerHTML = '';
    
        orders.forEach(entry => {
            const order = entry.Orders || {};
            const salesPerson = entry.SalesPersons || {};
            
            function formatCurrency(value) {
                const integerValue = Math.floor(value);
                let formattedValue = integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
    
                if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
                    formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
                }
                
                return `$ ${formattedValue}`;
            }
    
            const vatSumFormatted = formatCurrency(order.DocTotalNeto);
            const docTotalFormatted = formatCurrency(order.DocTotal);
    
            const getStatus = (order) => {
                if (order.Cancelled === 'Y') return 'Cancelado';
                else if (order.DocumentStatus === 'O') return 'Abierto';
                else if (order.DocumentStatus === 'C') return 'Cerrado';
                else return 'Activo';
            };
            const status = getStatus(order);
    
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><a href="#" class="order-link" data-docentry="${order.DocEntry}">${order.DocNum}</a></td>
                <td><a href="#" class="cliente-link" data-cadcode="${order.CardCode}">${order.CardCode} - ${order.CardName || 'Cliente Desconocido'}</a></td>
                <td>${salesPerson.SalesEmployeeName || 'N/A'}</td>
                <td>${order.DocDate}</td>
                <td>${status}</td>
                <td style="text-align: right;">${vatSumFormatted}</td>
                <td style="text-align: right;">${docTotalFormatted}</td>
            `;
            tbody.appendChild(tr);
        });
    
        // Agrega eventos a los enlaces de orden
        document.querySelectorAll('.order-link').forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const docEntry = event.target.getAttribute('data-docentry');
                
                if (docEntry) {
                    showLoadingOverlay();
                    window.location.href = `/ordenesVentas/?docentry=${docEntry}`;
                } else {
                    hideLoadingOverlay();
                    alert("No se pudo obtener el DocEntry de la orden.");
                }
            });
        });
    
        // Agrega eventos a los enlaces de clientes
        document.querySelectorAll('.cliente-link').forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                let cadCode = event.target.getAttribute('data-cadcode');
    
                if (cadCode && cadCode.endsWith("C")) {
                    cadCode = cadCode.slice(0, -1);
                }
    
                if (cadCode) {
                    showLoadingOverlay();
                    fetch(`/ventas/informacion_cliente/?rut=${cadCode}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Error al obtener la información del cliente: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Información del cliente:', data);
                        window.location.href = `/ventas/creacion_clientes/?rut=${cadCode}`;
                    })
                    .catch(error => {
                        hideLoadingOverlay();
                        console.error('Error en la solicitud AJAX:', error);
                        alert('Hubo un problema al obtener la información del cliente. Por favor, intenta de nuevo.');
                    });
                
                } else {
                    hideLoadingOverlay();
                    alert("No se pudo obtener el RUT del cliente.");
                }
            });
        });
    };
    

    const formatCurrency = (value) => {
        const integerValue = Math.floor(value);
        return `$ ${integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`;
    };

    const getFilterData = () => {
        const filters = {
            fecha_inicio: document.getElementById('fecha_inicio').value,
            fecha_fin: document.getElementById('fecha_fin').value,
            fecha_doc: document.getElementById('fecha_doc').value,
            docNum: document.getElementById('buscar_num_sap').value,
            cardName: document.getElementById('buscar_cliente').value,
            salesEmployeeName: document.getElementById('filtro_vendedor').value,
            DocumentStatus: document.getElementById('filtro_estado').value,
            docTotal: document.getElementById('buscar_bruto').value
        };
        console.log("Collected filter data:", filters);
        return filters;
    };

    const updatePagination = (page) => {
        console.log("Updating pagination for page:", page, "Total pages:", totalPages);
        const paginationContainers = document.querySelectorAll('.pagination');

        paginationContainers.forEach(paginationContainer => {
            paginationContainer.innerHTML = '';

            // Botón "Anterior"
            const prevButton = document.createElement('li');
            prevButton.classList.add('page-item');
            prevButton.innerHTML = `
                <a class="page-link" aria-label="Previous" href="#">
                    <span aria-hidden="true">«</span>
                </a>`;
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

            // Números de página
            let startPage = Math.max(1, page - 1);
            let endPage = Math.min(totalPages || page + 1, page + 1);

            for (let i = startPage; i <= endPage; i++) {
                const pageItem = document.createElement('li');
                pageItem.classList.add('page-item');
                if (i === page) {
                    pageItem.classList.add('active');
                }
                pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                pageItem.querySelector('a').addEventListener('click', (event) => {
                    event.preventDefault();
                    currentPage = i;
                    fetchAndDisplayData(currentPage);
                });
                paginationContainer.appendChild(pageItem);
            }

            // Botón "Siguiente"
            const nextButton = document.createElement('li');
            nextButton.classList.add('page-item');
            nextButton.innerHTML = `
                <a class="page-link" aria-label="Next" href="#">
                    <span aria-hidden="true">»</span>
                </a>`;
            if (totalPages === null || page < totalPages) {
                nextButton.querySelector('a').addEventListener('click', (event) => {
                    event.preventDefault();
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
        console.log("Fetching and displaying data for page:", page);
        applyFiltersAndFetchData(activeFilters, page);
        window.scrollTo(0, 0);
    };

    // Cargar la primera página con los filtros activos
    console.log("Initializing data fetch...");
    fetchAndDisplayData(currentPage);

    document.getElementById('OVsForm').addEventListener('keydown', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            const filters = getFilterData();
            console.log("Filters applied via Enter key:", filters);
            applyFiltersAndFetchData(filters);
        }
    });

    const attachImmediateClearListeners = () => {
        // Lista de inputs a observar
        const inputsToWatch = [
            { id: 'buscar_num_sap', filterKey: 'docNum' },
            { id: 'buscar_cliente', filterKey: 'cardName' },
            { id: 'buscar_bruto', filterKey: 'docTotal' }
        ];
    
        // Agrega eventos a cada input
        inputsToWatch.forEach(({ id, filterKey }) => {
            const input = document.getElementById(id);
    
            if (input) { // Validar que el input exista
                input.addEventListener('input', function () {
                    const filters = getFilterData(); // Obtiene los filtros actuales
                    const inputValue = this.value.trim();
    
                    if (inputValue === '') {
                        // Si el campo está vacío, elimina el filtro y ejecuta la búsqueda
                        console.log(`Input cleared: ${id}, removing filter: ${filterKey}`);
                        filters[filterKey] = ''; // Elimina el filtro correspondiente
                        applyFiltersAndFetchData(filters); // Update data when the field is cleared
                    } else {
                        // Si tiene texto, actualiza el filtro con el valor del input
                        console.log(`Input updated: ${id}, applying filter: ${filterKey}`);
                        filters[filterKey] = inputValue;
                        applyFiltersAndFetchData(filters); // Update data when the field is cleared

                    }
    
                    // Aplica la búsqueda con los filtros actualizados
                    console.log("Filters after change:", filters);
                    applyFiltersAndFetchData(filters);
                });
            } else {
                console.warn(`Input with ID "${id}" not found. Ensure the HTML element exists.`);
            }
        });
    };

    
    // Evento para aplicar búsqueda automáticamente al cambiar el estado
    const applyFiltersOnChange = (filterIds) => {
        filterIds.forEach((filterId) => {
            const filterElement = document.getElementById(filterId);
            if (filterElement) {
                filterElement.addEventListener("change", function () {
                    const filters = getFilterData(); // Obtiene los filtros actuales
                    console.log(`${filterId} cambiado, aplicando filtros:`, filters);
                    applyFiltersAndFetchData(filters); // Ejecuta la búsqueda automáticamente
                });
            } else {
                console.warn(`No se encontró el elemento con id=${filterId}.`);
            }
        });
    };
    
    // Llama a la función con los IDs de los filtros que deseas observar
    applyFiltersOnChange(["filtro_estado", "filtro_vendedor"]);
    
    
    


    attachImmediateClearListeners(); // Activa los listeners para eliminar filtros inmediatamente
});

document.addEventListener("DOMContentLoaded", function () {
    
});


document.addEventListener("DOMContentLoaded", function () {
    const buscarBrutoInput = document.getElementById("buscar_bruto");
    const buscarNetoInput = document.getElementById("buscar_neto");

    if (buscarBrutoInput && buscarNetoInput) {
        buscarBrutoInput.addEventListener("input", function () {
            const brutoValue = parseFloat(this.value) || 0; // Leer el valor de buscar_bruto
            const netoValue = brutoValue * 0.84; // Calcular el valor neto
            buscarNetoInput.value = `$${netoValue.toFixed(2)}`;
            
        });
    } else {
        console.warn("No se encontraron los elementos con id buscar_bruto o buscar_neto.");
    }
});

