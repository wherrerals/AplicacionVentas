document.addEventListener("DOMContentLoaded", function () {
    // Mostrar overlay de carga

    const savedLines = sessionStorage.getItem("documentLines");
  
    if (savedLines) {
      const documentLines = JSON.parse(savedLines);
      console.log("Usando líneas desde sessionStorage:", documentLines);
  
      documentLines.forEach((line, index) => {
        const linea_documento = index;
        const docEntry_linea = line.DocEntry_line;
        const productoCodigo = line.ItemCode;
        const nombre = line.ItemDescription;
        const cantidadCoti = line.Quantity;
        const cantidad = cantidadCoti;
        const sucursal = line.WarehouseCode;
        const comentario = line.FreeText;
        const descuentoAplcado =0;
        const tipoentrega2 = line.ShippingMethod;
  
        // Opcional: si no tienes stock ni imagen, se puede dejar en null o ajustar
        const imagen = line.imagen;
        const precioVenta = line.Price;
        const stockTotal = '';
        const precioLista = line.PriceList;
        const precioDescuento = line.descuentoMax;
        const stockBodega = '';
        const precioCoti = line.Price;
  
        const isSVProduct = productoCodigo.startsWith("SV");
  
        setTimeout(() => {
          document
            .querySelectorAll(`.valorCotizacion[data-itemcode="${productoCodigo}"]`)
            .forEach((elementoLinea) => {
              if (isSVProduct) {
                elementoLinea.setAttribute("hidden", "true");
              } else {
                elementoLinea.setAttribute("hidden", cantidadCoti > (stockBodega || 0) ? "false" : "true");
              }
            });
        }, 100);

        agregarProducto(
          docEntry_linea,
          linea_documento,
          productoCodigo,
          nombre,
          imagen,
          precioVenta,
          stockTotal,
          precioLista,
          precioDescuento,
          cantidad,
          sucursal,
          comentario,
          descuentoAplcado,
          cantidadCoti,
          precioCoti
          // pasando el total de parametros = 16
        );
      });
  
      sessionStorage.removeItem("documentLines");
  
    } else {
      console.log("No se encontraron datos en sessionStorage. Verificando URL...");
      // (opcional) puedes mantener la lógica del fetch si deseas fallback
    }
  });
  