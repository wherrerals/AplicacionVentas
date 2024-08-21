function agregarInteractividad(newRow) {
  // Obtener referencias a los elementos dentro de la fila
  var inputCantidad = newRow.querySelector('#calcular_cantidad');
  var inputDescuento = newRow.querySelector('#agg_descuento'); 
  var spanPrecioVenta = newRow.querySelector('small[name="precio_venta"]');
  var tdPrecioVenta = newRow.querySelector('#precio_Venta'); 
  var tdPrecioDescuento = newRow.querySelector('#Precio_Descuento'); 
  
  // Select the small elements inside the divs by their ID
  var valorBruto = document.querySelector('#total_bruto small');
  var valorIva = document.querySelector('#iva small');
  var valorNeto = document.querySelector('#total_neto small');

  
  // Agregar evento de cambio al input de cantidad para calcular el precio total
  inputCantidad.addEventListener('input', calcularPrecioTotal);
  
  // Agregar evento de cambio al input de descuento para aplicar el descuento
  inputDescuento.addEventListener('input', aplicarDescuento);

  // Función para calcular el precio total
  function calcularPrecioTotal() {
    var cantidad = parseFloat(inputCantidad.value) || 0;
    var precioUnitario = parseFloat(spanPrecioVenta.textContent) || 0;
    var precioTotal = (cantidad * precioUnitario);
    var descuento = parseFloat(inputDescuento.value) || 0;

    var precioFinal = precioTotal - (precioTotal * (descuento / 100));
    var precioConDescuento = precioUnitario * (1 - (descuento / 100));
    
    tdPrecioVenta.textContent = precioFinal.toFixed(2);
    tdPrecioDescuento.textContent = precioConDescuento.toFixed(2);
    
    sumarPrecio(precioFinal);
  }

  // Función para aplicar el descuento
  function aplicarDescuento() {
    calcularPrecioTotal();
  }

  // Función para sumar el precio al valor neto
  function sumarPrecio(precioConDescuento) {

    // Calcular el IVA (19% del precio neto)
    var iva = precioConDescuento * 0.19;
    valorIva.textContent = '$' + iva.toFixed(0);

    // El precio bruto es el precio con descuento más el IVA
    var bruto = precioConDescuento;
    valorBruto.textContent = '$' + bruto.toFixed(0);

    // El precio neto es simplemente el precio con descuento
    var neto = precioConDescuento - iva;
    valorNeto.textContent = '$' + neto.toFixed(0);
}


  
  window.agregarInteractividad = agregarInteractividad;
};
