$(document).ready(function(){
    $('#grabar-btn').click(function(event) {
        event.preventDefault();

        let formData = new FormData($('#formulario-cliente')[0]);

        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            type: 'POST',
            url: $('#formulario-cliente').attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                console.log('Cliente creado:', response);
                console.log('RUT del cliente:', response.rut);
                console.log('nom del cliente:', response.rut);

                let clienteId = response.rut;
                traerInformacionCliente(clienteId);

                let nombre = response.nombre || '';
                let apellido = response.apellido || '';
                $('#inputCliente').val(nombre + ' ' + apellido);

                $('#miModal').modal('hide');
            },
            error: function(xhr, status, error) {
                console.error('Error al crear el cliente:', error);
            }
        });
    });
});
