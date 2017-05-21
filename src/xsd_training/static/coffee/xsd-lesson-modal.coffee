class XSDLessonModal
    constructor: (opts) ->
        @modalEl = opts.modalEl
        @href = opts.href
        @triggerData = opts.triggerData

        @modalHeaderEl = @modalEl.querySelector('.modal-header')
        @modalTitleEl = @modalEl.querySelector('.modal-title')
        @modalBodyEl = @modalEl.querySelector('#lesson-body')

        @preOpen()
        @fetchBody()
        $(@modalEl).on 'hidden.bs.modal', @onClose

    getStateClass: ->
        "--state-#{@triggerData.state}"

    preOpen: ->
        @modalTitleEl.innerHTML = 'Loading...'
        @modalBodyEl.innerHTML = ''

        @modalHeaderEl.classList.add(@getStateClass())

    fetchBody: ->
        xhr = new XMLHttpRequest()
        xhr.open('GET', @href)
        xhr.responseType = "document"
        xhr.onload = @renderBody
        xhr.send()

    renderBody: (event) =>
        xhr = event.target
        if xhr.status == 200
            @modalTitleEl.innerHTML = xhr.response.querySelector('#lesson-title').innerHTML
            @modalBodyEl.innerHTML = xhr.response.querySelector('#lesson-body').innerHTML
        else
            @modalBodyEl.innerHTML = "Failed to fetch lesson"

    onClose: =>
        @modalHeaderEl.classList.remove(@getStateClass())


$(document).ready ->
    $('.xsd-lesson-modal').on 'show.bs.modal', (event) ->
        lessonModal = new XSDLessonModal
            modalEl: this,
            href: event.relatedTarget.href,
            triggerData: event.relatedTarget.dataset,

        window.lessonModal = lessonModal
