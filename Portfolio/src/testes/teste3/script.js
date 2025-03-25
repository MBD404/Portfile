const transitionanimate = [
    { background: "rgba(0, 0, 0, 0)" },
    { background: "rgba(0, 0, 0, 1)" },
];

const transitionTiming = {
    duration: 1200,
    iterations: 1,
}

document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.image');
    const overlay = document.querySelector('.overlay');

    images.forEach(image => {
        image.addEventListener('click', function() {
            // Remove a classe 'active' de todas as imagens
            images.forEach(img => img.classList.remove('active'));

            // Adiciona a classe 'active' apenas à imagem clicada
            this.classList.add('active');

            // Mostra o overlay
            overlay.style.display = 'block';
            overlay.animate(transitionanimate, transitionTiming)
        });
    });

    overlay.addEventListener('click', function() {
        // Esconde o overlay
        this.style.display = 'none';

        // Remove a classe 'active' de todas as imagens
        images.forEach(img => img.classList.remove('active'));
    });
});