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
    const applyButton = document.getElementById('btn-aplicar-cupon');

    if (couponInput) {
        // Detectar ENTER
        couponInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const codigoCupon = this.value.trim();
                if (codigoCupon !== '') {
                    aplicarCupon(codigoCupon);
                } 
            }
        });

        // Detectar cuando se borra el input
        couponInput.addEventListener('input', function () {
            if (this.value.trim() === '') {
                console.log('Cupón borrado, restaurando estado original...');
                restaurarEstadoCupon();
            }
        });
    }

    if (applyButton) {
        applyButton.addEventListener('click', function () {
            const codigoCupon = couponInput.value.trim();
            if (codigoCupon !== '') {
                aplicarCupon(codigoCupon);
            } 
        });
    }
});



// ---- FUNCIÓN INVERSA: restaurar estado SOLO en productos con cupón válido ----
function restaurarEstadoCupon() {
    const filasProductos = document.querySelectorAll('tbody.product-row');

    filasProductos.forEach(row => {
        const descuento = row.querySelector('#desc_cupon');

        if (descuento && !descuento.hidden) {
            // Extraer solo el número del texto, por ejemplo "Cupon: 100%" -> 100
            const porcentaje = parseInt(descuento.textContent.replace(/\D/g, ''), 10);

            // Solo actuar si el porcentaje es mayor a 0
            if (porcentaje > 0) {
                const inputDescuento = row.querySelector('#agg_descuento');

                if (inputDescuento) {
                    inputDescuento.removeAttribute('disabled');
                    inputDescuento.value = 0;
                    inputDescuento.max = 100; // valor estándar
                    inputDescuento.dispatchEvent(new Event('input', { bubbles: true }));
                }

                // Restaurar la etiqueta de cupón a su estado inactivo
                descuento.hidden = true;
                descuento.textContent = "Cupon: 0%";
                descuento.dataset.value = '';
                inputDescuento.dispatchEvent(new Event('input', { bubbles: true }));

                if (inputDescuento) {
                    inputDescuento.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
        }
    });

    console.log("Se restauraron solo los productos afectados por cupón.");
}




function aplicarCupon(codigoCupon) {
    showLoadingOverlay()
    if (!codigoCupon) {
        console.log('No coupon code provided.');
        hideLoadingOverlay();
        return;
    }
    const inputCliente = document.querySelector('#inputCliente');
    const cardCode = inputCliente.getAttribute('data-codigosn');
    const docTotal = document.getElementById("total_bruto").getAttribute("data-total-bruto");

    if(!cardCode) {
        //console.log('No card code found for the customer.');
        alert('Porfavor agrega un cliente primero.');
        hideLoadingOverlay();
        return;
        
    }
    const filasProductos = document.querySelectorAll('tbody.product-row');
    if (filasProductos.length === 0) {
        console.log('No products found in the order.');
        alert('No hay productos en el pedido.');
        hideLoadingOverlay();
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
        hideLoadingOverlay();
        alert(data.error);
    } else if (data.success) {
        
        actualizarDescuentosDesdeCupon(data);
        hideLoadingOverlay();

    } else {
        hideLoadingOverlay();
        alert('Ocurrió un error desconocido al aplicar el cupón.');
        
    }
})
.catch(error => {
    console.error('Error applying coupon:', error);
    hideLoadingOverlay();
    alert('Ocurrió un error al aplicar el cupón.');
});

}


function actualizarDescuentosDesdeCupon(reglas) {
    const filasProductos = document.querySelectorAll('tbody.product-row');

    // Creamos un mapa {codigo: descuento} para acceso rápido
    const descuentosPorProducto = {};
    if (reglas.products && Array.isArray(reglas.products)) {
        reglas.products.forEach(p => {
            const porcentaje = parseFloat(p.descuento) * 100;
            descuentosPorProducto[p.codigo] = parseFloat(porcentaje.toFixed(2));
        });
    }

    filasProductos.forEach(row => {
        const itemcode = row.getAttribute('data-itemcode');
        const descuentoCupon = descuentosPorProducto[itemcode] || null;

        if (descuentoCupon !== null) {
            console.log('Aplicando descuento para item:', itemcode, 'Descuento:', descuentoCupon);

            const inputDescuento = row.querySelector('#agg_descuento');
            if (inputDescuento) {
                inputDescuento.max = descuentoCupon;
                inputDescuento.value = 0;
                inputDescuento.setAttribute('disabled', 'disabled');

                const descuento = row.querySelector('#desc_cupon');
                if (descuento) {
                    descuento.textContent = `Cupón: ${descuentoCupon}%`;
                    descuento.hidden = false;
                    descuento.dataset.value = descuentoCupon;
                }

                inputDescuento.dispatchEvent(new Event('input', { bubbles: true }));
            }
        } else {
            // Si el producto no tiene descuento de cupón, limpiamos
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