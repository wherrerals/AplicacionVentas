document.addEventListener("DOMContentLoaded", function () {
  let currentPage = 1; // Controlar la página actual
  const recordsPerPage = 20; // Cantidad de registros por página
  let activeFilters = {}; // Variable para almacenar los filtros aplicados

  const getSkip = (page) => (page - 1) * recordsPerPage;

  const applyFiltersAndFetchData = (filters, page = 1) => {
    showLoadingOverlay();
    const filterData = {
        top: recordsPerPage,
        page: page,

        filters: {
            id: filters.id || null,
            nombre: filters.nombre || null,
        }
    };

    activeFilters = filters;

    fetch("/ventas/solicitudes_pendientes/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(filterData),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then((data) => {
        console.log("Data:", data);
        document.querySelector("#listadoCotizaciones").innerHTML = "";
        if (data && data.data && Array.isArray(data.data.value)) {
          displayDocuments(data.data.value);
        
          currentPage = page; // Actualizar la página actual
          updatePagination(page, data.totalRecords); // Modificar esta línea
          hideLoader();
        } else {
          console.error("Error: Expected data.data.value to be an array");
          displayDocuments([]);
          updatePagination(1, 0); // Resetear paginación si no hay datos
          hideLoader();
        }
      })
      .catch((error) => {
        console.error("Error applying filters:", error);
        displayDocuments([]);
        updatePagination(1, 0); // Resetear paginación en caso de error
        hideLoader();
      });
  };

  // Función para aplicar el filtro basado en el contenido del campo de búsqueda
  const aplicarFiltroDesdeBusqueda = () => {
    const searchText = document.querySelector("#buscarlistacootizacion").value.trim();

    // Coloca el valor en el campo de filtro correspondiente
    if (!isNaN(searchText)) {
      // Número de documento (SAP)
      document.querySelector('[name="docNum"]').value = searchText;
    } else if (/^\d{1,4}[-\/]\d{1,2}[-\/]\d{1,4}$/.test(searchText)) {
      // Fecha en formato YYYY-MM-DD
      document.querySelector('[name="fecha_documento"]').value = searchText;
    } else if (
      [
        "abierto",
        "cerrado",
        "cancelado",
        "Abierto",
        "Cerrado",
        "Cancelado",
      ].includes(searchText)
    ) {
      // Estado del documento
      const estadoMap = {
        abierto: "O",
        cerrado: "C",
        cancelado: "Y",
        Abierto: "O",
        Cerrado: "C",
        Cancelado: "Y",
      };
      document.querySelector('[name="DocumentStatus"]').value =
        estadoMap[searchText];
    } else {
      // Nombre del cliente
      document.querySelector('[name="cardName"]').value = searchText;
    }

    // Limpiar el input de búsqueda después de colocar el valor
    document.querySelector("#buscarlistacootizacion").value = "";

    // Aplica los filtros y realiza la búsqueda
    const filters = getFilterData();
    applyFiltersAndFetchData(filters); // Aplica los filtros
    window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
  };

  // Evento para capturar texto en el campo de búsqueda y aplicar el filtro al presionar "Enter"
  document
    .querySelector("#buscarlistacootizacion")
    .addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        aplicarFiltroDesdeBusqueda();
      }
    });

  // Evento para aplicar el filtro al hacer clic en la lupa
  document
    .querySelector("#lupa-busqueda")
    .addEventListener("click", function () {
      aplicarFiltroDesdeBusqueda();
    });

  showLoadingOverlay();

