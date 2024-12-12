document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1; // Controlar la página actual
    const recordsPerPage = 20; // Cantidad de registros por página
    let totalPages = null; // No conocemos el total de páginas inicialmente
    let activeFilters = {}; // Variable para almacenar los filtros aplicados

    const getSkip = (page) => (page - 1) * recordsPerPage;

    const applyFiltersAndFetchData = (filters, page = 1) => {
        console.log("Applying filters:", filters, "Page:", page);
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
});

document.addEventListener("DOMContentLoaded", function () {
    const applyGeneralSearch = () => {
        const searchText = document.getElementById("buscar").value.trim();
        console.log("Search text entered:", searchText);

        // Verifica el tipo de filtro según el texto ingresado
        const filters = getFilterData(); // Carga los filtros existentes
        if (!isNaN(searchText)) {
            // Si es un número, buscar por SAP (Número de documento)
            console.log("Applying filter: SAP Number");
            filters.docNum = searchText;
        } else if (/^\d{4}-\d{2}-\d{2}$/.test(searchText)) {
            // Si es una fecha en formato YYYY-MM-DD
            console.log("Applying filter: Date");
            filters.fecha_doc = searchText;
        } else if (["abierto", "cerrado", "cancelado"].includes(searchText.toLowerCase())) {
            // Si es un estado (Abierto, Cerrado, Cancelado)
            console.log("Applying filter: Document Status");
            const estadoMap = {
                abierto: "O",
                cerrado: "C",
                cancelado: "Y"
            };
            filters.DocumentStatus = estadoMap[searchText.toLowerCase()];
        } else {
            // Si no es ninguno de los anteriores, buscar por nombre del cliente
            console.log("Applying filter: Customer Name");
            filters.cardName = searchText;
        }

        console.log("Filters to apply:", filters);
        applyFiltersAndFetchData(filters); // Aplica los filtros
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

        input.addEventListener('input', function () {
            if (this.value === '') {
                console.log(`Input cleared: ${id}, removing filter: ${filterKey}`);
                const filters = getFilterData(); // Obtiene los filtros actuales
                filters[filterKey] = ''; // Elimina el filtro correspondiente
                console.log("Filters after clearing input:", filters);
                applyFiltersAndFetchData(filters); // Aplica la búsqueda con los filtros actualizados
            }
        });
    });
};

// Llamar esta función después de cargar la página
document.addEventListener("DOMContentLoaded", function () {
    attachImmediateClearListeners(); // Activa los listeners para eliminar filtros inmediatamente
});
