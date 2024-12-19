function togglePassword() {
    let toggleButton = document.getElementById("togglePasswordButton");
    let passwordInput = document.getElementById("password");

    // Verificar si los elementos existen antes de agregar el evento
    if (toggleButton && passwordInput) {
        toggleButton.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                toggleButton.textContent = "Ocultar";
            } else {
                passwordInput.type = "password";
                toggleButton.textContent = "Mostrar";
            }
        });
    }
}

togglePassword();

function toggleRepeatPassword() {
    let toggleButton = document.getElementById("toggleRepeatPasswordButton");
    let passwordInput = document.getElementById("rep_clave");

    // Verificar si los elementos existen antes de agregar el evento
    if (toggleButton && passwordInput) {
        toggleButton.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                toggleButton.textContent = "Ocultar";
            } else {
                passwordInput.type = "password";
                toggleButton.textContent = "Mostrar";
            }
        });
    }
}

toggleRepeatPassword();


// archivo formularioReactivo.js

function cambiarLabel(razonSocialRadioName, nombreLabelId, apellidoInputId, apellidolabelId) {
    var razonSocialRadio = document.getElementsByName(razonSocialRadioName);
    var nombreLabel = document.getElementById(nombreLabelId);
    var apellidoInput = document.getElementById(apellidoInputId);
    var apellidolabel = document.getElementById(apellidolabelId);

    if (razonSocialRadio[0].checked) {
        nombreLabel.textContent = 'Nombre';
        apellidoInput.style.display = 'block'; // Mostrar input de apellido
        apellidolabel.style.display = 'block'; // Mostrar label de apellido
    } else if (razonSocialRadio[1].checked) {
        nombreLabel.textContent = 'R. Social';
        apellidoInput.style.display = 'none'; // Ocultar input de apellido
        apellidolabel.style.display = 'none'; // Ocultar label de apellido
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const duplicarOpcion = document.getElementById('duplicar');

    if (duplicarOpcion) {
        duplicarOpcion.addEventListener('click', function (event) {
            event.preventDefault(); // Evitar acción predeterminada del enlace

            console.log('Evento click detectado en "Duplicar".');

            // Crear una nueva pestaña
            const nuevaVentana = window.open('', '_blank');
            if (nuevaVentana) {
                const docOriginal = document.documentElement.cloneNode(true);

                // Crear una estructura HTML completa en la nueva pestaña
                nuevaVentana.document.open();
                nuevaVentana.document.write(`
                    <!DOCTYPE html>
                    <html>
                        <head>
                            ${document.head.innerHTML} <!-- Clonar el contenido del <head> -->
                        </head>
                        <body>
                            ${document.body.innerHTML} <!-- Clonar el contenido del <body> -->
                        </body>
                    </html>
                `);
                nuevaVentana.document.close();
                console.log('Nueva pestaña creada con el contenido duplicado.');

                // Ejecutar la función global definida en ajax__clientes.js
                nuevaVentana.onload = function () {
                    if (typeof nuevaVentana.limpiarInformacionCliente === 'function') {
                        nuevaVentana.limpiarInformacionCliente();
                        console.log('Función limpiarInformacionCliente ejecutada en la nueva pestaña.');
                    } else {
                        console.error('La función limpiarInformacionCliente no está definida en la nueva pestaña.');
                    }
                };
            } else {
                alert('No se pudo abrir una nueva pestaña. Verifica bloqueadores de pop-ups.');
                return;
            }

            // Cerrar el menú desplegable
            const dropdownMenu = duplicarOpcion.closest('.dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.classList.remove('show');
            }

            // Asegúrate de cerrar también el botón de toggle
            const dropdownToggle = duplicarOpcion.closest('.dropdown').querySelector('.dropdown-toggle');
            if (dropdownToggle) {
                dropdownToggle.setAttribute('aria-expanded', 'false');
            }
        });
    } else {
        //console.error('No se encontró el enlace "Duplicar". Verifica el id.');
    }
});

const cerrarButton = document.getElementById("cerrar");

