document.addEventListener('DOMContentLoaded', function () {

    // Asignar el evento de click al botón con id 'duplicar-1'
    document.getElementById("duplicar-1").addEventListener("click", duplicarCotizacion);

    // Lista de elementos que no deben ser modificados (sus ID no deben ser limpiados)
    const excludeIds = [
        "stock_total", "descuento", "precio_venta", "precio_Venta", 
        "precio_Descuento", "eliminarp", "tipoEntrega", "fechaEntrega"
    ];

    // Método para limpiar todos los datos dentro de un contenedor
    function duplicarCotizacion() {
        // Obtener el contenedor de la cotización a limpiar
        var cotizacion = document.getElementById("contenedor");

        // Limpiar los campos dentro del contenedor (inputs, textareas, selects)
        var inputs = cotizacion.querySelectorAll("input, textarea, select");
        inputs.forEach(function(input) {
            // Solo limpiar si el id del input no está en la lista de exclusión
            if (!excludeIds.includes(input.id)) {
                input.value = "";  // Limpiar el valor de cada campo
            }
        });

        // Limpiar elementos con 'id' y 'data-*' (atributos 'data-*' válidos)
        var elementos = cotizacion.querySelectorAll("[id], [data-]");
        elementos.forEach(function(elemento) {
            // Si el id está en la lista de exclusión, no limpiar este elemento
            if (excludeIds.includes(elemento.id)) {
                return;  // No hacer nada si está en la lista de exclusión
            }

            // Limpiar valores o atributos según corresponda
            if (elemento.tagName === "P" && elemento.id === "numero_cotizacion") {
                // Limpiar el contenido del párrafo
                elemento.innerHTML = "";
                // Limpiar cualquier atributo "data-docEntry"
                elemento.setAttribute("data-docEntry", "");
            } else if (elemento.hasAttribute("data-docEntry")) {
                // Limpiar otros atributos "data-*"
                elemento.removeAttribute("data-docEntry");
            } else if (elemento.value !== undefined) {
                // Limpiar el valor de otros elementos como inputs o selects si tienen valor
                elemento.value = "";
            }
        });

        // Si deseas limpiar más tipos de datos o elementos, puedes agregar más lógica aquí
    }
});


