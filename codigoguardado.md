# Limitar cantidad segun stock bodega (producto.js)

```
// Limitar el selector de cantidad según el stock de la bodega seleccionada
const cantidadInput = row.querySelector('#calcular_cantidad');
cantidadInput.max = stockBodega;

// Ajustar el valor actual si excede el nuevo stock máximo
if (parseInt(cantidadInput.value, 10) > stockBodega) {
    cantidadInput.value = stockBodega;
}
```
