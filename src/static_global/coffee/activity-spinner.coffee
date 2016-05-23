class ActivitySpinner
  constructor: ->
    @spinnerEl = document.getElementById('activity-spinner')
    window.addEventListener('beforeunload', @showSpinner)

  showSpinner: =>
    @spinnerEl.classList.add('xsd-nav-app__activity-spinner--spin')

  hideSpinner: =>
    @spinnerEl.classList.remove('xsd-nav-app__activity-spinner--spin')

$(document).ready ->
  window.activitySpinner = new ActivitySpinner()
