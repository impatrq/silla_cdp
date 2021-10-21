const carouselImages = document.querySelector('.carousel__images');
const carouselButtons = document.querySelectorAll('.carousel__button');
const imagesNumber = document.querySelectorAll('.carousel__images img').length;
let imageIndex = 1;
let translateX = 0;

carouselButtons.forEach(button => {
    button.addEventListener('click', event => {
        if (event.target.id === 'previous') {
            if (imageIndex !== 1) {
                imageIndex--;
                translateX += 600;
            }
        } else {
            if (imageIndex !== imagesNumber) {
                imageIndex++;
                translateX -= 600;
            }
        }

        carouselImages.style.transform = `translateX(${translateX}px)`;
    });
});