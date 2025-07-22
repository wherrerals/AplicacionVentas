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
    // Function to apply the coupon
    const couponInput = document.getElementById('cupon_data');
    console.log('Coupon input element:', couponInput);

    if (couponInput) {
        couponInput.addEventListener('input', function () {
            aplicarCupon(this.value.trim());
            console.log('Coupon input changed:', this.value);
        });

        // escuchar el enter 

        couponInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent form submission
                const codigoCupon = this.value.trim();
                console.log('Enter pressed, applying coupon:', codigoCupon);
            }
        });

    }
});

function aplicarCupon(codigoCupon) {
    if (!codigoCupon) {
        console.log('No coupon code provided.');
        return;
    }

    const filasProductos = document.querySelectorAll('tbody.product-row');
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

        //const regla = reglas.find(r => r.itemcode === itemcode || r.operador === 'todo');
        const rules = reglas.discount * 100

        if (rules) {

            console.log('Applying discount for item:', itemcode, 'Discount:', rules);
            // Obtener los valores de descuento
            const maxBase = parseFloat(row.querySelector('#agg_descuento')?.value);
            const descuentoCupon = parseFloat(rules) || 0;
            const nuevoMax = maxBase + descuentoCupon;

            const inputDescuento = row.querySelector('#agg_descuento');
            if (inputDescuento) {
                inputDescuento.max = nuevoMax;
                inputDescuento.value = nuevoMax;
                inputDescuento.dispatchEvent(new Event('input', { bubbles: true }));
                
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