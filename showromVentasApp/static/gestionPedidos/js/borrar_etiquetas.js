// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {

    // Función para eliminar etiquetas HTML por ID
    function eliminarEtiquetaPorId(id) {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.remove(); // Elimina el elemento si existe
            console.log(`El elemento con ID ${id} ha sido eliminado.`);
        } else {
            console.log(`No se encontró el elemento con ID ${id}.`);
        }
    }

    // Event listener para el enlace con id "agregar_dir_despacho"
    document.getElementById("agregar_dir_despacho").addEventListener("click", function () {
        eliminarEtiquetaPorId("dirmens1"); // Eliminar el <p> con id="dirmens1"
    });

    document.getElementById("agregar_dir_facturacion").addEventListener("click", function () {
        eliminarEtiquetaPorId("dirmens1"); // Eliminar el <p> con id="dirmens1"
    });
    

    // Opción para reutilizar la función en otros enlaces en el futuro
    function agregarEventoEliminarEnlace(idEnlace, idElementoAEliminar) {
        document.getElementById(idEnlace).addEventListener("click", function () {
            eliminarEtiquetaPorId(idElementoAEliminar);
        });
    }

    // Ejemplo de cómo usar la función genérica para otros enlaces
    // agregarEventoEliminarEnlace("idDelOtroEnlace", "idDelElementoAEliminar");

});
