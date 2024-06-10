document.addEventListener("DOMContentLoaded", function() {
    fetch('prueba/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Verifica la estructura de los datos
            
            const tbody = document.querySelector('#listadoCotizaciones');
            
            // Asegúrate de que data contiene una clave "value" que es una lista
            const value = data.value || [];
            
            value.forEach(values => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><a href="cotizacion?docNum=${values.DocNum}">${values.DocNum}</a></td>
                    <td><a href="cliente.html">${values.CardName}</a></td>
                    <td>${values.SalesPersonCode}</td>
                    <td>${values.DocDate}</td>
                    <td>${values.SalesPersonCode}</td>
                    <td style="text-align: right;">${values.Cancelled}</td>
                    <td style="text-align: right;">${values.DocTotal}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error:', error));
}); 