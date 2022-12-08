// Start Credited code
$(document).ready(function () {
    var movementStrength = 50;
    var height = movementStrength / $(window).height();
    var width = movementStrength / $(window).width();
    $('.overlay').mousemove(function (e) {
        var pageX = e.pageX - ($(window).width() / 2);
        var pageY = e.pageY - ($(window).height() / 2);
        var newvalueX = width * pageX * -1 - 50;
        var newvalueY = height * pageY * -1 - 75;
        $('.background-img').css('background-position', newvalueX + 'px' + ' ' + newvalueY + 'px');
    });
});
// End Credited code