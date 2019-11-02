$(document).ready(() => // clicks on the whole cell should trigger the link
    $('.xsd-pl-matrix td').on('click', function (event) {
        // triggering the link should close the popover
        $(event.target).popover('hide');
        return $('a', event.target).click();
    })
);