// Verificar si el elemento existe antes de agregar el evento
if (cerrarButton) {
    cerrarButton.addEventListener("click", function (event) {
        event.preventDefault();
        handleAction("cerrar");
    });
} else {
    //console.warn('El botón con ID "cerrar" no existe en el DOM.');
}

const cancelarButton = document.getElementById("cancelar");
if (cancelarButton) {
    cancelarButton.addEventListener("click", function (event) {
        event.preventDefault();
        handleAction("cancelar");
    });
} else {
    //console.warn('El botón con ID "cerrar" no existe en el DOM.');
}



function handleAction(action) {
    const numeroCotizacion = document.getElementById("numero_cotizacion").innerText;
    const estado = action === "cerrar" ? "Close" : "Cancel";

    // Crear objeto de datos a enviar
    const payload = {
        DocNum: numeroCotizacion,
        Estado: estado
    };

    // Limpiar mensajes previos antes de mostrar nuevos
    limpiarMensajes();

    // Realizar POST con los datos
    fetch('/ventas/cambiar_estado_cotizacion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => {
            if (response.ok) {
                return response.json(); // Continuar para procesar la respuesta del servidor
            } else {
                // Mostrar mensaje de error con el estado de la respuesta
                mostrarMensaje("Error en la solicitud. Estado: " + response.statusText, "error");
                throw new Error("Respuesta no exitosa del servidor.");
            }
        })
        .then(data => {
            if (data.success) { // Suponiendo que el servidor retorna un campo 'success'
                mostrarMensaje("Acción realizada con éxito.", "success");
            } else {
                mostrarMensaje(data.message || "Se produjo un error desconocido.", "error");
            }
        })
        .catch(error => {
            // Mostrar mensaje de error si falla el POST
            console.error("Error al realizar el POST:", error);
            mostrarMensaje("Error al procesar la solicitud: " + error.message, "error");
        });

}

