class XSDLessonModal {
    constructor(opts) {
        this.renderBody = this.renderBody.bind(this);
        this.onClose = this.onClose.bind(this);
        this.modalEl = opts.modalEl;
        this.href = opts.href;
        this.triggerData = opts.triggerData;

        this.modalHeaderEl = this.modalEl.querySelector('.modal-header');
        this.modalTitleEl = this.modalEl.querySelector('.modal-title');
        this.modalBodyEl = this.modalEl.querySelector('#lesson-body');

        this.preOpen();
        this.fetchBody();
        $(this.modalEl).on('hidden.bs.modal', this.onClose);
    }

    getStateClass() {
        return `--state-${this.triggerData.state}`;
    }

    preOpen() {
        this.modalTitleEl.innerHTML = 'Loading...';
        this.modalBodyEl.innerHTML = '';

        return this.modalHeaderEl.classList.add(this.getStateClass());
    }

    fetchBody() {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', this.href);
        xhr.responseType = "document";
        xhr.onload = this.renderBody;
        return xhr.send();
    }

    renderBody(event) {
        const xhr = event.target;
        if (xhr.status === 200) {
            this.modalTitleEl.innerHTML = xhr.response.querySelector('#lesson-title').innerHTML;
            return this.modalBodyEl.innerHTML = xhr.response.querySelector('#lesson-body').innerHTML;
        } else {
            return this.modalBodyEl.innerHTML = "Failed to fetch lesson";
        }
    }

    onClose() {
        return this.modalHeaderEl.classList.remove(this.getStateClass());
    }
}


$(document).ready(function () {
    const xsdLessonModal = $('.xsd-lesson-modal');
    xsdLessonModal.on('show.bs.modal', function (event) {
        // Prep the modal
        const lessonModal = new XSDLessonModal({
            modalEl: this,
            href: event.relatedTarget.href,
            triggerData: event.relatedTarget.dataset
        });

        // Save a ref for debugging
        window.lessonModal = lessonModal;

        // Set the hash to pk of lesson
        return window.location.hash = event.relatedTarget.dataset.pk;
    });

    return xsdLessonModal.on('hide.bs.modal', () => // Remove hash
        window.location.hash = '');
});
