// Función para obtener el token CSRF desde las cookies
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

const csrftoken = getCookie('csrftoken');

document.getElementById('orderForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    const orderNumber = document.getElementById('orderNumber').value;
    try {
        const response = await fetch('/ordenes/', { // Asegúrate de que la URL es correcta
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ orderNumber })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        document.getElementById('result').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById('result').innerText = 'Error: ' + error.message;
    }
});
