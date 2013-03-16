function openPage(button) {
    activeElem = $($(button).attr('href'));
    isActive = $(activeElem).hasClass('active');
    //$('.active').removeClass('active');
    //if(!isActive) {
    //    $(activeElem).addClass('active');
    //}
    $(activeElem).toggleClass('active');
}

$("a.button").click(function() { openPage(this); return false; });
$("a.buttonlike").click(function() { openPage(this); return false; });

$(document).ready(function() {
   setTimeout(function() { $("a.button[href='#menu']:first").click(); }, 2000);
});
