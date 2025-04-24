document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1; // Controlar la página actual
    const recordsPerPage = 20; // Cantidad de registros por página
    let totalPages = null; // No conocemos el total de páginas inicialmente
    let activeFilters = {}; // Variable para almacenar los filtros aplicados

    const getSkip = (page) => (page - 1) * recordsPerPage;

    // Capturar el valor dinámico seleccionado por defecto en el filtro del vendedor
    const vendedorSelect = document.querySelector('#filtro_vendedor');
    const defaultVendedorValue = vendedorSelect.value; // Obtener el valor seleccionado por defecto

    activeFilters['salesEmployeeName'] = defaultVendedorValue;


    const applyFiltersAndFetchData = (filters, page = 1) => {
        showLoadingOverlay();
        const skip = getSkip(page); // Calcular el número de registros a omitir
        const filterData = {
            top: recordsPerPage,
            skip,
            ...filters
        };

        // Guardar los filtros activos para que funcionen con la paginación
        activeFilters = filters;

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
            document.querySelector('#listSales').innerHTML = '';
            if (data && data.data && Array.isArray(data.data.value)) {
                displayQuotations(data.data.value);

                // Si el backend devuelve el número total de registros
                if (data.totalRecords) {
                    totalPages = Math.ceil(data.totalRecords / recordsPerPage);
                }

                updatePagination(page); // Actualizar la paginación
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

// Función para aplicar el filtro basado en el contenido del campo de búsqueda
const aplicarFiltroDesdeBusqueda = () => {
    const searchText = document.querySelector('#buscarlistacootizacion').value.trim();

    // Coloca el valor en el campo de filtro correspondiente
    if (!isNaN(searchText)) {
        // Número de documento (SAP)
        document.querySelector('[name="docNum"]').value = searchText;
    } else if (/^\d{1,4}[-\/]\d{1,2}[-\/]\d{1,4}$/.test(searchText)) {
        // Fecha en formato YYYY-MM-DD
        document.querySelector('[name="fecha_documento"]').value = searchText;
    } else if (["abierto", "cerrado", "cancelado", "Abierto", "Cerrado", "Cancelado"].includes(searchText)) {
        // Estado del documento
        const estadoMap = {
            "abierto": "O",
            "cerrado": "C",
            "cancelado": "Y",
            "Abierto": "O",
            "Cerrado": "C",
            "Cancelado": "Y"
        };
        document.querySelector('[name="DocumentStatus"]').value = estadoMap[searchText];
    } else {
        // Nombre del cliente
        document.querySelector('[name="cardName"]').value = searchText;
    }

    // Limpiar el input de búsqueda después de colocar el valor
    document.querySelector('#buscarlistacootizacion').value = '';

    // Aplica los filtros y realiza la búsqueda
    const filters = getFilterData();
    applyFiltersAndFetchData(filters); // Aplica los filtros
    window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
};

// Evento para capturar texto en el campo de búsqueda y aplicar el filtro al presionar "Enter"
document.querySelector('#buscarlistacootizacion').addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); 
        aplicarFiltroDesdeBusqueda();
    }
});

// Evento para aplicar el filtro al hacer clic en la lupa
document.querySelector('#lupa-busqueda').addEventListener('click', function() {
    aplicarFiltroDesdeBusqueda();
});

