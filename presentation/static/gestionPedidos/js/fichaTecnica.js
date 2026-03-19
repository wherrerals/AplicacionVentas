async function generarFichaTecnica(sku) {
    if (!sku) {
        console.error("SKU inválido");
        return;
    }

    const url = `/ventas/ficha_tecnica/${encodeURIComponent(sku)}/pdf/`;

    try {
        showLoadingOverlay();

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }

        const blob = await response.blob();

        // Crear URL temporal
        const downloadUrl = window.URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = downloadUrl;
        link.download = `ficha_tecnica_${sku}.pdf`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Liberar memoria
        window.URL.revokeObjectURL(downloadUrl);

    } catch (error) {
        console.error("Error al generar ficha técnica:", error);
        alert("El producto no tiene ficha técnica disponible.");
    } finally {
        // ✔️ AQUÍ debe ir
        hideLoadingOverlay();
    }
}