// BOTON PARA SCROLL HACIA ARRIBA
topButton = document.getElementById('btnScrollTop');

window.onscroll = function() {scrollFunction()};

// MANEJAR NAV RESPONSIVE
const hamburger = document.querySelector('.hamburger');
const mobileNav = document.querySelector('.mobile-nav');
const navButtons = document.querySelectorAll('.nav-button');
let menuOpen = false;

hamburger.addEventListener('click', button => {
    hamburger.classList.toggle('is-active');
    mobileNav.classList.toggle('is-active');
    document.body.classList.toggle('disableScroll');

    if (!menuOpen) {
        hamburger.classList.add('open');
        menuOpen = true;
    } else {
        hamburger.classList.remove('open');
        menuOpen = false;
    }
});

navButtons.forEach((button) => {
    button.addEventListener('click', () => {
        document.body.classList.remove('disableScroll');
    })
})

// Funciones
function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        topButton.style.display = 'block';
        hamburger.classList.remove('is-active');
        mobileNav.classList.remove('is-active');
        hamburger.classList.remove('open');
        menuOpen = false;
    } else {
        topButton.style.display = 'none';
    }
}
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}