$(document).ready ->
  # clicks on the whole cell should trigger the link
  $('.xsd-pl-matrix td').on 'click', (event) ->
    # triggering the link should close the popover
    $(event.target).popover('hide')
    $('a', event.target).click()
