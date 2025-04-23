// Script para capturar datos de inputs y redirigir según corresponda
document.addEventListener('DOMContentLoaded', function() {
  // Mapa de ids de inputs a tipos de documentos
  const documentTypes = {
    'search_quotate': 'Quotations',
    'search_odv': 'Orders',
    'search_rr': 'ReturnRequest'
  };

  // Función para manejar la redirección según el input y el valor
  function handleSearch(inputId, svgId, urlPattern) {
    const searchInput = document.getElementById(inputId);
    const searchButton = document.getElementById(svgId);
    
    if (searchInput && searchButton) {
      // Función para procesar la búsqueda

      async function processSearch(searchValue) {
        if (searchValue) {
          try {
            // Obtener el tipo de documento correspondiente a este input
            const typeDocument = documentTypes[inputId];
            
            // Obtener el docEntry haciendo una consulta al endpoint
            showLoadingOverlay();

            const response = await fetch(`/ventas/get_docEntry/?docNum=${searchValue}&type_document=${typeDocument}`);
            const data = await response.json();
            
            // Verificar si el docEntry existe y es válido
            if (data && data !== null && data !== '' && data !== undefined) {
              // Construir la URL con el docEntry obtenido
              const redirectUrl = urlPattern.replace('${dato}', data);
              // Redirigir a la URL construida
              window.location.href = redirectUrl;
            } else {
              // Mostrar mensaje de error si el número de referencia no es correcto
              hideLoadingOverlay();
              alert("El número de referencia no es correcto.");
            }

          } catch (error) {
            console.error("Error al obtener docEntry:", error);
            alert("Ocurrió un error al buscar el documento. Por favor intente nuevamente.");
            hideLoadingOverlay();

          }
        }
      }
      
      // Evento de click para el botón de búsqueda
      searchButton.addEventListener('click', function() {
        const searchValue = searchInput.value.trim();
        processSearch(searchValue);
      });
      
      // También permitir búsqueda al presionar Enter en el input
      searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
          const searchValue = this.value.trim();
          processSearch(searchValue);
        }
      });
    }
  }
  
  // Configurar manejadores para cada par de input/botón
  handleSearch('search_quotate', 'search_quotate', '/ventas/generar_cotizacion/?docentry=${dato}');
  handleSearch('search_odv', 'search_odv', '/ventas/ordenesVentas/?docentry=${dato}');
  handleSearch('search_rr', 'search_rr', '/ventas/solicitudes_devolucion/?docentry=${dato}');
});