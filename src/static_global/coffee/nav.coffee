class SideBarNav
  constructor: ->
    @hamburgerEl = document.querySelector('.xsd-nav-app__hamburger')
    @sideNavEl   = document.querySelector('.xsd-nav-app__nav')
    @blurEl      = document.querySelector('.xsd-nav-app__blur')

    @touchingSideNav = false
    @startX
    @currentX

    @hamburgerEl.addEventListener('click', @showNav)
    @blurEl.addEventListener('click', @hideNav)

    document.addEventListener('touchstart', @onTouchStart)
    document.addEventListener('touchmove', @onTouchMove)
    document.addEventListener('touchend', @onTouchEnd)

    @sideBarAppSelection = new SideBarAppSelection()

  showNav: =>
    @sideNavEl.classList.add('xsd-nav-app__nav--visible')
    @blurEl.classList.add('xsd-nav-app__blur--visible')

  hideNav: =>
    @sideNavEl.classList.remove('xsd-nav-app__nav--visible')
    @blurEl.classList.remove('xsd-nav-app__blur--visible')
    @sideBarAppSelection.reset()

  onTouchStart: (e) =>
    if not @sideNavEl.classList.contains('xsd-nav-app__nav--visible')
      return

    @startX = e.touches[0].pageX
    @currentX = @startX
    @touchingSideNav = true
    requestAnimationFrame(@update)

  onTouchMove: (e) =>
    if not @touchingSideNav
      return

    @currentX = e.touches[0].pageX

  onTouchEnd: (e) =>
    if not @touchingSideNav
      return

    console.log @currentX - @startX

    if @currentX - @startX < -50
      @hideNav()

    @touchingSideNav = false
    @sideNavEl.style.transform = ''

  update: =>
    if not @touchingSideNav
      return

    requestAnimationFrame(@update)

    translateX = Math.min(0, @currentX - @startX)
    @sideNavEl.style.transform = "translateX(#{translateX}px)"

class SideBarAppSelection
  constructor: ->
    @allAppNodes     = document.querySelectorAll('.xsd-nav-app__nav-item')
    @currentAppNode  = document.querySelector('.xsd-nav-app__nav-item.active')
    @currentAppName = @currentAppNode.dataset.appName

    for appNode in @allAppNodes
      appNode.querySelector('a').addEventListener('click', @tapApp)
      moduleNode = @getModuleNode(appNode)
      h = moduleNode.getClientRects()[0].height
      moduleNode.dataset.fullHeight = h

      unless appNode.classList.contains('selected')
        moduleNode.style.maxHeight = 0

  getModuleNode: (appNode) ->
    appNode.querySelector('.xsd-nav-app__nav-module')

  tapApp: (e) =>
    e.preventDefault()
    window.e = e
    appName = e.srcElement.parentElement.dataset.appName
    @selectApp(appName)

  selectApp: (appName) =>
    for appNode in @allAppNodes
      moduleNode = @getModuleNode(appNode)
      if appNode.dataset.appName == appName
        currentAppNode = appNode
        appNode.classList.add('selected')
        @currentAppNode = appNode
        moduleNode.style.maxHeight = "#{moduleNode.dataset.fullHeight}px"
      else
        appNode.classList.remove('selected')
        moduleNode.style.maxHeight = 0
    return currentAppNode

  reset: ->
    @selectApp(@currentAppName)

$(document).ready ->
  sideBarNav = new SideBarNav()

  window.sideBarNav = sideBarNav
