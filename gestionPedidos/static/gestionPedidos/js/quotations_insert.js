document.addEventListener('DOMContentLoaded', function () {
    // Función para obtener el valor de un parámetro de consulta
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    const docNum = getQueryParam('docNum');
    if (docNum) {
        fetch(`detalleCotizacion/${docNum}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(docData => {
                const container = document.getElementById('cotizacionContainer');
                container.innerHTML = `
                            <h1>Cotización ${docData.DocNum}</h1>
                            <p>Cliente: ${docData.CardName}</p>
                            <p>Vendedor: ${docData.vendedor}</p>
                            <p>Fecha: ${docData.DocDate}</p>
                            <p>Código del Vendedor: ${docData.SalesPersonCode}</p>
                            <p>Cancelado: ${docData.Cancelled}</p>
                            <p>Total: ${docData.DocTotal}</p>
                            <!-- Agrega más campos según tu estructura de datos -->
                        `;
            })
            .catch(error => console.error('Error:', error));
    } else {
        console.error('No se proporcionó DocNum en la URL.');
    }
});

