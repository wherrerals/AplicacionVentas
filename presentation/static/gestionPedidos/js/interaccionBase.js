// interaccionBase.js
// Clase base compartida por productosInteraccion{,2,3}.js (cotización + ODV,
// solic_devolución, salesConsultation). Cada pantalla carga UN solo archivo
// productosInteraccion*.js, así que en la práctica las subclases viven
// aisladas entre sí. Esta base concentra el estado común y permite que
// cada subclase implemente sólo lo que difiere (calcularValores).
//
// Debe cargarse ANTES del archivo productosInteraccion*.js correspondiente.

class ValorTributarioBase {
    constructor(codigoProducto, precioFinal, indiceProducto, uid = null) {
        this.codigoProducto = codigoProducto;
        this.precioFinal = precioFinal;
        this.indiceProducto = indiceProducto; // referencia informativa
        this.uid = uid;                       // llave estable cuando aplica (cotización/ODV)
    }

    modificarPrecioFinal(precioFinal) {
        this.precioFinal = precioFinal;
    }

    // calcularValores() debe ser implementado por las subclases.
    // Cada pantalla tiene reglas matemáticas distintas (bruto/neto/iva).
}

// Array global de productos tributarios activos en la pantalla actual.
// Compartido entre la clase y agregarInteractividad/actualizarValores
// del archivo productosInteraccion*.js cargado.
const productos = [];
