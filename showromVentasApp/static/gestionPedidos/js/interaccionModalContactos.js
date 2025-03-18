$(document).ready(function () {
    $('#btn-grabar-cont').on('click', function (e) {
        e.preventDefault(); // Evitar comportamiento por defecto del botón

        console.log("Número de contactos detectados:", $('#listaContactos .col-sm-5').length);

        // Capturar todos los contactos en un array
        let contactos = [];

        // Recorrer cada div que contiene los contactos
        $('#listaContactos .col-sm-5').each(function () {
            // Obtener los valores de los inputs
            let nombre = $(this).find('input[name="nombre[]"]').val();
            let apellido = $(this).find('input[name="apellido[]"]').val();
            let telefono = $(this).find('input[name="telefono[]"]').val();
            let celular = $(this).find('input[name="celular[]"]').val();
            let email = $(this).find('input[name="email[]"]').val();
            let contactoid = $(this).find('input[name="contacto_id[]"]').val();
            let codigoInternoSap = $(this).find('input[name="contacto_id[]"]').data('bpcode');
            console.log('Codigo interno SAP:', codigoInternoSap);

            if (nombre && apellido && telefono && celular && email) {
                contactos.push({
                    'nombre': nombre,
                    'apellido': apellido,
                    'telefono': telefono,
                    'celular': celular,
                    'email': email,
                    'codigoInternoSap': codigoInternoSap,
                    "contacto_id": contactoid,
                });
            } else {
                console.log('Contacto ignorado porque no tiene todos los campos completos.');
            }
        });


        // Mostrar en consola el array completo de contactos
        console.log('Contactos capturados:', contactos);

        // Validar que al menos un contacto tenga datos completos
        if (contactos.length === 0) {
            alert('Debes agregar al menos un contacto.');
            return;
        }

        // Mostrar el cliente que se enviará en la petición
        let clienteRut = $('#inputCliente').data('rut');
        console.log('Cliente RUT capturado:', clienteRut);

        const rutCliemte = document.getElementById("inputCliente").getAttribute("data-codigoSN");


        // Enviar los contactos al backend mediante AJAX

        // Mostrar el overlay de carga
        showLoadingOverlay();

        // Limpiar mensajes previos
        limpiarMensajes();


        let urlguardarCont = `/ventas/guardar_contactos/${rutCliemte}/`;
        $.ajax({
            url: urlguardarCont,  // URL del endpoint en Django
            type: 'POST',
            data: {
                'contactos': JSON.stringify(contactos),
                'cliente': clienteRut  // Asumiendo que el cliente está en un atributo `data-rut`
            },
            headers: {
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()  // Incluir el token CSRF en los headers
            },
            success: function (response) {

                hideLoadingOverlay();


                console.log('Respuesta del servidor:', response);
                if (response.success) {
                    mostrarMensaje('Contactos guardados correctamente.', 'success');
                    $('#contactoModal').modal('hide');

                    const rutInput = document.getElementById('rutSN') || document.getElementById('inputCliente'); // Ajusta el ID según el HTML
                    const rutCliente = rutInput ? rutInput.value : '';

                    // Actualizar el campo de entrada con el RUT del cliente
                    if (rutCliente) {
                        const inputCliente = document.getElementById('rutSN') || document.getElementById('inputCliente');
                        if (inputCliente) {
                            inputCliente.value = rutCliente;
                        }
                        
                        console.log('RUT del cliente XXXXXX:', rutCliente);
                        $('#resultadosClientes').empty(); // Limpiar los resultados de la búsqueda 
                        traerInformacionCliente(rutCliente); // Traer la información del cliente
                    }
                    //location.reload();
                } else {
                    alert('Error al guardar contactos: ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error al guardar los contactos:', error);


                hideLoadingOverlay();
                mostrarMensaje('Ha ocurrido un error al guardar los conctactos.', 'error');
            }
        });
    });
});

$(document).ready(function () {
    // Escuchar cambios en los inputs de nombre y apellido
    $(document).on('input', 'input[name="nombre[]"], input[name="apellido[]"]', function () {
        // Recorrer cada fila de contacto
        $('#listaContactos .col-sm-5').each(function () {
            let nombre = $(this).find('input[name="nombre[]"]').val();
            let apellido = $(this).find('input[name="apellido[]"]').val();
            let contactoid = $(this).find('input[name="contacto_id[]"]').val();

            // Crear texto para mostrar en el selector
            let nuevoTexto = `${nombre} ${apellido}`;

            // Verificar si el selector existe
            if ($('#contactos_cliete').length > 0) {
                console.log('Selector contactos_cliete encontrado.');

                // Buscar si la opción ya existe en el selector
                let opcionExistente = $(`#contactos_cliete option[value="${contactoid}"]`);

                if (opcionExistente.length > 0) {
                    // Si la opción existe, actualiza el texto
                    opcionExistente.text(nuevoTexto);
                    console.log(`Opción actualizada: ${nuevoTexto}`);
                } else if (contactoid) {
                    // Si no existe, agregarla y seleccionarla
                    $(`#contactos_cliete`).append(
                        `<option value="${contactoid} ">${nuevoTexto}</option>`
                    );
                    console.log(`Nueva opción agregada: ${nuevoTexto}`);
                }
            } else {
                console.log('El selector contactos_cliete no existe.');
            }
        });
    });
});


