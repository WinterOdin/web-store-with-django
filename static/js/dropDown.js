(function($) {
console.log("xdddddddddddddddd")
    $('.clickFaq').click(function() {
    $('.displayFaq').toggle('1000');
    $("i", this).toggleClass("icon-up-circled icon-down-circled ");
});


$(".open").hide();
$('.faqQuestion ').click(function(){
    $(this).next().slideToggle();
});

$('.clickFaq').click(function(){
    $('.number').addClass('.numberColor');
});



})(jQuery);
