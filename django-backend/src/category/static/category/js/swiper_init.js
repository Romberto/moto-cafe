window.addEventListener('load', function(){

    const swiper = new Swiper('.swiper', {
    // Optional parameters
    speed: 1200,
    loop: true,
    effect: "cube",
      grabCursor: true,
      cubeEffect: {
        shadow: true,
        slideShadows: true,
        shadowOffset: 20,
        shadowScale: 0.94,
      },
      autoplay: {
        delay: 3000,
      },
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },


     navigation: {
       nextEl: '.swiper-button-next',
       prevEl: '.swiper-button-prev',
     },

    // And if we need scrollbar
    scrollbar: {
      el: '.swiper-scrollbar',
    },
  });
})