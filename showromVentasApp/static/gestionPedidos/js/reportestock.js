document.addEventListener("DOMContentLoaded", function () {
  let currentPage = 1; // Controlar la página actual
  const recordsPerPage = 20; // Cantidad de registros por página
  let activeFilters = {}; // Variable para almacenar los filtros aplicados

  const getSkip = (page) => (page - 1) * recordsPerPage;

  const applyFiltersAndFetchData = (filters, page = 1) => {
    showLoadingOverlay();
    const filterData = {
        top: recordsPerPage,
        page: page,  // Agregar la página actual
        filters: {
            nombre: filters.nombre || null,
            codigo: filters.codigo || null,
        }
    };

    // Guardar los filtros activos para que funcionen con la paginación
    activeFilters = filters;

    fetch("/ventas/productos/", {
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
        document.querySelector("#reporteStock").innerHTML = "";
        if (data && data.data && Array.isArray(data.data.value)) {
          displayProducts(data.data.value);

          // Verificar que totalRecords existe
          const totalRecords = data.totalRecords || 0;
          console.log("Total de registros:", totalRecords); // Para debug

          currentPage = page; // Actualizar la página actual
          updatePagination(page, data.totalRecords); // Modificar esta línea
          hideLoader();
        } else {
          console.error("Error: Expected data.data.value to be an array");
          displayProducts([]);
          updatePagination(1, 0); // Resetear paginación si no hay datos
          hideLoader();
        }
      })
      .catch((error) => {
        console.error("Error applying filters:", error);
        displayProducts([]);
        updatePagination(1, 0); // Resetear paginación en caso de error
        hideLoader();
      });
  };

  // Función para aplicar el filtro basado en el contenido del campo de búsqueda
  const aplicarFiltroDesdeBusqueda = () => {
    const searchText = document.querySelector("#buscarProductos").value.trim();

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
    document.querySelector("#buscarProductos").value = "";

    // Aplica los filtros y realiza la búsqueda
    const filters = getFilterData();
    applyFiltersAndFetchData(filters); // Aplica los filtros
    window.scrollTo(0, 0); // Desplazar hacia la parte superior de la página
  };

  // Evento para capturar texto en el campo de búsqueda y aplicar el filtro al presionar "Enter"
  document
    .querySelector("#buscarProductos")
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

  const displayProducts = (products) => {
    const tbody = document.querySelector("#reporteStock");
    tbody.innerHTML = "";
    showLoadingOverlay();

    products.forEach((product) => {
      // Función auxiliar para encontrar el stock de una bodega específica
      const getStockBodega = (idBodega) => {
        const bodega = product.bodegas.find((b) => b.id_Bodega === idBodega);
        return bodega ? bodega.stock_V : 0;
      };

      // Obtener stock para cada bodega
      const stockME = getStockBodega("ME");
      const stockPH = getStockBodega("PH");
      const stockLC = getStockBodega("LC");
      // quitar los decimales de los desucentos
      const descuentoTienda = Math.round(product.dsctoMaxTienda * 100);
      const descuentoProyecto = Math.round(product.dctoMaxProyectos * 100);

      const tr = document.createElement("tr");
      tr.innerHTML = `
                <td>${product.codigo}</td>
                <td>${product.nombre}</td>
                <td>${stockME}</td>
                <td>${stockPH}</td>
                <td>${stockLC}</td>
                <td style="text-align: center;">${product.stockTotal}</td>
                <td style="text-align: right;">${product.precioVenta}</td>
                <td style="text-align: center;">${descuentoTienda}</td>
                <td style="text-align: center;">${descuentoProyecto}</td>
            `;
      tbody.appendChild(tr);
    });

    hideLoadingOverlay();
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