const displayDocuments = (docs) => {
  const tbody = document.querySelector("#listadoCotizaciones");
  tbody.innerHTML = "";
  showLoadingOverlay();

  docs.forEach((doc) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><a href="#" class="id-link" data-id="${doc.id}">${doc.id}</a></td>
      <td><a href="#" class="cliente-link" data-cadcode="${doc.CardCode}">${doc.CardCode} - ${doc.nombre_cliente || 'Cliente Desconocido'}
      </a></td>
      <td>${doc.SalesEmployeeName || 'N/A'}</td>
      <td>${doc.fechaEntrega || '-'}</td>
      <td>${doc.estado_documento || '-'}</td>
      <td style="text-align: right;">${doc.totalDocumento?.toLocaleString() || 0}</td>
      <td style="text-align: right;">0</td>
    `;
    tbody.appendChild(tr);
  });

  // Agregar eventos después de insertar los elementos
  document.querySelectorAll('.id-link').forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const id = event.target.getAttribute('data-id');

      if (id) {
        showLoadingOverlay();
        window.location.href = `/ventas/solicitudes_devolucion/?id=${id}`;
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
            if (!response.ok) throw new Error('Error al obtener la información del cliente');
            return response.json();
          })
          .then(data => {
            console.log('Información del cliente:', data);
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

  hideLoadingOverlay();
};


  const getFilterData = () => {
    return {
        id: document.querySelector('[name="docNum"]').value,
        nombre: document.querySelector('[name="cardName"]').value,
    };
};


  const updatePagination = (page, totalRecords) => {
    console.log('Actualizando paginación:', { page, totalRecords }); // Para debug
    
    const totalPages = Math.ceil(totalRecords / recordsPerPage);
    const paginationContainers = document.querySelectorAll('.pagination');

    if (totalPages === 0) {
        // Si no hay páginas, ocultar o limpiar la paginación
        paginationContainers.forEach(container => {
            container.innerHTML = '';
        });
        return;
    }

    paginationContainers.forEach(paginationContainer => {
        // Limpiar contenido existente
        paginationContainer.innerHTML = '';

        // Botón "Anterior"
        const prevButton = document.createElement('li');
        prevButton.classList.add('page-item');
        if (page <= 1) prevButton.classList.add('disabled');
        prevButton.innerHTML = `
            <a class="page-link" aria-label="Previous" href="#">
                <span aria-hidden="true">«</span>
            </a>`;
        if (page > 1) {
            prevButton.querySelector('a').addEventListener('click', (event) => {
                event.preventDefault();
                fetchAndDisplayData(page - 1);
            });
        }
        paginationContainer.appendChild(prevButton);

        // Números de página
        for (let i = 1; i <= totalPages; i++) {
            if (
                i === 1 || // Primera página
                i === totalPages || // Última página
                (i >= page - 1 && i <= page + 1) // Páginas alrededor de la actual
            ) {
                const pageItem = document.createElement('li');
                pageItem.classList.add('page-item');
                if (i === page) pageItem.classList.add('active');
                pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
                pageItem.querySelector('a').addEventListener('click', (event) => {
                    event.preventDefault();
                    fetchAndDisplayData(i);
                });
                paginationContainer.appendChild(pageItem);
            } else if (
                (i === 2 && page > 3) || // Elipsis después de la primera página
                (i === totalPages - 1 && page < totalPages - 2) // Elipsis antes de la última página
            ) {
                const ellipsis = document.createElement('li');
                ellipsis.classList.add('page-item', 'disabled');
                ellipsis.innerHTML = '<span class="page-link">...</span>';
                paginationContainer.appendChild(ellipsis);
            }
        }

        // Botón "Siguiente"
        const nextButton = document.createElement('li');
        nextButton.classList.add('page-item');
        if (page >= totalPages) nextButton.classList.add('disabled');
        nextButton.innerHTML = `
            <a class="page-link" aria-label="Next" href="#">
                <span aria-hidden="true">»</span>
            </a>`;
        if (page < totalPages) {
            nextButton.querySelector('a').addEventListener('click', (event) => {
                event.preventDefault();
                fetchAndDisplayData(page + 1);
            });
        }
        paginationContainer.appendChild(nextButton);
    });
};

const fetchAndDisplayData = (page = 1) => {
    console.log('Obteniendo datos para página:', page); // Para debug
    applyFiltersAndFetchData(activeFilters, page);
    window.scrollTo(0, 0);
};
  // Llamar a la función para cargar la primera página con filtros activos al inicio
  fetchAndDisplayData(currentPage);

  // Escuchar el evento 'keydown' para capturar "Enter" en los campos de entrada
  const filterForm = document.querySelector("#filterForm");
  filterForm.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Evita que se envíe el formulario
      const filters = getFilterData();
      applyFiltersAndFetchData(filters); // Aplica los filtros cuando se presiona Enter
      window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
    }
  });

  // Escuchar el evento 'change' en los selectores para aplicar los filtros automáticamente
  const selects = document.querySelectorAll("select");
  selects.forEach((select) => {
    select.addEventListener("change", () => {
      const filters = getFilterData();
      applyFiltersAndFetchData(filters); // Aplicar los filtros cuando cambia el selector
    });
  });

  const attachClearEventListeners = () => {
    const filterInputs = document.querySelectorAll("#filterForm input");

    filterInputs.forEach((input) => {
      input.addEventListener("input", () => {
        if (input.value === "") {
          const filters = getFilterData();
          applyFiltersAndFetchData(filters); // Actualiza los datos cuando se borra un campo
        }
      });
    });
  };

  // Llamar a la función para agregar los eventos de limpiar filtros
  attachClearEventListeners();

  const urlParams = new URLSearchParams(window.location.search);
  const nombre = urlParams.get("nombre") || "";
  const id = urlParams.get("id") || "";

  // Si hay parámetros en la URL, aplicarlos automáticamente
  if (nombre || id) {
    // Colocar los valores en los campos correspondientes
    if (id) document.querySelector('[name="docNum"]').value = id;
    if (nombre) document.querySelector('[name="cardName"]').value = nombre;

    // Aplicar los filtros automáticamente
    const filters = getFilterData();
    applyFiltersAndFetchData(filters);
  }
});
