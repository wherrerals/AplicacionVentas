document.addEventListener("DOMContentLoaded", function () {
    // Función para obtener parámetros de la URL
    function getQueryParam(param) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
    }
  
    // Manejo de docEntry
    const docEntry = getQueryParam('docentry');
  
      fetch(`/ventas/duplicar_cotizacion/?docentry=${docEntry}`)
        .then(response => {
          if (!response.ok) throw new Error('Error al duplicar cotización');
          return response.json();
        })
        .then(data => {
          if (data.Cliente && data.Cliente.SalesPersons) {
            console.log("Datos de la cotización:", data);

  
            // Iteración sobre `DocumentLines` para añadir cada producto
            const documentLines = data.DocumentLines;
            documentLines.forEach((line) => {
              console.log("Producto: ", line)
              const productoCodigo = line.ItemCode;
              const nombre = line.ItemDescription;
              const imagen = 'ruta_a_la_imagen.jpg';
              const precioVenta = line.PriceAfterVAT;
              const stockTotal = 0;
              const precioLista = line.GrossPrice;
              const precioDescuento = line.DiscountPercent;
  
              console.log("Agregando producto con datos:", {
                productoCodigo,
                nombre,
                imagen,
                precioVenta,
                stockTotal,
                precioLista,
                precioDescuento
              });
  
              agregarProducto(productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, line.Quantity, sucursal);
            });
          }
        })
        .catch(error => {
          console.error('Error en la solicitud AJAX:', error);
          if (vendedorDataElement) {
            vendedorDataElement.innerText = "Error al cargar datos";
          }
        });
  });