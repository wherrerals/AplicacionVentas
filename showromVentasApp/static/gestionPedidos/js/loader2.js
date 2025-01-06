// Seleccionar el loader
const loader = document.getElementById('loader');

// Función para mostrar el loader
const showLoader = () => {
  loader.style.display = 'block';
};

// Función para ocultar el loader
const hideLoader = () => {
  loader.style.display = 'none';
};

// Wrapper para fetch
const fetchWithLoader = async (url, options = {}) => {
  showLoader();
  try {
    const response = await fetch(url, options);
    return await response.json(); // Si la respuesta es JSON
  } catch (error) {
    console.error(error);
    throw error;
  } finally {
    hideLoader();
  }
};
