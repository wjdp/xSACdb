class EmailLoginForm
    constructor: ->
        @emailFormEl = document.querySelector('.xsd-preauth-email-login')
        @blurEl = document.querySelector('.xsd-preauth-blur')

        @showEl = document.querySelector('.xsd-preauth-login__alternate__email a')

        @showEl.addEventListener('click', @showEmailForm)
        @blurEl.addEventListener('click', @hideEmailForm)

    showEmailForm: (e) =>
        e.preventDefault()
        @emailFormEl.classList.add('xsd-preauth-email-login--visible')
        @blurEl.classList.add('xsd-preauth-blur--visible')
    hideEmailForm: (e) =>
        e.preventDefault()
        @emailFormEl.classList.remove('xsd-preauth-email-login--visible')
        @blurEl.classList.remove('xsd-preauth-blur--visible')

class NewMemberActivityFaker
    constructor: ->
        @newMemberLink = document.querySelector('.xsd-preauth-login__alternate__register a')
        @blurEl = document.querySelector('.xsd-preauth-blur')

        @newMemberLink.addEventListener('click', @blur)

    blur: (e) =>
        @blurEl.classList.add('xsd-preauth-blur--visible')

$(document).ready ->
    if document.getElementById('xsd_frontend-login')
        emailLoginForm = new EmailLoginForm()
        newMemberActivityFaker = new NewMemberActivityFaker()
        window.elf = emailLoginForm
