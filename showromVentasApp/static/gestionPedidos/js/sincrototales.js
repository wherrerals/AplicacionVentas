async function manejarSwitches() {
  const switches = document.querySelectorAll(".switch-producto");
  const totalBrutoDiv = document.getElementById("total_bruto");
  const folioInput = document.querySelector("#folio_referencia");
  const folio = folioInput ? folioInput.getAttribute("data-refdocentr") : null;

  console.log("Total bruto div:", totalBrutoDiv);
  console.log("Folio input element:", folioInput);
  console.log("Folio capturado:", folio);
  console.log("Switches:", switches);

  function areAllSwitchesChecked() {
    const result = Array.from(switches).every(sw => sw.checked);
    console.log("Todos los switches están marcados:", result);
    return result;
  }

  async function actualizarTotalBruto() {
    if (!folio) {
      console.warn("No se encontró folio para la consulta.");
      return;
    }

    const response = await fetch(`/ventas/get_doctotal/?folio=${encodeURIComponent(folio)}`);
    if (!response.ok) throw new Error("Error en la respuesta");

    const data = await response.json();
    const nuevoTotal = data.doctotal;

    console.log("Nuevo total bruto:", nuevoTotal);

    totalBrutoDiv.dataset.totalBruto = nuevoTotal;
    totalBrutoDiv.textContent = `$ ${nuevoTotal.toLocaleString('es-CL')}`;
  }

  if (areAllSwitchesChecked()) {
    await actualizarTotalBruto();
  } else {
    console.log("No todos los switches están marcados, no se actualiza el total bruto.");
  }
}


function initSwitches() {
  const switches = document.querySelectorAll(".switch-producto");

  // Sincronizar estado inicial basado en data-estado
  switches.forEach(sw => {
    const estado = sw.dataset.estado;
    sw.checked = estado === "1";
  });

  // Registrar listeners
  switches.forEach(sw => {
    sw.addEventListener("change", () => {
      sw.dataset.estado = sw.checked ? "1" : "0";
      manejarSwitches();
    });
  });

  manejarSwitches();
}

document.addEventListener("DOMContentLoaded", initSwitches);

