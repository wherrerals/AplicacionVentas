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
                // Accede a Quotations dentro de entry
                const quotation = entry.Quotations || {};
                const salesPerson = entry.SalesPersons || {};

                // Crea una fila para cada entrada en value
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><a href="generar_cotizacion?docNum=${quotation.DocNum}" data-doc-entry="${entry.DocEntry}" data-document-lines="[]">${quotation.DocNum}</a></td>
                    <td><a href="cliente.html">${quotation.CardName}</a></td>
                    <td>${salesPerson.SalesEmployeeName}</td>
                    <td>${quotation.DocDate}</td>
                    <td>${quotation.Cancelled}</td>
                    <td style="text-align: right;">$ ${quotation.VatSum}</td>
                    <td style="text-align: right;">$ ${quotation.DocTotal}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error:', error));
});
