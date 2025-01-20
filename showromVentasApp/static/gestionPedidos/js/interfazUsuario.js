document.addEventListener('DOMContentLoaded', function () {
    function formatNumber(num) {
        return num < 10 ? '0' + num : num;
    }

    function sumarTresDias() {
        let hoy = new Date();
        let tresDiasDespues = new Date(hoy.getTime() + (10 * 24 * 60 * 60 * 1000));

        let dia = formatNumber(tresDiasDespues.getDate());
        let mes = formatNumber(tresDiasDespues.getMonth() + 1);
        let año = tresDiasDespues.getFullYear();

        let fechaFormateada = año + '-' + mes + '-' + dia;

        let diasVencidosLabel = document.getElementById('docDueDate');
        if (diasVencidosLabel) {
            diasVencidosLabel.textContent = fechaFormateada;
        } else {
            //console.error('Elemento con ID "docDueDate" no encontrado.');
        }
    }

    sumarTresDias();
});

function formatCurrency(value) {
    // Convertimos el valor a número entero
    const integerValue = Math.floor(value);
    let formattedValue = integerValue.toLocaleString('es-ES', { minimumFractionDigits: 0, maximumFractionDigits: 2 });

    // Si el valor tiene 4 dígitos y no incluye un punto, lo añadimos manualmente
    if (integerValue >= 1000 && integerValue < 10000 && !formattedValue.includes(".")) {
        formattedValue = `${formattedValue.slice(0, 1)}.${formattedValue.slice(1)}`;
    }

    // Agregamos el símbolo de peso al principio
    return `$ ${formattedValue}`;
}

document.addEventListener('DOMContentLoaded', function () {
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0]; // Formato YYYY-MM-DD
    document.getElementById('fecha_entrega').value = formattedDate;
});

// Oculta el botón de acciones si no hay número de cotización y deshabilita campos relacionados
document.addEventListener('DOMContentLoaded', function () {
    const elementosMonitoreados = [
        document.getElementById('numero_cotizacion'),
        document.getElementById('numero_orden')
    ].filter(elemento => elemento); // Filtra elementos nulos o indefinidos

    const botonAcciones = document.querySelector('.btn.btn-primary.dropdown-toggle');
    const btn = document.querySelector('#botonacciones');

    // Campos que se deben deshabilitar
    const camposADeshabilitar = [
        document.getElementById('inputCliente'),
        document.getElementById('contactos_cliete'),
        //document.getElementById('contactos_cliete'),
        //document.getElementById('direcciones_despacho'),
        //document.getElementById('tipoEntrega-1'),
        //document.getElementById('direcciones_facturacion')
    ].filter(campo => campo); // Filtra campos nulos o indefinidos

    function checkElementos() {
        const tieneTexto = elementosMonitoreados.some(elemento => elemento.textContent.trim() !== '');

        // Ocultar o mostrar el botón de acciones
        botonAcciones.style.display = tieneTexto ? 'inline-block' : 'none';

        // Ocultar o mostrar el botón de acciones en la vista de impresión
        btn.style.display = tieneTexto ? 'inline-block' : 'none';

        // Deshabilitar o habilitar campos
        camposADeshabilitar.forEach(campo => {
            campo.disabled = tieneTexto;
        });
    }

    // Verificar el estado inicial
    checkElementos();

    // Configurar observadores para todos los elementos monitoreados
    elementosMonitoreados.forEach(elemento => {
        const observer = new MutationObserver(checkElementos);
        observer.observe(elemento, { childList: true, subtree: true });
    });
});

