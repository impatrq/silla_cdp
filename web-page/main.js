
// BOTON PARA SCROLL HACIA ARRIBA
topButton = document.getElementById('btnScrollTop');

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        topButton.style.display = 'block';
    } else {
        topButton.style.display = 'none';
    }
}
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// MANEJAR NAV RESPONSIVE
const hamburger = document.querySelector('.hamburger');
const mobileNav = document.querySelector('.mobile-nav');
let menuOpen = false;

hamburger.addEventListener('click', button => {
    hamburger.classList.toggle('is-active');
    mobileNav.classList.toggle('is-active');

    if (!menuOpen) {
        hamburger.classList.add('open');
        menuOpen = true;
    } else {
        hamburger.classList.remove('open');
        menuOpen = false;
    }
});