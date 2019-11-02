// Assorted behaviour for trainee profile page

const traineeNotesInit = function () {
    if (window.location.hash === '#qualification-list') {
        return $('.xsd-qualification-modal--list').modal('show');
    } else {
        return $(window.location.hash).click();
    }
};


$(document).ready(function () {
    if (document.querySelector('#xsd_training-TraineeNotes')) {
        // TODO HACK so the document is ready for clicking on
        return setTimeout(traineeNotesInit, 10);
    }
});
