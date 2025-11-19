document.addEventListener("DOMContentLoaded", () => {
  const userSelect = document.getElementById("inputCliente");

  if (userSelect) {
    // Detectar cuando se borra el input del cliente
    userSelect.addEventListener("input", async function () {
      if (this.value.trim() === "") {
        console.log("Cliente borrado. Obteniendo precios originales...");


        const couponInput = document.getElementById("cupon_data");
        if (couponInput && couponInput.value.trim() !== "") {
            console.log("Cliente borrado → cupón activo encontrado, eliminando...");
            couponInput.value = "";      
            restaurarEstadoCupon();      // llama al script 2
        }

        // Paso 1: capturar los productos actuales
        const productos = capturarProductosActuales();
        if (productos.length === 0) {
          console.log("No hay productos cargados.");
          return;
        }

        try {
          // Paso 2: enviar los SKUs al servidor
          const response = await fetch("/ventas/restaurar-precios/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ productos }),
          });

          if (!response.ok)
            throw new Error("Error al obtener precios desde el servidor");

          const data = await response.json();
          console.log("Precios obtenidos:", data);

          // Paso 3: actualizar precios con los nuevos valores
          actualizarPreciosDesdeServidor(data);
        } catch (error) {
          console.error("Error restaurando precios:", error);
        }
      }
    });
  }
});

// Captura los productos cargados actualmente en la tabla
function capturarProductosActuales() {
  const filasProductos = document.querySelectorAll("tbody.product-row");
  const productos = [];

  filasProductos.forEach((row) => {
    const sku = row
      .querySelector('small[name="sku_producto"]')
      ?.textContent?.trim();
    if (sku) productos.push({ sku });
  });

  return productos;
}

// Actualiza los precios en base a los datos que vienen del servidor
function actualizarPreciosDesdeServidor(data) {
  if (typeof productos !== "undefined" && Array.isArray(productos)) {
    productos.length = 0; // Vaciar array global de productos tributarios
    console.log("🧹 Limpieza: array 'productos' reiniciado.");
  }

  const filasProductos = document.querySelectorAll("tbody.product-row");

  filasProductos.forEach((row) => {
    const skuElem = row.querySelector('small[name="sku_producto"]');
    const precioVentaElem = row.querySelector('small[name="precio_venta"]');
    const inputCantidad = row.querySelector("#calcular_cantidad");
    const descuento = row.querySelector('small[name="descuento_max"]');

    console.log("descuento elem:", descuento);

    let  inputDescuento = row.querySelector("#agg_descuento");
    if (inputCantidad) {
      const clone = inputCantidad.cloneNode(true);
      inputCantidad.parentNode.replaceChild(clone, inputCantidad);
    }

    if (inputDescuento) {
      const clone = inputDescuento.cloneNode(true);
      inputDescuento.parentNode.replaceChild(clone, inputDescuento);
      inputDescuento = clone; // 🔄 referenciar el nuevo nodo
    }

    if (!skuElem || !precioVentaElem) return;

    const sku = skuElem.textContent.trim();
    const productoServidor = data.find((p) => p.codigo === sku);

    if (productoServidor && productoServidor.precio) {
      const nuevoPrecio = parseFloat(productoServidor.precio);
      const maxDescuento = productoServidor.maxDescuento || 0;

      inputDescuento.setAttribute("max", maxDescuento);
      inputDescuento.value = Math.min(inputDescuento.value, maxDescuento); // opcional

      const nuevoDescuento = maxDescuento;
      descuento.textContent = `Max: ${nuevoDescuento}%`;

      // Actualizar el atributo y texto del precio
      precioVentaElem.setAttribute("data-preciounitario", nuevoPrecio);
      precioVentaElem.textContent = formatCurrency(nuevoPrecio);

      // Paso 4: forzar recálculo de totales
      if (inputCantidad) {
        inputCantidad.dispatchEvent(new Event("input", { bubbles: true }));
      }

      if (inputDescuento) {
        inputDescuento.dispatchEvent(new Event("input", { bubbles: true }));
      }
    }
  });

  filasProductos.forEach((row) => {
    const sku = row
      .querySelector('small[name="sku_producto"]')
      ?.textContent?.trim();
    const indiceProducto =
      row.querySelector("#indixe_producto")?.dataset?.indice;

    if (sku && indiceProducto) {
      agregarInteractividad(row, sku, indiceProducto);
    }
  });
}

// Formatea el precio al formato local CLP o el que uses

function formatCurrency(value) {
  // Convertimos el valor a número entero
  const integerValue = Math.floor(value);
  let formattedValue = integerValue.toLocaleString("es-ES", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  });

  // Si el valor tiene 4 dígitos y no incluye un punto, lo añadimos manualmente
  if (
    integerValue >= 1000 &&
    integerValue < 10000 &&
    !formattedValue.includes(".")
  ) {
    formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
  }

  // Agregamos el símbolo de peso al principio
  return `$ ${formattedValue}`;
}

async function actualizarPreciosPorCliente(cardcode) {
  console.log("🔄 Actualizando precios para cliente:", cardcode);

  const productos = capturarProductosActuales();
  if (productos.length === 0) {
    console.log("No hay productos cargados, no se actualizarán precios.");
    return;
  }

  try {
    const response = await fetch("/ventas/restaurar-precios/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ productos, cardcode }),
    });

    if (!response.ok)
      throw new Error("Error al obtener precios desde el servidor");

    const data = await response.json();
    console.log("✅ Precios cliente obtenidos:", data);

    actualizarPreciosDesdeServidor(data);
  } catch (error) {
    console.error("Error actualizando precios del cliente:", error);
  }
}
