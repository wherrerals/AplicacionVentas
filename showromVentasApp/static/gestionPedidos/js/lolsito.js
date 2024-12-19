// Asegurarse de que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function () {

    // Asignar el evento de click al botón con id 'duplicar-1'
    document.getElementById("duplicar-1").addEventListener("click", duplicarCotizacion);

    // Método para limpiar todos los datos dentro de un contenedor
    function duplicarCotizacion() {
        // Obtener el contenedor de la cotización a limpiar
        var cotizacion = document.getElementById("contenedor");

        // Limpiar los campos dentro del contenedor (inputs, textareas, selects)
        var inputs = cotizacion.querySelectorAll("input, textarea, select");
        inputs.forEach(function(input) {
            input.value = "";  // Limpiar el valor de cada campo
        });

        // Limpiar elementos con 'id' y 'data-*' (atributos 'data-*' válidos)
        var elementos = cotizacion.querySelectorAll("[id], [data-]");
        elementos.forEach(function(elemento) {
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

