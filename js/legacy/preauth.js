class EmailLoginForm {
    constructor() {
        this.showEmailForm = this.showEmailForm.bind(this);
        this.hideEmailForm = this.hideEmailForm.bind(this);
        this.emailFormEl = document.querySelector('.xsd-preauth-email-login');
        this.blurEl = document.querySelector('.xsd-preauth-blur');

        this.showEl = document.querySelector('.xsd-preauth-login__alternate__email a');

        this.showEl.addEventListener('click', this.showEmailForm);
        this.blurEl.addEventListener('click', this.hideEmailForm);
    }

    showEmailForm(e) {
        e.preventDefault();
        this.emailFormEl.classList.add('xsd-preauth-email-login--visible');
        return this.blurEl.classList.add('xsd-preauth-blur--visible');
    }

    hideEmailForm(e) {
        e.preventDefault();
        this.emailFormEl.classList.remove('xsd-preauth-email-login--visible');
        return this.blurEl.classList.remove('xsd-preauth-blur--visible');
    }
}

class NewMemberActivityFaker {
    constructor() {
        this.blur = this.blur.bind(this);
        this.newMemberLink = document.querySelector('.xsd-preauth-login__alternate__register a');
        this.blurEl = document.querySelector('.xsd-preauth-blur');

        this.newMemberLink.addEventListener('click', this.blur);
    }

    blur() {
        return this.blurEl.classList.add('xsd-preauth-blur--visible');
    }
}

$(document).ready(function () {
    if (document.getElementById('xsd_frontend-login')) {
        new EmailLoginForm();
        new NewMemberActivityFaker();
    }
});
