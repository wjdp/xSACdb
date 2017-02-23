class XSDTripList
  constructor: ->
    @tableEl = document.getElementById('xsd_trip-list')
    @rows = []
    for row in @tableEl.querySelectorAll('[data-trip-row]')
      @rows.push(new XSDTripListRow(row))

class XSDTripListRow
  constructor: (row) ->
    @row = row
    linkEl = row.querySelector('[data-trip-link]')
    if linkEl
      @url = linkEl.href
      @row.addEventListener('click', @tripNavigate)

  tripNavigate: (e) =>
    window.location = @url

$(document).ready ->
  if document.getElementById('xsd_trip-list')
    tripList = new XSDTripList()
    window.xtl = tripList
