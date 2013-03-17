function openPage(elem) {
    activeElem = $(elem);
    isActive = $(activeElem).hasClass('active');
    if(!isActive) {
        $(activeElem).data('zindex', $(activeElem.css('z-index')));
        $(activeElem).css('z-index', 1000);
        $(activeElem).addClass('active');
    } else {
        $(activeElem).removeClass('active');
        $(activeElem).css('z-index', $(activeElem.data('zindex')));
    }
}

function _openPage() {
    openPage($(this).attr('href'));
    return false;
}

$("a.button").click(_openPage);
$("a.buttonlike").click(_openPage);

