// loader con "cargando cotizaciones"
const showLoader = () => {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'block';
    }
};

const hideLoader = () => {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
    }
};

//Loaer pagina gris con cargador al medio
const showLoadingOverlay = () => {
    document.getElementById('loadingOverlay').style.display = 'flex';
};

// Ocultar el overlay de carga (si necesitas ocultarlo en algún momento)
const hideLoadingOverlay = () => {
    document.getElementById('loadingOverlay').style.display = 'none';
};