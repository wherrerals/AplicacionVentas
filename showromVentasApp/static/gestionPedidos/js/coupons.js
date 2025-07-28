// ---- CSRF helper ----
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    const couponInput = document.getElementById('cupon_data');
    console.log('Coupon input element:', couponInput);

    if (couponInput) {
        couponInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Evita el envío del formulario
                const codigoCupon = this.value.trim();
                if (codigoCupon !== '') {
                    console.log('Enter pressed, applying coupon:', codigoCupon);
                    aplicarCupon(codigoCupon);
                } else {
                    console.log('Input is empty, no coupon applied');
                }
            }
        });
    }
});


function aplicarCupon(codigoCupon) {
    if (!codigoCupon) {
        console.log('No coupon code provided.');
        return;
    }
    const inputCliente = document.querySelector('#inputCliente');
    const cardCode = inputCliente.getAttribute('data-codigosn');
    if(!cardCode) {
        //console.log('No card code found for the customer.');
        alert('Porfavor agrega un cliente primero.');
        return;
    }
    const filasProductos = document.querySelectorAll('tbody.product-row');
    if (filasProductos.length === 0) {
        console.log('No products found in the order.');
        alert('No hay productos en el pedido.');
        return;
    }
    
    const productos = Array.from(filasProductos).map(row => {
        return {
            itemCode: row.getAttribute('data-itemcode'),
            id: row.getAttribute('data-id'),
        };

        // validar los datos del cupon
    });

    fetch('/ventas/validar_cupon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            //'X-CSRFToken': csrftoken

        },

        body: JSON.stringify({
            card_code: cardCode,
            code: codigoCupon,
            product_codes: productos
        })

    })
        .then(response => response.json())
        .then(data => {
            console.log('Coupon response:', data);
            if (data.success) {
                actualizarDescuentosDesdeCupon(data);
            } else {
                console.log('Invalid coupon code.');
                alert('Invalid coupon code.');
            }
        })
        .catch(error => {
            console.error('Error applying coupon:', error);
            alert('An error occurred while applying the coupon.');
        });
}


function actualizarDescuentosDesdeCupon(reglas) {
    const filasProductos = document.querySelectorAll('tbody.product-row');

    filasProductos.forEach(row => {
        const itemcode = row.getAttribute('data-itemcode');
        const rules = reglas.discount * 100;

        if (rules) {
            console.log('Applying discount for item:', itemcode, 'Discount:', rules);

            const inputDescuento = row.querySelector('#agg_descuento');
            const descuentoCupon = parseFloat(rules) || 0;

            if (inputDescuento) {
                // Establecer el nuevo valor máximo y reiniciar valor visible
                inputDescuento.max = descuentoCupon;
                inputDescuento.value = 0; // o podrías poner descuentoCupon si quieres mostrar el % directo
                inputDescuento.setAttribute('disabled', 'disabled');

                // Mostrar info de cupón
                const descuento = row.querySelector('#desc_cupon');
                if (descuento) {
                    descuento.textContent = `Cupon: ${descuentoCupon}%`;
                    descuento.hidden = false;
                    descuento.dataset.value = descuentoCupon;
                }

                // 🔁 Lanzar evento manual para recalcular
                inputDescuento.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    });
}



/* class coupons {
    constructor(code, discount, valid) {
        this.code = code;
        this.discount = discount || 0;
        this.valid = valid || false;
        // listado de codigos_productos para validar en el servidor
        this.product_codes = [];
    }

    consult_coupon() {
        let url = 'consult_coupon/';
        let data = {
            'code': this.code,
            'product_codes': this.product_codes
        };

        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(data),
            contentType: 'application/json',
            dataType: 'json',
            success: (response) => {
                if (response.valid) {
                    this.discount = response.discount;
                    this.valid = true;
                    alert(`Coupon applied! Discount: ${this.discount}%`);
                } else {
                    this.valid = false;
                    alert('Invalid coupon code.');
                }
            },
            error: (xhr, status, error) => {
                console.error('Error consulting coupon:', error);
                alert('An error occurred while consulting the coupon.');
            }
        });
    }
} */