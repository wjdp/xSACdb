$(document).ready ->
  $('.xsd-pl-matrix td').on 'click', (event) ->
    $('a', event.target).click()
