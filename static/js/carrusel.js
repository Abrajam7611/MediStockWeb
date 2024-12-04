document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".carousel img"); // Todas las imágenes
    const indicators = document.querySelectorAll(".carousel-indicators .indicator"); // Indicadores del carrusel
    let current = 0; // Índice actual

    function showNextImage() {
        // Quitar la clase 'active' de la imagen e indicador actuales
        images[current].classList.remove("active");
        indicators[current].classList.remove("active");

        // Mover al siguiente índice (volver al principio si es la última imagen)
        current = (current + 1) % images.length; // Esto asegura el bucle infinito

        // Agregar la clase 'active' a la nueva imagen e indicador
        images[current].classList.add("active");
        indicators[current].classList.add("active");
    }

    // Ejecutar la función cada 5 segundos
    setInterval(showNextImage, 7000);
});
