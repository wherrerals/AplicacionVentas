$(document).ready(function () {
    // Variable para almacenar direcciones
    let direccionesAlmacenadas = [];

    // Función común para capturar direcciones - modificada para usar contenedor específico
    function capturarDirecciones(contenedor) {
        const direcciones = [];
        
        console.log("contenedor", contenedor);
        
        // Utilizar el contenedor específico para limitar el alcance de los selectores
        $(`${contenedor} .col-sm-5`).each(function () {
            // Buscar tanto inputs normales como estáticos
            let nombreDireccion = $(this).find('input[name="nombre_direccion[]"]').val() || 
                                  $(this).find('input[name="direccion_static[]"]').val();
            
            let pais = $(this).find('select[name="pais[]"]').val() || 
                       $(this).find('input[name="pais_static[]"]').val() ||
                       $(this).find('select[name="pais_static[]"]').val();
            
            let region = $(this).find('select[name="region[]"]').val() || 
                         $(this).find('input[name="region_static[]"]').val() ||
                         $(this).find('select[name="region_static[]"]').val();
            
            let ciudad = $(this).find('input[name="ciudad[]"]').val() || 
                         $(this).find('input[name="cuidad_static[]"]').val();
            
            let comuna = $(this).find('select[name="comuna[]"]').val() || 
                         $(this).find('input[name="comuna_static[]"]').val() ||
                         $(this).find('select[name="comuna_static[]"]').val();
            
            let direccion = $(this).find('input[name="direccion[]"]').val() || 
                            $(this).find('input[name="nombreDireccion_static[]"]').val();
            
            let direccionId = $(this).find('input[name="direccionid[]"]').val();
            
            // Capturamos el tipo de dirección (incluimos todos los posibles nombres) 
            let tipoDireccion = null;
    
            // Verificamos si existe alguno de los posibles elementos y obtenemos su valor
            let selectTipoDireccion = $(this).find('select[name="tipodireccion[]"]');
            let selectTipoDireccionStatic = $(this).find('select[name="tipoDireccion_static[]"]');
            let inputTipoDireccionStatic = $(this).find('input[name="tipoDireccion_static[]"]');
            let inputTipoDireccion = $(this).find('input[name="tipodireccion_static[]"]');
    
            if (selectTipoDireccion.length) {
                tipoDireccion = selectTipoDireccion.val();
            } else if (selectTipoDireccionStatic.length) {
                tipoDireccion = selectTipoDireccionStatic.val();
            } else if (inputTipoDireccionStatic.length) {
                let staticValue = inputTipoDireccionStatic.val();
                if (staticValue === 'Despacho') {
                    tipoDireccion = 12;
                } else if (staticValue === 'Facturación') {
                    tipoDireccion = 13;
                } else {
                    tipoDireccion = staticValue; // Por si ya viene como valor numérico
                }
            } else if (inputTipoDireccion.length) {
                let staticValue = inputTipoDireccion.val();
                if (staticValue === 'Despacho') {
                    tipoDireccion = 12;
                } else if (staticValue === 'Facturación') {
                    tipoDireccion = 13;
                } else {
                    tipoDireccion = staticValue; // Por si ya viene como valor numérico
                }
            }
    
            // Agregar depuración para todos los campos posibles
            console.log('Valores de campos encontrados:', {
                nombreDireccion: {
                    normal: $(this).find('input[name="nombre_direccion[]"]').val(),
                    static: $(this).find('input[name="nombre_direccion_static[]"]').val()
                },
                pais: {
                    normal: $(this).find('select[name="pais[]"]').val(),
                    static_input: $(this).find('input[name="pais_static[]"]').val(),
                    static_select: $(this).find('select[name="pais_static[]"]').val()
                },
                region: {
                    normal: $(this).find('select[name="region[]"]').val(),
                    static_input: $(this).find('input[name="region_static[]"]').val(),
                    static_select: $(this).find('select[name="region_static[]"]').val()
                },
                ciudad: {
                    normal: $(this).find('input[name="ciudad[]"]').val(),
                    static: $(this).find('input[name="ciudad_static[]"]').val()
                },
                comuna: {
                    normal: $(this).find('select[name="comuna[]"]').val(),
                    static_input: $(this).find('input[name="comuna_static[]"]').val(),
                    static_select: $(this).find('select[name="comuna_static[]"]').val()
                },
                direccion: {
                    normal: $(this).find('input[name="direccion[]"]').val(),
                    static: $(this).find('input[name="direccion_static[]"]').val()
                },
                tipoDireccion: {
                    select_normal: selectTipoDireccion.length ? selectTipoDireccion.val() : 'no encontrado',
                    select_static: selectTipoDireccionStatic.length ? selectTipoDireccionStatic.val() : 'no encontrado',
                    input_static_1: inputTipoDireccionStatic.length ? inputTipoDireccionStatic.val() : 'no encontrado',
                    input_static_2: inputTipoDireccion.length ? inputTipoDireccion.val() : 'no encontrado'
                }
            });
    
            // Validación y depuración de los campos obligatorios
            if (tipoDireccion === null || !nombreDireccion || !pais || !region || !ciudad || !comuna || !direccion) {
                console.log('Campos incompletos en dirección:', {
                    contenedor,
                    tipoDireccion,
                    nombreDireccion,
                    pais,
                    region,
                    ciudad,
                    comuna,
                    direccion
                });
            }
    
            // Validar campos obligatorios
            if (tipoDireccion !== null && nombreDireccion && pais && region && ciudad && comuna && direccion) {
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
                
                // Actualizar los selectores correspondientes
                if (contenedor === '#listaDireccionDespacho') {
                    // Para el caso de elementos estáticos, tratamos de obtener el texto de la comuna de otra manera
                    let comunaNombre = $(this).find('select[name="comuna[]"] option:selected').text() || 
                                      $(this).find('select[name="comuna_static[]"] option:selected').text() ||
                                      $(this).find('input[name="comuna_static[]"]').val();
                    
                    let nuevoTexto = `${nombreDireccion} - ${ciudad} ${comunaNombre}`;
                    actualizarSelector('#direcciones_despacho', nuevoTexto);
                }
                else if (contenedor === '#listaDireccionFacturacion') {
                    // Para el caso de elementos estáticos, tratamos de obtener el texto de la comuna de otra manera
                    let comunaNombre = $(this).find('select[name="comuna[]"] option:selected').text() || 
                                      $(this).find('select[name="comuna_static[]"] option:selected').text() ||
                                      $(this).find('input[name="comuna_static[]"]').val();
                    
                    let nuevoTexto = `${nombreDireccion} - ${ciudad} ${comunaNombre}`;
                    actualizarSelector('#direcciones_facturacion', nuevoTexto);
                }
            } else {
                console.log('Dirección ignorada porque no tiene todos los campos completos.');
            }
        });
    
        console.log(`Direcciones capturadas en ${contenedor}:`, direcciones);
        return direcciones;
    }

    // Función para actualizar un selector
    function actualizarSelector(selectorId, nuevoTexto) {
        let opcionExistente = $(`${selectorId} option[value="${nuevoTexto}"]`);

        if (opcionExistente.length > 0) {
            $(selectorId).val(nuevoTexto);
            console.log(`Opción seleccionada: ${nuevoTexto}`);
        } else {
            $(selectorId).append(
                `<option value="${nuevoTexto}">${nuevoTexto}</option>`
            ).val(nuevoTexto);
            console.log(`Nueva opción agregada y seleccionada: ${nuevoTexto}`);
        }
    }

    // Función común para manejar el guardado de direcciones
    function manejarGuardadoDirecciones(contenedor, tipoDescripcion) {
        // Capturar todas las direcciones en un array
        let direcciones = capturarDirecciones(contenedor);

        // Mostrar en consola el array completo de direcciones
        console.log(`Direcciones de ${tipoDescripcion} capturadas:`, direcciones);

        // Validar que al menos una dirección tenga datos completos
        if (direcciones.length === 0) {
            alert('Debes agregar al menos una dirección.');
            return;
        }

        // Actualizar la variable global de direcciones
        direccionesAlmacenadas = [...direccionesAlmacenadas, ...direcciones];
        
        // Enviar las direcciones al backend mediante AJAX
        enviarDirecciones(direcciones);
    }

    // Asignar evento para el modal de despacho
    $('#btn-grabar-direcciones-despacho').on('click', function (e) {
        manejarGuardadoDirecciones('#listaDireccionDespacho', 'despacho');
    });

    // Asignar evento para el modal de facturación
    $('#btn-grabar-direcciones-facturacion').on('click', function (e) {
        manejarGuardadoDirecciones('#listaDireccionFacturacion', 'facturación');
    });

    // Manejar eventos de cambio en selectores de tipo de dirección
    $(document).on('change', 'select[name="tipodireccion[]"]', function() {
        const nuevoTipoDireccion = $(this).val();
        console.log('Tipo de dirección actualizado:', nuevoTipoDireccion);

        // Solo si tenemos acceso a cliente.direcciones
        if (typeof cliente !== 'undefined' && cliente.direcciones) {
            // Ejecutar la actualización de direcciones
            actualizarDirecciones(cliente.direcciones, '#direcciones_despacho', "12");
            actualizarDirecciones(cliente.direcciones, '#direcciones_facturacion', "13");
        }
    });

    function enviarDirecciones(direcciones) {
        // Asegurar que estamos obteniendo el RUT correcto
        let clienteRut = $('#inputCliente').data('rut');
        console.log('Cliente RUT capturado:', clienteRut);

        const rutCliente = document.getElementById("inputCliente").getAttribute("data-codigoSN");

        // URL para guardar direcciones
        let urlguardarDir = `/ventas/guardar_direcciones/${rutCliente}/`;

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

                    // Cerrar el modal activo pero sin afectar al DOM completo
                    $('.modal.show').modal('hide');
                    
                    // Esperar a que termine la animación del cierre del modal
                    setTimeout(function() {
                        // Obtener el RUT del cliente para buscar la información 
                        const rutInput = document.getElementById('rutSN') || document.getElementById('inputCliente');
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
                    }, 500); // Esperar 500ms para que termine la animación
                } else {
                    mostrarMensaje(response.message || 'Error al guardar las direcciones.', 'error');
                }
            },
            error: function (xhr, status, error) {
                console.error('Error al guardar direcciones:', error);
                console.log('Detalles de la respuesta:', xhr.responseText);

                // Ocultar el overlay de carga y mostrar mensaje de error
                hideLoadingOverlay();
                mostrarMensaje('Ha ocurrido un error al guardar las direcciones.', 'error');
            }
        });
    }
    
    // Exponer la variable direccionesAlmacenadas al scope global
    window.direccionesAlmacenadas = direccionesAlmacenadas;
});

// Manejador de eventos para cuando se elimina una dirección
document.addEventListener('direccionEliminada', function (event) {
    const direccionId = event.detail.direccionId;
    console.log('Dirección eliminada:', direccionId);

    // Verificar que direccionesAlmacenadas exista en el scope global
    if (typeof window.direccionesAlmacenadas !== 'undefined') {
        // Buscar el índice de la dirección a eliminar
        const index = window.direccionesAlmacenadas.findIndex(dir => dir.direccionId === direccionId);
        console.log('Índice encontrado:', index);

        if (index > -1) {
            window.direccionesAlmacenadas.splice(index, 1);
        }

        // Imprimir el estado actual del array de direcciones después de la eliminación
        console.log('Estado actual del array de direcciones:', window.direccionesAlmacenadas);
    } else {
        console.error('La variable direccionesAlmacenadas no está disponible en el scope global');
    }
});