showLoadingOverlay();

    const displayQuotations = (quotations) => {
        const tbody = document.querySelector('#listSales');
        tbody.innerHTML = '';
    
        showLoadingOverlay();
        quotations.forEach(entry => {
            const quotation = entry.Quotations || {};
            const salesPerson = entry.SalesPersons || {};
            function formatCurrency(value) {
                // Convertimos el valor a número entero
                const integerValue = Math.floor(value);
                let formattedValue = integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
            
                // Si el valor tiene 4 dígitos y no incluye un punto, lo añadimos manualmente
                if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
                    formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
                }
            
                // Agregamos el símbolo de peso al principio
                return `$ ${formattedValue}`;
            }
            
            // Aplicamos la función a los valores necesarios
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

            date = quotation.DocDate
            let partesFecha = date.split("-");

            // Cambia el orden de las partes para obtener "dd/mm/aaaa"
            let fechaFormateada = `${partesFecha[2]}/${partesFecha[1]}/${partesFecha[0]}`;
    
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><a href="#" class="docentry-link" data-docentry="${quotation.DocEntry}">${quotation.DocNum}</a></td>
                <td><a href="#" class="docentry-link" data-docentry="${quotation.DocEntry}">${quotation.DocNum}</a></td>
                <td><a href="#" class="docentry-link" data-docentry="${quotation.DocEntry}">${quotation.DocNum}</a></td>
                <td><a href="#" class="cliente-link" data-cadcode="${quotation.CardCode}">${quotation.CardCode} - ${quotation.CardName || 'Cliente Desconocido'}</a></td>
                <td>${salesPerson.SalesEmployeeName || 'N/A'}</td>
                <td>${fechaFormateada}</td>
                <td>${status}</td>
                <td style="text-align: right;"> ${vatSumFormatted}</td>
                <td style="text-align: right;"> ${docTotalFormatted}</td>
            `;
            tbody.appendChild(tr);
        });
        
        document.querySelectorAll('.docentry-link').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const docEntry = event.target.getAttribute('data-docentry');
            
            if (docEntry) {
                showLoadingOverlay();
                // Redirige a la página de generación de cotización con docentry en la URL
                window.location.href = `/ventas/generar_cotizacion/?docentry=${docEntry}`;
            } else {
                hideLoadingOverlay();
                alert("No se pudo obtener el DocEntry de la cotización.");
            }
        });
    });

    hideLoadingOverlay();


        // Agrega el evento click a todos los enlaces de clientes después de añadir las filas
        document.querySelectorAll('.cliente-link').forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                let cadCode = event.target.getAttribute('data-cadcode');
        
                // Eliminar la "C" final si está presente
                if (cadCode && cadCode.endsWith("C") || cadCode && cadCode.endsWith("c")) {
                    cadCode = cadCode.slice(0, -1);
                }
        
                if (cadCode) {
                    showLoadingOverlay();
                    // Realiza la solicitud AJAX al backend para obtener la información del cliente
                    fetch(`/ventas/informacion_cliente/?rut=${cadCode}`)
                        .then(response => {
                            if (!response.ok) throw new Error('Error al obtener la información del cliente');
                            return response.json();
                        })
                        .then(data => {
                            console.log('Información del cliente:', data);
        
                            // Redirige a la página de creación de cliente después de obtener los datos
                            window.location.href = `/ventas/creacion_clientes/?rut=${cadCode}`;
                        })
                        .catch(error => {
                            hideLoadingOverlay();
                            console.error('Error en la solicitud AJAX:', error);
                        });
                } else {
                    hideLoadingOverlay();
                    alert("No se pudo obtener el RUT del cliente.");
                }
            });
        });
        ;
    };
    
    const getFilterData = () => {
        return {
            fecha_inicio: document.querySelector('[name="fecha_inicio"]').value,
            fecha_fin: document.querySelector('[name="fecha_fin"]').value,
            fecha_doc: document.querySelector('[name="fecha_documento"]').value,
            docNum: document.querySelector('[name="docNum"]').value,
            carData: document.querySelector('[name="cardName"]').value,
            salesEmployeeName: document.querySelector('#filtro_vendedor').value,
            DocumentStatus: document.querySelector('[name="DocumentStatus"]').value,
            docTotal: document.querySelector('[name="docTotal"]').value
        };
    };


    const updatePagination = (page) => {
        console.log('Updating pagination:', { page, totalPages });

        const paginationContainers = document.querySelectorAll('.pagination');
    
        paginationContainers.forEach(paginationContainer => {
            paginationContainer.innerHTML = ''; // Limpiar la paginación actual
    
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
        applyFiltersAndFetchData(activeFilters, page);
        window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
    };
    

    // Llamar a la función para cargar la primera página con filtros activos al inicio
    fetchAndDisplayData(currentPage);

    // Escuchar el evento 'keydown' para capturar "Enter" en los campos de entrada
    const filterForm = document.querySelector('#filterForm');
    filterForm.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Evita que se envíe el formulario
            const filters = getFilterData();
            applyFiltersAndFetchData(filters); // Aplica los filtros cuando se presiona Enter
            window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
        }
    });

    // Escuchar el evento 'change' en los selectores para aplicar los filtros automáticamente
    const selects = document.querySelectorAll('select');
    selects.forEach(select => {
        select.addEventListener('change', () => {
            const filters = getFilterData();
            applyFiltersAndFetchData(filters); // Aplicar los filtros cuando cambia el selector
        });
    });

    const attachClearEventListeners = () => {
        const filterInputs = document.querySelectorAll('#filterForm input');
        
        filterInputs.forEach(input => {
            input.addEventListener('input', () => {
                if (input.value === '') {
                    const filters = getFilterData();
                    applyFiltersAndFetchData(filters); // Actualiza los datos cuando se borra un campo
                }
            });
        });
    };

    // Llamar a la función para agregar los eventos de limpiar filtros
    attachClearEventListeners();

    // Selecciona los campos de bruto y neto
    const inputBruto = document.getElementById('buscar_bruto');
    const inputNeto = document.getElementById('buscar_neto');

    // Escucha los cambios en el campo de bruto
    inputBruto.addEventListener('input', function() {
    // Convierte el valor del bruto a número y calcula el neto
    const brutoValue = parseFloat(inputBruto.value) || 0;
    const netoValue = brutoValue * 0.84;

    // Muestra el valor calculado en el campo neto
    inputNeto.value = netoValue; // Limita a 2 decimales
    });
    

    const urlParams = new URLSearchParams(window.location.search);
    const rutSN = urlParams.get("rutSN") || "";
    const nombreSN = urlParams.get("nombreSN") || "";
  
    // Si hay parámetros en la URL, aplicarlos automáticamente
    if (rutSN || nombreSN) {
      console.log("Aplicando filtros desde la URL:", { rutSN, nombreSN });
  
      // Colocar los valores en los campos correspondientes
      if (rutSN) document.querySelector('[name="cardName"]').value = rutSN;
      if (nombreSN) document.querySelector('[name="cardName"]').value = nombreSN;
  
      // Aplicar los filtros automáticamente
      const filters = getFilterData();
      applyFiltersAndFetchData(filters);
    }

});