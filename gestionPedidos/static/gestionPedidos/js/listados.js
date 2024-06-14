document.addEventListener("DOMContentLoaded", function() {
    fetch('debug/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Verifica la estructura de los datos
            
            const tbody = document.querySelector('#listadoCotizaciones');
            
            // Asegúra que data contiene una clave "value" que es una lista
            const value = data.value || [];
            
            value.forEach(entry => {
                // Obténiene DocumentLines para este entry
                const documentLines = entry.DocumentLines || [];

                // Serializa documentLines a JSON
                const documentLinesJSON = JSON.stringify(documentLines);

                // Crear una fila para cada entry en value
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><a href="generar_cotizacion?docNum=${entry.DocNum}" data-doc-entry="${entry.DocEntry}" data-document-lines="${documentLinesJSON}">${entry.DocNum}</a></td>
                    <td><a href="cliente.html">${entry.CardName}</a></td>
                    <td>${entry.SalesPersonCode}</td>
                    <td>${entry.DocDate}</td>
                    <td>${entry.Cancelled}</td>
                    <td style="text-align: right;">${entry.VatSum}</td>
                    <td style="text-align: right;">${entry.DocTotal}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error:', error));
});
