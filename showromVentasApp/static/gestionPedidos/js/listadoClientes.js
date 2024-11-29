document.addEventListener("DOMContentLoaded", function () {
    const baseURL = '/ventas/listado_socios_negocio/';
    let currentPage = 1; // Página actual
    const recordsPerPage = 20; // Cantidad de registros por página
    let hasMoreData = true; // Determina si hay más datos para cargar

    const getSkip = (page) => (page - 1) * recordsPerPage;

    const fetchAndDisplayData = (page = 1) => {
        if (!hasMoreData && page > currentPage) return;
    
        // Desplazar hacia la parte superior antes de comenzar la carga
        window.scrollTo({
            top: 0,
            behavior: 'smooth',
        });
    
        // Mostrar el loader después de iniciar el desplazamiento
        setTimeout(() => {
            showLoader();
    
            const skip = getSkip(page);
            const url = `${baseURL}?top=${recordsPerPage}&skip=${skip}`;
    
            fetch(url)
                .then(response => {
                    if (!response.ok) throw new Error('Error al obtener los datos del servidor');
                    return response.json();
                })
                .then(data => {
                    if (data.value && Array.isArray(data.value)) {
                        displayClients(data.value);
    
                        // Determinar si hay más datos basándonos en el tamaño de los datos devueltos
                        hasMoreData = data.value.length === recordsPerPage;
                        currentPage = page;
    
                        updatePagination(page);
                    } else {
                        console.error('Error: Formato inesperado de los datos');
                    }
                })
                .catch(error => {
                    console.error('Error al obtener los datos:', error);
                })
                .finally(() => {
                    hideLoader();
                });
        }, 300); // Tiempo para garantizar que el desplazamiento se vea antes del loader
    };
    

    const displayClients = (clients) => {
        const tbody = document.querySelector('#listadoClientes');
        tbody.innerHTML = ''; // Limpiar datos anteriores

        clients.forEach(client => {
            const cardCodeClean = client.CardCode ? client.CardCode.replace(/C$/, '') : 'N/A';
            const groupType = client.GroupCode === 100 ? 'Persona' : client.GroupCode === 105 ? 'Empresa' : 'N/A';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><a href="/ventas/creacion_clientes/?rut=${cardCodeClean}" class="client-link">${cardCodeClean}</a></td>
                <td>${client.CardName || 'Desconocido'}</td>
                <td>${groupType}</td>
                <td>${client.Phone1 || 'No disponible'}</td>
                <td>${client.EmailAddress || 'no disponible'}</td>
            `;
            tbody.appendChild(tr);
        });
    };

    const updatePagination = (page) => {
        const paginationContainers = [
            document.querySelector('#paginationTop'),
            document.querySelector('#paginationBottom'),
        ];
    
        paginationContainers.forEach((paginationContainer) => {
            paginationContainer.innerHTML = ''; // Limpiar la paginación actual
    
            const createPageItem = (pageNum, isActive = false) => {
                const pageItem = document.createElement('li');
                pageItem.classList.add('page-item');
                if (isActive) {
                    pageItem.classList.add('active');
                }
                pageItem.innerHTML = `<a class="page-link" href="#">${pageNum}</a>`;
                pageItem.querySelector('a').addEventListener('click', (event) => {
                    event.preventDefault();
                    fetchAndDisplayData(pageNum);
                    // Desplazar hacia la parte superior de la tabla al cambiar de página
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
                return pageItem;
            };
    
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
                    fetchAndDisplayData(page - 1);
                });
            } else {
                prevButton.classList.add('disabled');
            }
            paginationContainer.appendChild(prevButton);
    
            // Números de página (mostrar 3 números centrados en la página actual)
            const startPage = Math.max(1, page - 1);
            const endPage = page + 1;
    
            for (let i = startPage; i <= endPage; i++) {
                paginationContainer.appendChild(createPageItem(i, i === page));
            }
    
            // Botón "Siguiente"
            const nextButton = document.createElement('li');
            nextButton.classList.add('page-item');
            nextButton.innerHTML = `
                <a class="page-link" aria-label="Next" href="#">
                    <span aria-hidden="true">»</span>
                </a>`;
            if (hasMoreData) {
                nextButton.querySelector('a').addEventListener('click', (event) => {
                    event.preventDefault();
                    fetchAndDisplayData(page + 1);
                });
            } else {
                nextButton.classList.add('disabled');
            }
            paginationContainer.appendChild(nextButton);
        });
    };
    
    // Llama a la función para cargar los datos de la primera página al inicio
    fetchAndDisplayData(currentPage);

});
