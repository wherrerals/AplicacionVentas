// Crear un nuevo documento de ventas
document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("grabar-btn").addEventListener("click", submitForm);
    
    function submitForm() {
        // Capturar los datos del documento

        const name = document.getElementById("nombreSN").value;
        const apellido = document.getElementById("apellidoSN").value;
        const nombre_completo = name + ' ' + apellido; // Agregar un espacio entre nombre y apellido
        const rut = document.getElementById("rutSN").value;
        const telefono = document.getElementById("telefonoSN").value;
        const salesPersonCode = "-1";
        //const salesPersonCode = document.getElementById("salesPersonCode").getAttribute("data-salespersoncode");

        // Capturando el valor del radio button seleccionado
        const grupoSNSeleccionado = document.querySelector('input[name="grupoSN"]:checked').value;
        let tipoDoc = grupoSNSeleccionado === "105" ? "105" : "100"; // Asignar "Persona" o "Empresa"

        const giro = document.getElementById("giroSN").value;
        const email = document.getElementById("emailSN").value;


        // Captura las líneas del documento
        const dirs = [];

        // Selecciona todas las líneas de cada producto
        const dirRows = document.querySelectorAll('.dir-row');

        dirRows.forEach((row) => {
            const direccionSelecionada = document.querySelector('input[name="tipodireccion"]:checked').value;
            let tipoDir = direccionSelecionada === "12" ? "Despacho" : "Facturación"; // Asignar "Despacho" o "Facturación"
            const nameDir = row.querySelector("[name='nombre_direccion[]'").value;
            const paisDir = row.querySelector("[name='pais[]']").value;
            const regionDir = row.querySelector("[name='region[]']").value;
            const ciudadDir = row.querySelector("[name='ciudad[]']").value;
            const comunaDir = row.querySelector("[name='comuna[]']").value;
            const calleDir = row.querySelector("[name='direccion[]']").value;

            // Crea un objeto con los datos direcion
            const dir = {
                "AddressName": nameDir,
                "Street": calleDir,
                "City": ciudadDir,
                "County": comunaDir,
                "Country": paisDir,
                "State": regionDir,
                "FederalTaxID": rut,
                "TaxCode": "IVA",
                "AddressType": tipoDir,
            };
            dirs.push(dir);
        });

        const contacs = [];

        const contacRows = document.querySelectorAll('.contac-row');

        contacRows.forEach((row) => {
            const nameContac = row.querySelector("[name='nombre_contacto']").value;
            const lastNameContac = row.querySelector("[name='apellido_contacto']").value;
            const telefonoContac = row.querySelector("[name='telefono_contacto']").value;
            const celularContac = row.querySelector("[name='celular_contacto']").value;
            const emailContac = row.querySelector("[name='email_contacto']").value;

            const contac = {
                "Name": nameContac + ' ' + lastNameContac,
                "Phone1": telefonoContac,
                "MobilePhone": celularContac,
                "E_Mail": emailContac,
                "LastName": lastNameContac,
                "FirstName": nameContac,
            };

            contacs.push(contac);
        });


        // Crea el objeto final que será enviado en formato JSON
        const documentData = {
            "CardCode": rut,
            "CardName": nombre_completo,
            "CardType": tipoDoc,
            "GroupCode": grupoSNSeleccionado,
            "Phone1": telefono,
            "Phone2":telefono,
            "Notes": "Persona",
            "PayTermsGrpCode": -1,
            "FederalTaxID": null,
            "SalesPersonCode": salesPersonCode,
            "Cellular": telefono,
            "EmailAddress": email,
            "CardForeignName": name + ' ' + apellido,
            "ShipToDefault": "DESPACHO",
            "BilltoDefault": "FACTURACION",
            "DunningTerm": "ESTANDAR",
            "CompanyPrivate": "cPrivate",
            "AliasName": nombre_completo,
            "U_Tipo": "N",
            "U_FE_Export": "N",
            "BPAddresses": dirs,
            "ContactEmployees": contacs,
        };

        // Convertir a JSON
        const jsonData = JSON.stringify(documentData);
        console.log(jsonData);

        // Enviar los datos al backend usando fetch
        fetch('/ventas/crear_cliente/', {
            method: 'POST', // Método POST para enviar datos
            headers: {
                'Content-Type': 'application/json', // Indica que el cuerpo es JSON
                'X-CSRFToken': getCSRFToken() // Obtener el token CSRF si es necesario en Django
            },
            body: jsonData // Datos en formato JSON
        })

            .then(response => {
                if (response.ok) {
                    return response.json(); // Procesar respuesta si es exitosa
                } else {
                    throw new Error('Error en la creación del Cliente');
                }
            })
            .then(data => {
                console.log('Documento creado exitosamente:', data);
                // Puedes hacer algo aquí como redirigir al usuario o mostrar un mensaje de éxito
                if (data.success) {
                    // Mostrar el número de documento y el mensaje de éxito en un popup bonito
                    Swal.fire({
                        icon: 'success',
                        title: 'Cotización creada',
                        text: `Cliente Creado: ${data.cardCode}`,
                        confirmButtonText: 'Aceptar'
                    });

                    const numeroCotizacion = document.getElementById('numero_cotizacion');

                    if (numeroCotizacion) {
                        numeroCotizacion.textContent = `${data.docNum}`;
                    }


                } else {
                    // Mostrar el mensaje de error en un popup
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: `Error al crear El Cliente: ${data.message}`,
                        confirmButtonText: 'Aceptar'
                    });
                }
            })


            .catch(error => {
                console.error('Hubo un error al crear el Cliente:', error);
            });
    }

    // Función para obtener el token CSRF (si usas Django)
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});

