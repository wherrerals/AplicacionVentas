function agregarInteractividad(newRow) {
  // Obtener referencias a los elementos dentro de la fila
  var inputCantidad = newRow.querySelector('#calcular_cantidad');
  var inputDescuento = newRow.querySelector('#agg_descuento'); 
  var spanPrecioVenta = newRow.querySelector('small[name="precio_venta"]');
  var tdPrecioVenta = newRow.querySelector('#precio_Venta'); 
  var tdPrecioDescuento = newRow.querySelector('#Precio_Descuento'); 
  
  var valorBruto = document.getElementById('total_bruto');
  var valorIva = document.getElementById('iva');
  var valorNeto = document.getElementById('total_neto');
  
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

    var dctoFinal = (descuento / 100);
    console.log("Descuento final:", dctoFinal); // Debug: Verifica el descuento final
    var precioConDescuento = precioTotal * (descuento / 100);
    console.log("Precio con descuento calculado:", precioConDescuento); // Debug: Verifica el cálculo del precio con descuento

    
    tdPrecioVenta.textContent = precioTotal.toFixed(2);
    tdPrecioDescuento.textContent = precioConDescuento.toFixed(2);
    
    sumarPrecio(precioConDescuento);
  }

  // Función para aplicar el descuento
  function aplicarDescuento() {
    calcularPrecioTotal();
  }

  // Función para sumar el precio al valor neto
  function sumarPrecio(precioUnitario) {
    var bruto = parseFloat(valorBruto.textContent.replace('$', '')) || 0;
    var iva = parseFloat(valorIva.textContent.replace('$', '')) || 0;
    var neto = parseFloat(valorNeto.textContent.replace('$', '')) || 0;

    bruto += precioUnitario;
    valorBruto.textContent = '$' + bruto.toFixed(0);

    iva = bruto * 0.19;
    valorIva.textContent = '$' + iva.toFixed(0);

    neto = bruto - iva;
    valorNeto.textContent = '$' + neto.toFixed(0);
    console.log("Valor neto actualizado:", neto); // Debug: Verifica el valor neto actualizado
    console.log("Valor bruto actualizado:", bruto); // Debug: Verifica el valor bruto actualizado
    console.log("Valor IVA actualizado:", iva); // Debug: Verifica el valor IVA actualizado
  }
  
  window.agregarInteractividad = agregarInteractividad;
};
