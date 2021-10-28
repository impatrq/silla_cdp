const carouselImages = document.querySelector('.carousel__images');
const carouselButtons = document.querySelectorAll('.carousel__button');
const imagesNumber = document.querySelectorAll('.carousel__images img').length;
let imageIndex = 1;
let translateX = 0;

carouselButtons.forEach(button => {
    button.addEventListener('click', event => {
        var imageWidth = document.querySelector('.carousel').offsetWidth;
        if (event.target.id === 'previous') {
            if (imageIndex !== 1) {
                imageIndex--;
                translateX += imageWidth;
            }
        } else {
            if (imageIndex !== imagesNumber) {
                imageIndex++;
                translateX -= imageWidth;
            }
        }
        console.log(imageWidth)
        carouselImages.style.transform = `translateX(${translateX}px)`;
    });
});