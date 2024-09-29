// loader.js
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
