document.addEventListener("DOMContentLoaded", function() {
    fetch('testing1/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Verifica la estructura de los datos
            // Verifica si data es un objeto
            if (typeof data === 'object' && data !== null) {
                // Si data es un objeto, conviértelo en un array de un solo elemento
                const dataArray = [data];
                const tbody = document.querySelector('#listadoCotizaciones');
                dataArray.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><a href="cotizacion.html">${item.sap}</a></td>
                        <td><a href="cliente.html">${item.cliente}</a></td>
                        <td>${item.vendedor}</td>
                        <td>${item.fecha}</td>
                        <td>${item.estado}</td>
                        <td style="text-align: right;">${item.neto}</td>
                        <td style="text-align: right;">${item.bruto}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } else {
                console.error('Expected an object but got:', data);
            }
        })
        .catch(error => console.error('Error:', error));
});
