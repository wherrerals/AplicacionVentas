$(document).ready(function () {
    // Asignar evento para el modal de despacho
    $('#btn-grabar-direcciones-despacho').on('click', function (e) {
        e.preventDefault(); // Evitar comportamiento por defecto del botón

        // Capturar todas las direcciones de despacho en un array
        let direcciones = [];

        $('#listaDireccionDespacho .col-sm-5').each(function () {
            let nombreDireccion = $(this).find('input[name="nombre_direccion[]"]').val();
            let pais = $(this).find('select[name="pais[]"]').val();
            let region = $(this).find('select[name="region[]"]').val();
            let ciudad = $(this).find('input[name="ciudad[]"]').val();
            let comuna = $(this).find('select[name="comuna[]"]').val();
            let direccion = $(this).find('input[name="direccion[]"]').val();
            let direccionId = $(this).find('input[name="direccionid[]"]').val();
            let rowNum = $(this).find('input[name="direccionid[]"]').data('rowNum');

            console.log('rowNum:', rowNum);

            // Capturamos el tipo de dirección
            let tipoDireccion = null;

            // Verificamos si es un select o un input y obtenemos el valor
            let selectTipoDireccion = $(this).find('select[name="tipodireccion[]"]');
            let inputTipoDireccionStatic = $(this).find('input[name="tipoDireccion_static[]"]');

            if (selectTipoDireccion.length) {
                // Si es un select, tomamos el valor seleccionado
                tipoDireccion = selectTipoDireccion.find('option:selected').val();

                // Agregamos el evento change para actualizar las direcciones dinámicamente
                selectTipoDireccion.on('change', function () {
                    const nuevoTipoDireccion = $(this).val();
                    console.log('Tipo de dirección actualizado:', nuevoTipoDireccion);

                    // Ejecutar la actualización de direcciones
                    actualizarDirecciones(cliente.direcciones, '#direcciones_despacho', "12");
                    actualizarDirecciones(cliente.direcciones, '#direcciones_facturacion', "13");
                });
            } else if (inputTipoDireccionStatic.length) {
                // Si es un input, tomamos su valor directamente
                let staticValue = inputTipoDireccionStatic.val();
                if (staticValue === 'Despacho') {
                    tipoDireccion = 12;
                } else if (staticValue === 'Facturación') {
                    tipoDireccion = 13;
                }
            }

            // Validar tipo de dirección y otros campos
            if (tipoDireccion === null || !nombreDireccion || !pais || !region || !ciudad || !comuna || !direccion) {
                console.log('Dirección ignorada porque no tiene todos los campos completos.');
                return; // Saltar este elemento si falta algún campo
            }

            console.log(
                'Diccionario modificado:',
                tipoDireccion,
                nombreDireccion,
                pais,
                region,
                ciudad,
                comuna,
                direccion,
                direccionId,
                rowNum
            );

            direcciones.push({
                'tipoDireccion': tipoDireccion,
                'nombreDireccion': nombreDireccion,
                'pais': pais,
                'region': region,
                'ciudad': ciudad,
                'comuna': comuna,
                'direccion': direccion,
                'direccionId': direccionId
            });

            // Obtener el nombre de la comuna seleccionada
            let comunaNombre = $(this).find('select[name="comuna[]"] option:selected').text();
            console.log('Nombre de la comuna seleccionada:', comunaNombre);

            let nuevoTexto = `${nombreDireccion} - ${ciudad} ${comunaNombre}`;
            console.log('nuevoTexto: ', nuevoTexto);

            // Manejar la opción en el selector de direcciones de despacho
            let opcionExistente = $(`#direcciones_despacho option[value="${nuevoTexto}"]`);

            if (opcionExistente.length > 0) {
                $(`#direcciones_despacho`).val(nuevoTexto);
                console.log(`Opción seleccionada: ${nuevoTexto}`);
            } else {
                $(`#direcciones_despacho`).append(
                    `<option value="${nuevoTexto}">${nuevoTexto}</option>`
                ).val(nuevoTexto);
                console.log(`Nueva opción agregada y seleccionada: ${nuevoTexto}`);
            }
        });


        // Mostrar en consola el array completo de direcciones
        console.log('Direcciones de despacho capturadas:', direcciones);

        // Validar que al menos una dirección tenga datos completos
        if (direcciones.length === 0) {
            alert('Debes agregar al menos una dirección.');
            return;
        }

        // Enviar las direcciones al backend mediante AJAX
        enviarDirecciones(direcciones);
    });

    // Asignar evento para el modal de facturación
    $('#btn-grabar-direcciones-facturacion').on('click', function (e) {
        e.preventDefault(); // Evitar comportamiento por defecto del botón

        // Capturar todas las direcciones de facturación en un array
        let direcciones = [];

        // Recorrer cada div que contiene las direcciones de facturación
        $('#listaDireccionFacturacion .col-sm-5').each(function () {
            let tipoDireccion = $(this).find('select[name="tipodireccion[]"]').val();
            let nombreDireccion = $(this).find('input[name="nombre_direccion[]"]').val();
            let pais = $(this).find('select[name="pais[]"]').val();
            let region = $(this).find('select[name="region[]"]').val();
            let ciudad = $(this).find('input[name="ciudad[]"]').val();
            let comuna = $(this).find('select[name="comuna[]"]').val();
            let direccion = $(this).find('input[name="direccion[]"]').val();
            let direccionId = $(this).find('input[name="direccionid[]"]').val();


            // Validar que todos los campos obligatorios tengan valores
            if (tipoDireccion && nombreDireccion && pais && region && ciudad && comuna && direccion) {
                direcciones.push({
                    'tipoDireccion': tipoDireccion,
                    'nombreDireccion': nombreDireccion,
                    'pais': pais,
                    'region': region,
                    'ciudad': ciudad,
                    'comuna': comuna,
                    'direccion': direccion,
                    'direccionId': direccionId
                });
            } else {
                console.log('Dirección ignorada porque no tiene todos los campos completos. BBBBBBBBBBBBBBBBBBBBB');
            }
        });

        // Mostrar en consola el array completo de direcciones
        console.log('Direcciones de facturación capturadas:', direcciones);

        // Validar que al menos una dirección tenga datos completos
        if (direcciones.length === 0) {
            alert('Debes agregar al menos una dirección.');
            return;
        }

        // Enviar las direcciones al backend mediante AJAX
        enviarDirecciones(direcciones);
    });

    function enviarDirecciones(direcciones) {
        let clienteRut = $('#inputCliente').data('rut');
        console.log('Cliente RUT capturado:', clienteRut);

        const rutCliemte = document.getElementById("inputCliente").getAttribute("data-codigoSN");

        // URL para guardar direcciones
        let urlguardarDir = `/ventas/guardar_direcciones/${rutCliemte}/`;

        // Mostrar el overlay de carga
        showLoadingOverlay();

        // Limpiar mensajes previos
        limpiarMensajes();

        $.ajax({
            url: urlguardarDir,
            type: 'POST',
            data: {
                'direcciones': JSON.stringify(direcciones),
                'cliente': clienteRut
            },
            headers: {
                "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
            },
            success: function (response) {
                // Ocultar el overlay de carga
                hideLoadingOverlay();

                // Manejar la respuesta del servidor
                if (response.success) {
                    mostrarMensaje('Direcciones guardadas correctamente.', 'success');

                    // Cerrar el modal si existe
                    const modalDespElement = document.getElementById('dirDespModal');
                    const modalFactElement = document.getElementById('dirFactModal');

                    // Obtener instancias de los modales
                    const modalDespInstance = bootstrap.Modal.getInstance(modalDespElement);
                    const modalFactInstance = bootstrap.Modal.getInstance(modalFactElement);

                    // Cerrar modal de despacho si existe
                    if (modalDespInstance) {
                        modalDespInstance.hide();
                    }

                    // Cerrar modal de facturación si existe
                    if (modalFactInstance) {
                        modalFactInstance.hide();
                    }

                    // Obtener el RUT del cliente para buscar la información 
                    const rutInput = document.getElementById('rutSN') || document.getElementById('inputCliente'); // Ajusta el ID según el HTML
                    const rutCliente = rutInput ? rutInput.value : '';

                    // Actualizar el campo de entrada con el RUT del cliente
                    if (rutCliente) {
                        const inputCliente = document.getElementById('rutSN') || document.getElementById('inputCliente');
                        if (inputCliente) {
                            inputCliente.value = rutCliente;
                        }

                        $('#resultadosClientes').empty(); // Limpiar los resultados de la búsqueda 
                        traerInformacionCliente(rutCliente); // Traer la información del cliente
                    }

                    // Opcional: refrescar la página
                    // location.reload();
                } else {
                    mostrarMensaje(response.message || 'Error al guardar las direcciones.', 'error');
                }
            },
            error: function (xhr, status, error) {
                console.error('Error al guardar direcciones:', error);

                // Ocultar el overlay de carga y mostrar mensaje de error
                hideLoadingOverlay();
                mostrarMensaje('Ha ocurrido un error al guardar las direcciones.', 'error');
            }
        });
    }

});

document.addEventListener('direccionEliminada', function (event) {
    const direccionId = event.detail.direccionId;
    console.log('Producto eliminado:', direccionId);

    // Buscar el índice del producto a eliminar
    const index = direccion.findIndex(producto => producto.direccionId === direccionId);
    console.log('Índice encontrado:', index);

    if (index > -1) {
        direccion.splice(index, 1);
    }

    // Imprimir el estado actual del array productos después de la eliminación
    console.log('Estado actual del array productos:', direccion);

});