document.addEventListener("DOMContentLoaded", function () {
    const baseURL = '/ventas/filtrar_socios_negocio/';
    let currentPage = 1; // Página actual
    const recordsPerPage = 20; // Cantidad de registros por página
    let hasMoreData = true; // Determina si hay más datos para cargar

    const getSkip = (page) => (page - 1) * recordsPerPage;


    const getFilterData = () => {
        // Captura el valor seleccionado en el filtro tipoSN
        const tipoSNValue = document.querySelector('[name="tipoSN"]').value.trim();

        // Convierte el valor a "Persona" o "Empresa"
        const tipoSNText = tipoSNValue === "105" ? "Persona" : tipoSNValue === "100" ? "Empresa" : "";

        const filters = {
            codigo: document.querySelector('[name="codigo"]').value.trim(),
            nombre: document.querySelector('[name="nombre"]').value.trim(),
            telefono: document.querySelector('[name="telefono"]').value.trim(),
            email: document.querySelector('[name="email"]').value.trim(),
            tipoSN: document.querySelector('[name="tipoSN"]').value.trim() //Captura el codigo
            //tipoSN: tipoSNText //Captura el Nombre
        };
        
        console.log("Filtros capturados:", filters);
        return filters;
    };
    

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
            const filters = getFilterData(); // Captura los filtros
            const payload = {
                top: recordsPerPage,
                skip: skip,
                filters: filters,
            };

                    // Agrega un console.log para verificar el payload antes de enviarlo
        console.log("Payload enviado al servidor:", payload);

            fetch(baseURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload), // Convertimos el objeto en JSON
            })
                .then(response => {
                    if (!response.ok) throw new Error('Error al obtener los datos del servidor');
                    return response.json();
                })
                .then(data => {
                    if (data.value && Array.isArray(data.value)) {
                        displayClients(data.value);
                        console.log(data); // Aquí puedes ver la estructura de los datos


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

    const applySearchFromBuscador = () => {
        const searchText = document.querySelector('#buscador').value.trim();

        if (!searchText) {
            console.log("El buscador está vacío, limpiando filtros...");
            // Limpia todos los filtros
            document.querySelectorAll('.form-control, .form-select').forEach(filter => filter.value = '');
            fetchAndDisplayData(1);
            return;
        }
        console.log("Texto ingresado en el buscador:", searchText);
        // Determinar a qué filtro pertenece el texto ingresado
        if (/^\d+$/.test(searchText)) {
            // Es un código (solo números)
            document.querySelector('[name="codigo"]').value = searchText;
            console.log("entro en codigo ")

        } else if (searchText.toLowerCase() === 'persona' || searchText.toLowerCase() === 'empresa') {
            // Es el tipo (Persona o Empresa)
            const tipoMap = { persona: '12', empresa: '13' };
            document.querySelector('[name="tipo"]').value = tipoMap[searchText.toLowerCase()];
            console.log("entro en tipo ")
        } else if (/^\+/.test(searchText)) {
            // Es un teléfono (empieza con "+")
            document.querySelector('[name="telefono"]').value = searchText;
            console.log("entro en telefono ")
        } else if (/@/.test(searchText)) {
            // Es un email (contiene "@")
            document.querySelector('[name="email"]').value = searchText;
            console.log("entro en email ")
        } else {
            // Se asume que es un nombre si no encaja en las otras categorías
            document.querySelector('[name="nombre"]').value = searchText;
            console.log("entro en nombre ")
        }

        console.log("Aplicando búsqueda con filtro identificado:", getFilterData());
        fetchAndDisplayData(1);
    };

    // Agregar evento al hacer clic en la lupa
    document.querySelector('#lupa-busqueda').addEventListener('click', () => {
        applySearchFromBuscador();
    });

    // Evento para buscar al presionar "Enter" en el buscador
    document.querySelector('#buscador').addEventListener('keydown', (event) => {
        if (event.key === "Enter") {
            event.preventDefault(); // Evitar que el formulario se envíe
            applySearchFromBuscador(); // Ejecutar búsqueda
        }
    });

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


    // Agregar evento keydown para aplicar filtros al presionar "Enter"
    document.querySelectorAll('.form-control, .form-select').forEach(filter => {
        filter.addEventListener('keydown', (event) => {
            if (event.key === "Enter") { // Detectar la tecla Enter
                event.preventDefault(); // Evitar el envío del formulario

                const filters = getFilterData(); // Capturar los datos de los filtros
                console.log("Filtros aplicados al presionar Enter:", filters);

                fetchAndDisplayData(1); // Realizar la búsqueda desde la primera página
            }
        });
    });


    // Agregar eventos a los inputs para buscar al borrar contenido o al presionar la "x"
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('input', () => {
            if (input.value.trim() === '') {
                console.log("Filtro vacío, aplicando búsqueda...");
                fetchAndDisplayData(1);
            }
        });
    });

    // Agregar eventos a los selects para buscar al cambiar la selección
    document.querySelectorAll('.form-select').forEach(select => {
        select.addEventListener('change', () => {
            console.log("Filtro modificado en selector, aplicando búsqueda...");
            fetchAndDisplayData(1);
        });
    });

    // Llama a la función para cargar los datos de la primera página al inicio
    fetchAndDisplayData(currentPage);

});
