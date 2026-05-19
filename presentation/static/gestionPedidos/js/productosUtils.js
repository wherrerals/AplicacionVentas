// productosUtils.js
// Helpers compartidos entre productos.js (cotizacion) y productoODV.js (orden de venta).
// Debe cargarse ANTES de cualquiera de esos archivos.

const BODEGA_MAP = {
    "LC": "LC",
    "PH": "PH",
    "ME": "ME",
    "VI": "VI",
    "GR": "GR"
};

async function obtenerStockBodegas(codigoProducto) {
    try {
        const response = await fetch(`/ventas/obtener_stock_bodegas/?idProducto=${codigoProducto}`);
        if (!response.ok) {
            throw new Error("Error al obtener el stock");
        }
        return await response.json();
    } catch (error) {
        console.error("Error al obtener el stock:", error);
        return null;
    }
}

function aplicarUICupon(newRow, cuponDescuento) {
    if (!cuponDescuento || Number(cuponDescuento) <= 0) return;

    const descuentoCupon = Number(cuponDescuento);

    const inputDescuento = newRow.querySelector('#agg_descuento');
    if (inputDescuento) {
        inputDescuento.max = descuentoCupon;
        inputDescuento.value = 0;
        inputDescuento.setAttribute('disabled', 'disabled');
    }

    const descElem = newRow.querySelector('#desc_cupon');
    if (descElem) {
        descElem.textContent = `Cupon: ${descuentoCupon}%`;
        descElem.hidden = false;
        descElem.dataset.value = descuentoCupon;
    }
}

function agregarTooltipStockBodegas(row, codigoProducto) {
    const elem = row.querySelector('#stock_total');
    if (!elem) return;

    elem.addEventListener('mouseover', async () => {
        const stockData = await obtenerStockBodegas(codigoProducto);
        if (!stockData) return;

        const stockFiltrado = stockData.filter(bodega => bodega.bodega in BODEGA_MAP);
        const tooltipContent = stockFiltrado
            .map(bodega => `${bodega.bodega}: ${bodega.stock_disponible}`)
            .join('\n');

        elem.title = `Stock en otras tiendas:\n${tooltipContent}`;
    });
}

function actualizarIndicesProductos() {
    document.querySelectorAll('.product-row').forEach((fila, index) => {
        const indiceElemento = fila.querySelector('#indixe_producto');
        if (indiceElemento) {
            indiceElemento.textContent = `${index + 1})`;
        }
    });
}

let draggedRow = null;

function inicializarDragAndDrop(fila) {
    const handle = fila.querySelector('#drag-handle');

    if (handle) {
        handle.addEventListener('mousedown', () => {
            fila.setAttribute('draggable', 'true');
        });
        handle.addEventListener('mouseup', () => {
            fila.setAttribute('draggable', 'false');
        });
    }

    fila.addEventListener('dragstart', (e) => {
        if (!fila.getAttribute('draggable') || fila.getAttribute('draggable') === 'false') {
            e.preventDefault();
            return;
        }
        draggedRow = fila;
        setTimeout(() => fila.classList.add('dragging'), 0);
        e.dataTransfer.effectAllowed = 'move';
    });

    fila.addEventListener('dragend', () => {
        fila.setAttribute('draggable', 'false');
        fila.classList.remove('dragging');
        draggedRow = null;
        limpiarIndicadores();
    });

    fila.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';

        if (fila === draggedRow) return;

        limpiarIndicadores();

        const rect = fila.getBoundingClientRect();
        const midY = rect.top + rect.height / 2;

        if (e.clientY < midY) {
            fila.classList.add('drag-over-top');
        } else {
            fila.classList.add('drag-over-bottom');
        }
    });

    fila.addEventListener('dragleave', (e) => {
        if (!fila.contains(e.relatedTarget)) {
            fila.classList.remove('drag-over-top', 'drag-over-bottom');
        }
    });

    fila.addEventListener('drop', (e) => {
        e.preventDefault();

        if (!draggedRow || fila === draggedRow) return;

        const container = fila.parentNode;
        const rect = fila.getBoundingClientRect();
        const midY = rect.top + rect.height / 2;

        if (e.clientY < midY) {
            container.insertBefore(draggedRow, fila);
        } else {
            container.insertBefore(draggedRow, fila.nextSibling);
        }

        limpiarIndicadores();
        recalcularIndices();
    });
}

function limpiarIndicadores() {
    document.querySelectorAll('.product-row').forEach(f => {
        f.classList.remove('drag-over-top', 'drag-over-bottom');
    });
}

function recalcularIndices() {
    document.querySelectorAll('tbody.product-row').forEach((fila, index) => {
        const nuevoIndice = index + 1;
        fila.setAttribute('id', nuevoIndice);

        const indiceTd = fila.querySelector('[id="indixe_producto"]');
        if (indiceTd) {
            indiceTd.textContent = `${nuevoIndice})`;
            indiceTd.setAttribute('data-indice', nuevoIndice);
        }
    });
}

/**
 * Normaliza los argumentos de agregarProducto(...).
 *
 * Si rawArgs es `[opts]` con un único objeto plano, lo devuelve tal cual
 * (forma nueva: agregarProducto({ ... })).
 *
 * En caso contrario asume forma posicional y mapea cada índice a la clave
 * correspondiente de `ordenPosicional` (forma vieja: agregarProducto(a, b, c, ...)).
 *
 * Permite migrar agregarProducto a una firma única basada en objeto
 * sin romper los call sites existentes que pasan args posicionales.
 */
function argsAOpts(rawArgs, ordenPosicional) {
    if (
        rawArgs.length === 1 &&
        rawArgs[0] !== null &&
        typeof rawArgs[0] === 'object' &&
        !Array.isArray(rawArgs[0])
    ) {
        return rawArgs[0];
    }
    const opts = {};
    ordenPosicional.forEach((key, i) => {
        opts[key] = rawArgs[i];
    });
    return opts;
}

/**
 * Formatea un valor numérico como moneda chilena: `$ 1.234`.
 * Usa Math.floor para descartar decimales (precios CLP enteros).
 * Maneja el caso de 4 dígitos sin separador de miles que toLocaleString
 * a veces omite ("1234" → "1.234").
 */
function formatCurrency(value) {
    const integerValue = Math.floor(value);
    let formattedValue = integerValue.toLocaleString('es-ES', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
    if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
        formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
    }
    return `$ ${formattedValue}`;
}
