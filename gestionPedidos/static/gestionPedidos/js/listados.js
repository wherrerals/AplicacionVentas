document.addEventListener("DOMContentLoaded", function() {
    let nextPageLink = 'listado_Cotizaciones/'; // URL inicial o primera página
    
    const fetchAndDisplayData = (url) => {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data); // Verifica la estructura de los datos
                
                const tbody = document.querySelector('#listadoCotizaciones');
                tbody.innerHTML = ''; // Limpiar tabla antes de agregar nuevas filas
                
                const value = data.value || [];
                
                value.forEach(entry => {
                    const quotation = entry.Quotations || {};
                    const salesPerson = entry.SalesPersons || {};
    
                    const vatSumFormatted = quotation.DocTotalNeto.toLocaleString('es-ES', {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 2
                    });
    
                    const docTotalFormatted = quotation.DocTotal.toLocaleString('es-ES', {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 2
                    });
                    
                    const getStatus = (quotation) => {
                        if (quotation.Cancelled === 'Y') {
                            return 'Cancelado';
                        } else if (quotation.DocumentStatus === 'O') {
                            return 'Abierto';
                        } else if (quotation.DocumentStatus === 'C') {
                            return 'Cerrado';
                        } else {
                            return 'Activo';
                        }
                    };
    
                    const status = getStatus(quotation);
    
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><a href="generar_cotizacion?docNum=${quotation.DocNum}" data-doc-entry="${entry.DocEntry}" data-document-lines="[]">${quotation.DocNum}</a></td>
                        <td><a href="cliente.html">${quotation.CardName}</a></td>
                        <td>${salesPerson.SalesEmployeeName || ''}</td>
                        <td>${quotation.DocDate}</td>
                        <td>${status}</td>
                        <td style="text-align: right;">$ ${vatSumFormatted}</td>
                        <td style="text-align: right;">$ ${docTotalFormatted}</td>
                    `;
                    tbody.appendChild(tr);
                });
                
                // Guarda el enlace para la siguiente página si está disponible
                nextPageLink = data['@odata.nextLink'] || null;
            })
            .catch(error => console.error('Error:', error));
    };
    
    // Función inicial para cargar los datos
    fetchAndDisplayData(nextPageLink);
    
    // Event listener para el botón de siguiente página
    const nextButton = document.querySelector('#nextButton');
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (nextPageLink) {
                fetchAndDisplayData(nextPageLink);
            }
        });
    }
});
