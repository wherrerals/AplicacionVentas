function agregarInteractividad(newRow) {
    // Obtener referencias a los elementos dentro de la fila
    var inputCantidad = newRow.querySelector('#calcular_cantidad'); // Cambié el selector a class
    var inputDescuento = newRow.querySelector('#agg_descuento'); // Cambié el selector a class
    var spanPrecioVenta = newRow.querySelector('#precio_Venta'); // Cambié el selector a class
    var tdPrecioVenta = newRow.querySelector('#precio_Venta'); // Cambié el selector a class
    var tdPrecioDescuento = newRow.querySelector('#Precio_Descuento'); // Cambié el selector a class
    var valorBruto = document.getElementById('total_bruto');
    var valorIva = document.getElementById('iva');
    var valorNeto= document.getElementById('total_neto');
    
    // Agregar evento de cambio al input de cantidad para calcular el precio total
    inputCantidad.addEventListener('input', calcularPrecioTotal);
    
    // Agregar evento de cambio al input de descuento para aplicar el descuento
    inputDescuento.addEventListener('input', aplicarDescuento);
  
    // Función para calcular el precio total
    function calcularPrecioTotal() {
      var cantidad = parseFloat(inputCantidad.value) || 0;
      var precioUnitario = parseFloat(spanPrecioVenta.textContent) || 0;
      var precioTotal = cantidad * precioUnitario;
      var descuento = parseFloat(inputDescuento.value) || 0;
      var precioConDescuento = precioTotal - (precioTotal * (descuento / 100));
      
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
      console.log("Sumar precio ejecutado"); // Agregar un console.log para verificar si se ejecuta
      var bruto = parseFloat(valorBruto.textContent.replace('$', '')) || 0; // Inicializar a 0 si no hay valor
      var iva = parseFloat(valorIva.textContent.replace('$', '')) || 0;
      var neto = parseFloat(valorNeto.textContent.replace('$', '')) || 0;
  
      bruto += precioUnitario;
      valorBruto.textContent = '$' + bruto.toFixed(0); // Mostrar total con dos decimales
  
      iva = bruto * 0.19;
      valorIva.textContent = '$' + iva.toFixed(0);
  
      neto = bruto - iva;
      valorNeto.textContent = '$' + neto.toFixed(0);
      
    }
    
    window.agregarInteractividad = agregarInteractividad;
  };