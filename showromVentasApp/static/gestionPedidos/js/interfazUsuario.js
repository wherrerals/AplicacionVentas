document.addEventListener("DOMContentLoaded", function () {
  function formatNumber(num) {
    return num < 10 ? "0" + num : num;
  }

  function sumarTresDias() {
    let hoy = new Date();
    let tresDiasDespues = new Date(hoy.getTime() + 10 * 24 * 60 * 60 * 1000);

    let dia = formatNumber(tresDiasDespues.getDate());
    let mes = formatNumber(tresDiasDespues.getMonth() + 1);
    let año = tresDiasDespues.getFullYear();

    let fechaFormateada = dia + "/" + mes + "/" + año;

    let fechaSAp = año + "-" + mes + "-" + dia;

    let diasVencidosLabel = document.getElementById("docDueDate");
    if (diasVencidosLabel) {
      diasVencidosLabel.textContent = fechaFormateada;
      // crear e insertar en el atributo  data-doc-due-date
      diasVencidosLabel.setAttribute("data-docDueDate", fechaSAp);
    } else {
      //console.error('Elemento con ID "docDueDate" no encontrado.');
    }
  }

  sumarTresDias();
});

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

// Oculta el botón de acciones si no hay número de cotización y deshabilita campos relacionados
document.addEventListener("DOMContentLoaded", function () {
  const elementosMonitoreados = [
    document.getElementById("numero_cotizacion"),
    document.getElementById("numero_orden"),
    document.getElementById("id_documento"),
  ].filter((elemento) => elemento); // Filtra elementos nulos o indefinidos

  const botonAcciones = document.querySelector(
    ".btn.btn-primary.dropdown-toggle"
  );
  const btn = document.querySelector("#botonacciones");
  const btn2 = document.querySelector("#botonmodalcontacto");
  const aprobar = document.getElementById("aprobar-1");
  const botonGuardado = document.querySelector("#saveButton");
  const botonGuardado2 = document.querySelector("#saveButton2");

  const estadoElemento = document.querySelector("#estado"); // Elemento para verificar estado

  // Campos que se deben deshabilitar
  const camposADeshabilitar = [
    document.getElementById("inputCliente"),
    document.getElementById("contactos_cliete"),
    //document.getElementById('contactos_cliete'),
    //document.getElementById('direcciones_despacho'),
    //document.getElementById('tipoEntrega-1'),
    //document.getElementById('direcciones_facturacion')
  ].filter((campo) => campo); // Filtra campos nulos o indefinidos

  function checkElementos() {
    console.log("Verificando elementos...");
    const tieneTexto = elementosMonitoreados.some(
      (elemento) => elemento.textContent.trim() !== ""
    );
    const noTieneTexto = elementosMonitoreados.every(
      (elemento) => elemento.textContent.trim() === ""
    );
    const estado = estadoElemento ? estadoElemento.textContent.trim() : "";
    const esEstadoInvalido = estado === "Cancelado" || estado === "Cerrado";

    // Ocultar o mostrar el botón de acciones
    botonAcciones.style.display = tieneTexto ? "inline-block" : "none";

    // Ocultar o mostrar el botón de acciones en la vista de impresión
    btn.style.display = tieneTexto ? "inline-block" : "none";

    // Ocultar o mostrar el botón de acciones en la vista de impresión
    botonGuardado.style.display =
      tieneTexto && !esEstadoInvalido ? "inline-block" : "none";
    botonGuardado2.style.display =
      tieneTexto && !esEstadoInvalido ? "inline-block" : "none";

    // Ocultar o mostrar el botón de acciones en la vista de impresión
    btn2.style.display = noTieneTexto ? "inline-block" : "none";

    // Ocultar o mostrar el botón de aprobar
    if (aprobar) {
      aprobar.style.display = tieneTexto ? "inline-block" : "none";
    }

    ocultar();

    // Deshabilitar o habilitar campos
    camposADeshabilitar.forEach((campo) => {
      campo.disabled = tieneTexto;
    });

    if (estado === "Abierta") {
      botonGuardado.style.display = "inline-block";
      botonGuardado2.style.display = "inline-block";
    }
  }

function ocultar() {
  const estado = document.getElementById("estado").textContent.trim();
  const btn = document.getElementById("copiar-ODV");
  const btn2 = document.getElementById("botonacciones");
  const aprobar = document.getElementById("aprobar-1");
  const numeroOrden = document.getElementById("numero_orden");

  console.log(estado);

  if (estado === "Cerrado" || estado === "Cancelado") {
    if (btn) btn.style.display = "none";
    if (btn2) btn2.style.display = "none";
    console.log("Oculto");
  } else {
    if (btn) btn.style.display = "block";
    if (btn2) btn2.style.display = "block";
    console.log("Visible");
  }

  // Verificar que ambos elementos existen antes de operar
  if (numeroOrden && aprobar) {
    const numeroOrdenTexto = numeroOrden.textContent.trim();

    if (numeroOrdenTexto !== "") {
      aprobar.style.display = "none";
      console.log("Oculto botón Aprobar");
    } else {
      aprobar.style.display = "block";
      console.log("Mostrar botón Aprobar");
    }
  }
}


  // Verificar el estado inicial
  ocultar();
  checkElementos();

  // Configurar observadores para todos los elementos monitoreados
  elementosMonitoreados.forEach((elemento) => {
    const observer = new MutationObserver(checkElementos);
    observer.observe(elemento, { childList: true, subtree: true });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const today = new Date();
  const formattedDate = today.toISOString().split("T")[0]; // Formato YYYY-MM-DD
  document.getElementById("fecha_entrega").value = formattedDate;
});
