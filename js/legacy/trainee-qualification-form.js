class TraineeQualificationForm {
    // Attaches to the trainee qualification create/update form
    constructor(formEl) {
        this.update = this.update.bind(this);
        this.formEl = formEl;

        this.modeDropdownEl = formEl.querySelector('#id_mode');
        this.xoFieldEl = formEl.querySelector('#id_xo_from');
        this.xoFormControlEl = this.xoFieldEl.parentElement.parentElement;

        this.modeDropdownEl.addEventListener('change', this.update);

        this.update();
    }

    update() {
        if (this.modeDropdownEl.value !== "XO") {
            $(this.xoFormControlEl).hide();
            return this.xoFieldEl.value = "";
        } else {
            return $(this.xoFormControlEl).show();
        }
    }
}


$(document).ready(function () {
    const qualForm = document.querySelector('#trainee-qualification-form');

    if (qualForm) {
        return window.traineeQualificationForm = new TraineeQualificationForm(qualForm);
    }
});
