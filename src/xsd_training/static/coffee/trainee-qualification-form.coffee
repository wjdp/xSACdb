class TraineeQualificationForm
    # Attaches to the trainee qualification create/update form
    constructor: (formEl) ->
        @formEl = formEl

        @modeDropdownEl = formEl.querySelector('#id_mode')
        @xoFieldEl = formEl.querySelector('#id_xo_from')
        @xoFormControlEl = @xoFieldEl.parentElement.parentElement

        @modeDropdownEl.addEventListener('change', @update)

        @update()

    update: =>
        if @modeDropdownEl.value != "XO"
            $(@xoFormControlEl).hide()
            @xoFieldEl.value = ""
        else
            $(@xoFormControlEl).show()


$(document).ready ->
    qualForm = document.querySelector('#trainee-qualification-form')

    if qualForm
        window.traineeQualificationForm = new TraineeQualificationForm(qualForm)
