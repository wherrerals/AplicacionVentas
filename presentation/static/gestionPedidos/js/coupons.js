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
    const docTotal = document.getElementById("total_bruto").getAttribute("data-total-bruto");

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
        'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
        card_code: cardCode,
        code: codigoCupon,
        product_codes: productos,
        doc_total: docTotal
    })
})
.then(response => response.json())
.then(data => {
    console.log('Coupon response:', data);

    if (data.error) {
        // Muestra todos los errores devueltos por el backend
        alert(data.error);
    } else if (data.success) {
        actualizarDescuentosDesdeCupon(data);
    } else {
        alert('Ocurrió un error desconocido al aplicar el cupón.');
    }
})
.catch(error => {
    console.error('Error applying coupon:', error);
    alert('Ocurrió un error al aplicar el cupón.');
});

}


function actualizarDescuentosDesdeCupon(reglas) {
    const filasProductos = document.querySelectorAll('tbody.product-row');
    const productosAplicables = reglas.products.map(p => p.codigo); // Extrae los códigos permitidos
    const porcentajeDescuento = parseFloat(reglas.discount) * 100;

    filasProductos.forEach(row => {
        const itemcode = row.getAttribute('data-itemcode');

        // Solo aplica si el item está en la lista de productos del cupón
        if (productosAplicables.includes(itemcode)) {
            console.log('Applying discount for item:', itemcode, 'Discount:', porcentajeDescuento);

            const inputDescuento = row.querySelector('#agg_descuento');
            const descuentoCupon = porcentajeDescuento || 0;

            if (inputDescuento) {
                inputDescuento.max = descuentoCupon;
                inputDescuento.value = 0;
                inputDescuento.setAttribute('disabled', 'disabled');

                const descuento = row.querySelector('#desc_cupon');
                if (descuento) {
                    descuento.textContent = `Cupon: ${descuentoCupon}%`;
                    descuento.hidden = false;
                    descuento.dataset.value = descuentoCupon;
                }

                inputDescuento.dispatchEvent(new Event('input', { bubbles: true }));
            }
        } else {
            // Opción: limpiar descuento si el producto no aplica
            const inputDescuento = row.querySelector('#agg_descuento');
            if (inputDescuento) {
                inputDescuento.removeAttribute('disabled');
            }

            const descuento = row.querySelector('#desc_cupon');
            if (descuento) {
                descuento.hidden = true;
                descuento.textContent = '';
                descuento.dataset.value = '';
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