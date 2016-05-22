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

  showNav: =>
    @sideNavEl.classList.add('xsd-nav-app__nav--visible')
    @blurEl.classList.add('xsd-nav-app__blur--visible')

  hideNav: =>
    @sideNavEl.classList.remove('xsd-nav-app__nav--visible')
    @blurEl.classList.remove('xsd-nav-app__blur--visible')

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


$(document).ready ->
  sideBarNav = new SideBarNav()
