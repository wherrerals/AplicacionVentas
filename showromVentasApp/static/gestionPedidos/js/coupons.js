//const { act } = require("react");

document.addEventListener('DOMContentLoaded', () => {
    // Function to apply the coupon
    const couponInput = document.getElementById('coupon_code');
    console.log('Coupon input element:', couponInput);
    if (couponInput) {
        couponInput.addEventListener('input', function() {
            aplicarCupon(this.value.trim());
            console.log('Coupon input changed:', this.value);
        });
    }
});


function aplicarCupon(codigoCupon) {
    if (!codigoCupon) {
        console.log('No coupon code provided.');
        return;
    }

    const filasProductos = document.querySelectorAll('tbody.product-row');
    const productos  = Array.from(filasProductos).map(row => {
        return {
            itemCode: row.getAttribute('data-itemcode'),
            id: row.getAttribute('data-id'),
        };

        // validar los datos del cupon
    });

    fetch('/consult_coupon/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Assuming you have a function to get CSRF token
        },
        body: JSON.stringify({
            code: codigo,
            product_codes: productos
    })

    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            actualizarDescuentosDesdeCupon(data.reglas);
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

        const regla = reglas.find(r => r.itemcode === itemcode || r.operador === 'todo');

        if (regla) {
            // Obtener los valores de descuento
            const maxBase = parseFloat(row.querySelector('#descuento')?.textContent.replace('Max: ', '') || '0');
            const descuentoCupon = parseFloat(regla.descuento_cupon) || 0;
            const nuevoMax = maxBase + descuentoCupon;

            // Actualizar visualmente
            const elemDescuento = row.querySelector('#descuento');
            if (elemDescuento) {
                elemDescuento.textContent = `Max: ${nuevoMax}%`;
                elemDescuento.hidden = false;
            }

            const inputDescuento = row.querySelector('#agg_descuento');
            if (inputDescuento) {
                inputDescuento.max = nuevoMax;
                if (parseFloat(inputDescuento.value) > nuevoMax) {
                    inputDescuento.value = nuevoMax;
                }
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