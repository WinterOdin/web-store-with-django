
  let slider = $('.owl-carousel');
  slider.each(function () {
    $(this).owlCarousel({
      nav: true,
      loop:false,
      dots: false,
      pagination: false,
      margin: 25,
      autoHeight: false,
      stagePadding: 50,
      responsive:{
        0:{
          items: 1,
          stagePadding: 0,
          margin: 30,
        },
        767:{
          items: 3,
          stagePadding: 25,
        },
        1000:{
          items: 3,
        }
      }
    });
  });
