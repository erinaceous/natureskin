$("a.button").click(function() {
    $($(this).attr('href')).toggleClass("active");
    return false;
});