document.addEventListener('DOMContentLoaded', function () {
    const generarPDF = document.getElementById('generarPDF');

    if (generarPDF) {
        generarPDF.addEventListener('click', function () {
            const { jsPDF } = window.jspdf; // Accede a jsPDF desde window.jspdf

            // Inicializa el PDF
            const pdf = new jsPDF();

            // Captura los datos del cliente
            const rutSN = document.getElementById('rutSN')?.value || 'No disponible';
            const nombreSN = document.getElementById('nombreSN')?.value || '';
            const apellidoSN = document.getElementById('apellidoSN')?.value || '';
            const grupoSN = document.querySelector('input[name="grupoSN"]:checked')?.nextElementSibling?.textContent.trim() || 'No especificado';
            const direccion = document.getElementById('nombreDireccion_0')?.value || 'No disponible';
            const contactoNombre = document.getElementById('nombre_0')?.value || '';
            const contactoApellido = document.getElementById('apellido_0')?.value || '';
            const contactoSelect = document.getElementById('contactos_cliete');
            const contactoNombreCompleto = contactoSelect.options[contactoSelect.selectedIndex].text.trim();
            const direcconSelect = document.getElementById('direcciones_despacho');
            const direccionCompleta = direcconSelect.options[direcconSelect.selectedIndex].text.trim();



            const telefonoSN = document.getElementById('telefonoSN')?.value || 'No disponible';
            const emailSN = document.getElementById('emailSN')?.value || 'No disponible';

            // Captura los datos de la cotización
            const fechaActual = new Date().toISOString().replace('T', ' ').split('.')[0];
            const docDueDate = document.getElementById('docDueDate')?.textContent || 'No disponible';
            const vendedorData = document.getElementById('vendedor_data')?.textContent || 'No disponible';
            const emailVendedor = 'email@vendedor'; // Texto plano
            const telefonoVendedor = '(+56) 2 2385 3700'; // Texto plano
            const showroomCode = document.getElementById('sucursal')?.textContent || 'No especificado';
            const numeroCotizacion = document.getElementById('numero_cotizacion')?.textContent || 'No disponible';

            // Lógica para las direcciones de showroom
            let showroomDireccion;
            if (showroomCode === 'LC') {
                showroomDireccion = 'Av. Las Condes 7363, Las Condes, Santiago';
            } else if (showroomCode === 'PH') {
                showroomDireccion = 'Av. Padre Hurtado Nte 1199, 7640280 Vitacura, Región Metropolitana';
            } else if (showroomCode === 'GR') {
                showroomDireccion = 'Av. Pdte. Eduardo Frei Montalva #550, Av. Pdte. Eduardo Frei Montalva 520, 8640000 Renca, Región Metropolitana';
            } else if (showroomCode === 'PR') {
                showroomDireccion = 'PR -- No especificado';
            } else {
                showroomDireccion = 'Showroom no especificado';
            }

            const observaciones = document.getElementById('Observaciones')?.value || 'Sin observaciones';

            // Log de toda la información capturada
            console.log({
                rutSN,
                nombreSN,
                apellidoSN,
                grupoSN,
                direccion,
                contactoNombre,
                contactoApellido,
                telefonoSN,
                emailSN,
                fechaActual,
                docDueDate,
                vendedorData,
                emailVendedor,
                telefonoVendedor,
                showroomCode,
                showroomDireccion,
                observaciones,
                numeroCotizacion,
            });

            // Función para agregar encabezado
            const agregarEncabezado = (pdf) => {
                const pageWidth = pdf.internal.pageSize.getWidth();
                const headerHeight = 20;

                // Fondo azul del encabezado
                pdf.setFillColor(0, 0, 255);
                pdf.rect(0, 0, pageWidth, headerHeight, 'F');

                // Imagen del encabezado
                const imgWidth = pageWidth * 0.6;
                const imgHeight = headerHeight - 4;
                const imgData = 'data:image/png;base64,...'; // Sustituye con el Base64 de tu imagen
                //pdf.addImage(imgData, 'PNG', 2, 2, imgWidth, imgHeight);

                // Texto "Cotización N°"
                pdf.setFontSize(14);
                pdf.setTextColor(255, 255, 255); // Blanco
                pdf.text(`Cotización N° ${numeroCotizacion}`, imgWidth + 10, 13);
            };

            // Configurar contenido del PDF
            const midX = pdf.internal.pageSize.getWidth() / 2; // Punto medio de la página
            let yPosition = 30; // Ajusta el contenido para evitar el encabezado

            // Agregar encabezado
            agregarEncabezado(pdf);

            // Títulos
            pdf.setTextColor(0, 0, 255); // Azul
            pdf.setFontSize(14);
            pdf.text('Datos del Cliente', 10, yPosition); // Primera mitad
            pdf.text('Detalles de la Cotización', midX + 10, yPosition); // Segunda mitad
            yPosition += 10;

            pdf.setTextColor(0, 0, 0); // Negro
            pdf.setFontSize(10);

            // Datos del Cliente
            pdf.text(`${rutSN}`, 10, yPosition);
            pdf.text(`${nombreSN} ${apellidoSN}`, 10, yPosition + 6);
            pdf.text(`${grupoSN}`, 10, yPosition + 12);
            //pdf.text(`${direccion}`, 10, yPosition + 18);
            pdf.text(`${direccionCompleta}`, 10, yPosition + 18);
            pdf.text(`Contacto: ${contactoNombreCompleto}`, 10, yPosition + 24);
            //pdf.text(`Contacto: ${contactoNombre} ${contactoApellido}`, 10, yPosition + 24);    
            pdf.text(`Teléfono: ${telefonoSN}`, 10, yPosition + 30);
            pdf.text(`Email: ${emailSN}`, 10, yPosition + 36);

            // Detalles de la Cotización
            pdf.text(`Fecha: ${fechaActual}`, midX + 10, yPosition);
            pdf.text(`Válido Hasta: ${docDueDate}`, midX + 10, yPosition + 6);
            pdf.text(`Vendedor: ${vendedorData}`, midX + 10, yPosition + 12);
            pdf.text(`Email: ${emailVendedor} / Teléfono: ${telefonoVendedor}`, midX + 10, yPosition + 18);
            pdf.text(`Showroom: ${showroomDireccion}`, midX + 10, yPosition + 24);
            pdf.text(`Observaciones: ${observaciones}`, midX + 10, yPosition + 30);


            const agregarPieDePagina = (pdf, pageNumber, totalPages) => {
                const pageWidth = pdf.internal.pageSize.getWidth();
                const pageHeight = pdf.internal.pageSize.getHeight();
                const footerHeight = 20;
                const columnWidth = pageWidth / 4;

                // Fondo gris para el pie de página
                pdf.setFillColor(200, 200, 200); // Gris
                pdf.rect(0, pageHeight - footerHeight, pageWidth, footerHeight, 'F');

                // Estilo de texto
                pdf.setFontSize(8);
                pdf.setTextColor(0, 0, 0); // Negro

                // Primera columna
                pdf.text('Showroom Las Condes', 5, pageHeight - 16);
                pdf.text('Av. Las Condes 7363', 5, pageHeight - 12);
                pdf.text('Lunes a viernes: 9:30 a 19:00 Hrs.', 5, pageHeight - 8);
                pdf.text('Sábados: 10:00 a 14:00 Hrs.', 5, pageHeight - 4);
                pdf.text('+56 2 2385 3700', 5, pageHeight);

                // Segunda columna
                pdf.text('Showroom Vitacura', columnWidth + 5, pageHeight - 16);
                pdf.text('Av. Padre Hurtado Norte 1199', columnWidth + 5, pageHeight - 12);
                pdf.text('Lunes a viernes: 9:30 a 19:00 Hrs.', columnWidth + 5, pageHeight - 8);
                pdf.text('Sábados: 10:00 a 14:00 Hrs.', columnWidth + 5, pageHeight - 4);
                pdf.text('+56 2 2385 3600', columnWidth + 5, pageHeight);

                // Tercera columna
                pdf.text('Showroom / Centro logístico Patio Panal', columnWidth * 2 + 5, pageHeight - 16);
                pdf.text('Av. Pdte Eduardo Frei Montalva 550, Mod 2,', columnWidth * 2 + 5, pageHeight - 12);
                pdf.text('Renca', columnWidth * 2 + 5, pageHeight - 8);
                pdf.text('Lunes a viernes: 8:30 a 18:00 Hrs.', columnWidth * 2 + 5, pageHeight - 4);
                pdf.text('+56 2 2385 3500', columnWidth * 2 + 5, pageHeight);

                // Cuarta columna (numeración de páginas)
                pdf.text(`Página | ${pageNumber} de ${totalPages}`, columnWidth * 3 + 5, pageHeight - 8);
            };

            // Añadir tabla de totales
            const agregarTablaTotales = () => {
                const totalNeto = document.getElementById('total_neto')?.textContent || '$0';
                const iva = document.getElementById('iva')?.textContent || '$0';
                const totalBruto = document.getElementById('total_bruto')?.textContent || '$0';

                const startY = yPosition + 50; // Espacio adicional debajo de los detalles

                pdf.setFontSize(10);
                pdf.text('Subtotal Neto:', 10, startY);
                pdf.text(totalNeto, 80, startY);

                pdf.text('IVA 19%:', 10, startY + 10);
                pdf.text(iva, 80, startY + 10);

                pdf.text('Total a Pagar:', 10, startY + 20);
                pdf.text(totalBruto, 80, startY + 20);
            };
            agregarTablaTotales();

            // Configurar contenido del PDF
            const totalPages = 2; // Cambiar dinámicamente según el contenido
            for (let pageNumber = 1; pageNumber <= totalPages; pageNumber++) {
                if (pageNumber > 1) {
                    pdf.addPage();
                }

                // Agregar encabezado (si aplica) y contenido aquí

                // Agregar pie de página
                agregarPieDePagina(pdf, pageNumber, totalPages);
            }


            // Guardar el PDF
            pdf.save('Cotizacion.pdf');
        });
    }
});
