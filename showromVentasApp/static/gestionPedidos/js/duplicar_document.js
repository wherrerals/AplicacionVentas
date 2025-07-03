document.addEventListener("DOMContentLoaded", function () {
  // Mostrar overlay de carga

  const savedLines = sessionStorage.getItem("documentLines");
  const cardCode = sessionStorage.getItem("cardCode");
  const tipoDocumento = sessionStorage.getItem("tipoDocumento");
  const folio_cotizacion = sessionStorage.getItem("folio");

  if (tipoDocumento == 'Solicitud') {

    console.log("Tipo de documento desde sessionStorage:", tipoDocumento);
    console.log("Card Code desde sessionStorage:", cardCode);
    traerInformacionCliente(cardCode);

    // agregar folio en el input folio_cotizacion

    const folioInput = document.getElementById("folio_referencia");
    const docentry_in_folio = sessionStorage.getItem("docentry_in_folio");

    if (folioInput && folio_cotizacion) {
      folioInput.value = folio_cotizacion;
      folioInput.setAttribute("data-refdocentr", docentry_in_folio); // Agregar el atributo data-docentry
    }


    // ✅ Eliminar después de usar  
    sessionStorage.removeItem("cardCode");
    sessionStorage.removeItem("folio");
    // folio in sessionStorage
    sessionStorage.removeItem("docentry_in_folio");
  }



  if (savedLines) {

    const documentLines = JSON.parse(savedLines);
    console.log("Usando líneas desde sessionStorage:", documentLines);

    documentLines.forEach((line, index) => {
      const linea_documento = line.LineNum;
      const docEntry_linea = line.DocEntry;
      const productoCodigo = line.ItemCode;
      const nombre = line.ItemDescription;
      const cantidadCoti = line.Quantity;
      const cantidad = cantidadCoti;
      const sucursal = line.WarehouseCode;
      const comentario = line.FreeText;
      const descuentoAplcado = line.DiscountPercent;
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

      console.log("Linea Documento:", linea_documento);
      if (cantidad > 0) {
        if (tipoDocumento == 'Solicitud') {
          //(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, descuentoAplcado)
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
            cantidad,
            sucursal,
            comentario,
            descuentoAplcado,
            cantidadCoti,
            precioCoti,
            // pasando el total de parametros = 16
          );

        } else {
          //(docEntry_linea, linea_documento, productoCodigo, nombre, imagen, precioVenta, stockTotal, precioLista, precioDescuento, cantidad, sucursal, comentario, descuentoAplcado)
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
          );
        }
      }
    }); //ok

    sessionStorage.removeItem("documentLines");

  } else {
    console.log("No se encontraron datos en sessionStorage. Verificando URL...");
    // (opcional) puedes mantener la lógica del fetch si deseas fallback
  }
});
