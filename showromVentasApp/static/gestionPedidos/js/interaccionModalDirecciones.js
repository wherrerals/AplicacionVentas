$(document).ready(function() {
    // Función común para procesar direcciones
    function procesarDirecciones(selector, tipo) {
        let direcciones = [];

        $(selector).each(function() {
            let nombreDireccion = $(this).find('input[name="nombre_direccion[]"]').val();
            let pais = $(this).find('select[name="pais[]"]').val();
            let region = $(this).find('select[name="region[]"]').val();
            let ciudad = $(this).find('input[name="ciudad[]"]').val();
            let comuna = $(this).find('select[name="comuna[]"]').val();
            let direccion = $(this).find('input[name="direccion[]"]').val();
            let direccionId = $(this).find('input[name="direccionid[]"]').val();

            let tipoDireccion = null;
            let selectTipoDireccion = $(this).find('select[name="tipodireccion[]"]');
            let inputTipoDireccionStatic = $(this).find('input[name="tipoDireccion_static[]"]');

            if (selectTipoDireccion.length) {
                tipoDireccion = selectTipoDireccion.find('option:selected').val();
            } else if (inputTipoDireccionStatic.length) {
                let staticValue = inputTipoDireccionStatic.val();
                tipoDireccion = staticValue === 'Despacho' ? 12 : staticValue === 'Facturación' ? 13 : null;
            }

            if (tipoDireccion === null || !nombreDireccion || !pais || !region || !ciudad || !comuna || !direccion) {
                console.log('Dirección ignorada porque no tiene todos los campos completos.');
                return;
            }

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
        });

        console.log(`${tipo} capturadas:`, direcciones);

        if (direcciones.length === 0) {
            alert(`Debes agregar al menos una dirección de ${tipo}.`);
            return;
        }

        return direcciones;
    }

    // Función para enviar las direcciones al backend
    function enviarDirecciones(direcciones, tipo) {
        let clienteRut = $('#inputCliente').data('rut');
        let rutCliemte = $('#inputCliente').data('codigoSN');

        let urlguardarDir = `/ventas/guardar_direcciones/${rutCliemte}/`;
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
            success: function(response) {
                console.log(`Respuesta del servidor para ${tipo}:`, response);
                if (response.success) {
                    alert(`Direcciones de ${tipo} guardadas correctamente.`);
                    $('.modal').modal('hide');
                } else {
                    alert(`Error al guardar direcciones de ${tipo}: ${response.message}`);
                }
            },
            error: function(xhr, status, error) {
                console.error(`Error al guardar direcciones de ${tipo}:`, error);
                alert(`Ha ocurrido un error al guardar las direcciones de ${tipo}.`);
            }
        });
    }

    // Evento para ambos botones
    $('#btn-grabar-direcciones-despacho, #btn-grabar-direcciones-facturacion').on('click', function(e) {
        e.preventDefault();

        // Procesar y enviar direcciones de despacho
        let direccionesDespacho = procesarDirecciones('#listaDireccionDespacho .col-sm-5', 'despacho');
        if (direccionesDespacho) {
            enviarDirecciones(direccionesDespacho, 'despacho');
        }

        // Procesar y enviar direcciones de facturación
        let direccionesFacturacion = procesarDirecciones('#listaDireccionFacturacion .col-sm-5', 'facturación');
        if (direccionesFacturacion) {
            enviarDirecciones(direccionesFacturacion, 'facturación');
        }
    });

    // Asignar evento para el modal de facturación
    $('#btn-grabar-direcciones-facturacion').on('click', function(e) {
        e.preventDefault(); // Evitar comportamiento por defecto del botón

        // Capturar todas las direcciones de facturación en un array
        let direcciones = [];

        // Recorrer cada div que contiene las direcciones de facturación
        $('#listaDireccionFacturacion .col-sm-5').each(function() {
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

    // Función común para enviar las direcciones al backend
    function enviarDirecciones(direcciones) {
        let clienteRut = $('#inputCliente').data('rut');
        console.log('Cliente RUT capturado:', clienteRut);

        const rutCliemte = document.getElementById("inputCliente").getAttribute("data-codigoSN");

        // Enviar las direcciones al backend mediante AJAX
        let urlguardarDir = `/ventas/guardar_direcciones/${rutCliemte}/`;
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
            success: function(response) {
                console.log('Respuesta del servidor:', response);
                if (response.success) {
                    alert('Direcciones guardadas correctamente');
                    $('.modal').modal('hide');  // Ocultar cualquier modal que esté abierto
                    //location.reload();
                } else {
                    alert('Error al guardar direcciones: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error al guardar direcciones:', error);
                alert('Ha ocurrido un error al guardar las direcciones.');
            }
        });
    }
});
