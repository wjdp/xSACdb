# Assorted behaviour for trainee profile page

traineeNotesInit = ->
    if window.location.hash == '#qualification-list'
        $('.xsd-qualification-modal--list').modal('show')
    else
        $(window.location.hash).click()


$(document).ready ->
    if document.querySelector('#xsd_training-TraineeNotes')
        # TODO HACK so the document is ready for clicking on
        setTimeout(traineeNotesInit, 10)
