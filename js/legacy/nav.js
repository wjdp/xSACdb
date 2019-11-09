class SideBarAppSelection {
    constructor(sideBarNav) {
        this.tapApp = this.tapApp.bind(this);
        this.selectApp = this.selectApp.bind(this);
        this.sideBarNav = sideBarNav;

        this.allAppNodes = document.querySelectorAll('.xsd-nav-app__nav-item');
        this.currentAppNode = document.querySelector('.xsd-nav-app__nav-item.active');
        if (this.currentAppNode) {
            this.currentAppName = this.currentAppNode.dataset.appName;
        }

        for (const appNode of Array.from(this.allAppNodes)) {
            appNode.querySelector('a').addEventListener('click', this.tapApp);
            const moduleNode = this.getModuleNode(appNode);
            // TODO: BS4 defudge Why are we getting the height of something that is hidden, it won't work! How did this even work before?
            moduleNode.dataset.fullHeight = moduleNode.getClientRects()[0].height;

            if (!appNode.classList.contains('selected')) {
                moduleNode.style.maxHeight = 0;
            }
        }
    }

    getModuleNode(appNode) {
        return appNode.querySelector('.xsd-nav-app__nav-module');
    }

    tapApp(e) {
        e.preventDefault();
        const {
            appName
        } = e.srcElement.parentElement.dataset;
        return this.selectApp(appName);
    }

    touchEvent(e) {
        const elem = e.srcElement;
        if (elem.parentElement.dataset.appName === 'xsd-dashboard') {
            this.sideBarNav.hideNav();
            return window.location = elem.href;
        } else if (elem.classList.contains('xsd-nav-app__nav-link')) {
            return this.selectApp(elem.parentElement.dataset.appName);
        }
    }

    selectApp(appName) {
        for (const appNode of Array.from(this.allAppNodes)) {
            const moduleNode = this.getModuleNode(appNode);
            if (appNode.dataset.appName === appName) {
                appNode.classList.add('selected');
                this.currentAppNode = appNode;
                moduleNode.style.maxHeight = `${moduleNode.dataset.fullHeight}px`;
            } else {
                appNode.classList.remove('selected');
                moduleNode.style.maxHeight = 0;
            }
        }
        setTimeout(() => {
                return this.sideBarNav.scrollTo(this.currentAppNode);
            }
            , 100 + 60); // Need to wait for CSS transition because we need to know the height. Add some ms to account for delays
        return this.currentAppNode;
    }

    reset() {
        if (this.currentAppName) {
            return this.selectApp(this.currentAppName);
        }
    }
}

class SideBarModuleNavigation {
    constructor(sideBarNav) {
        this.touchEvent = this.touchEvent.bind(this);
        this.sideBarNav = sideBarNav;
    }

    touchEvent(e) {
        const elem = e.srcElement;
        if (elem.classList.contains('xsd-nav-module__link-text')) {
            this.sideBarNav.hideNav();
            return window.location = elem.parentElement.href;
        }
    }
}

class SideBarNav {
    constructor() {
        this.showNav = this.showNav.bind(this);
        this.hideViaBlur = this.hideViaBlur.bind(this);
        this.hideNav = this.hideNav.bind(this);
        this.onTouchStart = this.onTouchStart.bind(this);
        this.onTouchMove = this.onTouchMove.bind(this);
        this.onTouchEnd = this.onTouchEnd.bind(this);
        this.update = this.update.bind(this);
        this.hamburgerEl = document.querySelector('.xsd-nav-app__hamburger');
        this.pageTitle = document.querySelector('.xsd-nav-app__title');
        this.sideNavEl = document.querySelector('.xsd-nav-app__nav');
        this.sideNavInnerEl = document.querySelector('.xsd-nav-app__nav-inner');
        this.blurEl = document.querySelector('.xsd-nav-app__blur');

        this.touchingSideNav = false;
        this.doingInertialScroll = false;
        this.startX = 0;
        this.currentX = 0;
        this.startY = 0;
        this.currentY = 0;
        this.currentYTranslate = 0;
        this.translateY = 0;
        this.spreadY = 0;
        this.lastTranslateY = 0;
        this.startTimestamp = null;
        this.animationLength = null;

        this.minLimitY = 0;
        this.maxLimitY;

        this.hamburgerEl.addEventListener('click', this.showNav);
        this.pageTitle.addEventListener('click', this.showNav);
        this.blurEl.addEventListener('click', this.hideViaBlur);

        document.addEventListener('touchstart', this.onTouchStart);
        document.addEventListener('touchmove', this.onTouchMove);
        document.addEventListener('touchend', this.onTouchEnd);

        this.sideBarAppSelection = new SideBarAppSelection(this);
        this.sideBarModuleNavigation = new SideBarModuleNavigation(this);
    }

    calcLimitY() {
        return this.maxLimitY = -Math.max(this.sideNavInnerEl.offsetHeight - 200, 0);
    }

    showNav() {
        this.sideNavEl.classList.add('xsd-nav-app__nav--visible');
        this.sideNavEl.classList.add('xsd-nav-app__nav--animate');
        this.blurEl.classList.add('xsd-nav-app__blur--visible');

        // Fix #279, uses BS class on body to do this
        return $(document.body).addClass('modal-open');
    }

    hideViaBlur(e) {
        // Prevent clicking things under the blur
        e.preventDefault();
        return this.hideNav();
    }

    hideNav() {
        this.sideNavEl.classList.remove('xsd-nav-app__nav--visible');
        this.blurEl.classList.remove('xsd-nav-app__blur--visible');
        this.sideBarAppSelection.reset();

        // Fix #279, uses BS class on body to do this
        return $(document.body).removeClass('modal-open');
    }

    onTouchStart(e) {
        if (!this.sideNavEl.classList.contains('xsd-nav-app__nav--visible')) {
            return;
        } else {
            e.preventDefault();
        }

        this.sideNavEl.classList.remove('xsd-nav-app__nav--animate');
        this.sideNavInnerEl.classList.remove('xsd-nav-app__nav-inner--animate');

        e.preventDefault();

        this.startX = e.touches[0].pageX;
        this.startY = e.touches[0].pageY;
        this.currentX = this.startX;
        this.currentY = this.startY;
        this.currentYTranslate = this.startY + this.lastTranslateY;
        this.touchingSideNav = true;

        this.calcLimitY();

        return requestAnimationFrame(this.update);
    }

    onTouchMove(e) {
        if (!this.touchingSideNav) {
            return;
        } else {
            e.preventDefault();
        }

        const lastY = this.currentY;

        this.currentX = e.touches[0].pageX;
        this.currentY = e.touches[0].pageY;
        this.currentYTranslate = e.touches[0].pageY + this.lastTranslateY;

        return this.spreadY = this.currentY - lastY;
    }

    onTouchEnd(e) {
        if (!this.touchingSideNav) {
            return;
        } else {
            e.preventDefault();
        }

        this.sideNavEl.classList.add('xsd-nav-app__nav--animate');

        if ((this.currentX - this.startX) < -50) {
            this.hideNav();
        }

        this.touchingSideNav = false;
        this.sideNavEl.style.transform = "";
        // Inertial scrolling
        this.sideNavInnerEl.classList.add('xsd-nav-app__nav-inner--animate');
        const inertialScrollY = this.translateY + Math.min(250, Math.pow(1.2, this.spreadY) + (3 * this.spreadY));
        this.setTranslateY(inertialScrollY, true);
        this.lastTranslateY = this.translateY;

        // Click detection
        if ((Math.abs(this.currentX - this.startX) + Math.abs(this.currentY - this.startY)) < 3) {
            window.e = e;
            this.sideBarAppSelection.touchEvent(e);
            this.sideBarModuleNavigation.touchEvent(e);
            return this.touchEvent(e);
        }
    }

    touchEvent() {
        const elem = e.srcElement;
        if (elem.classList.contains('xsd-nav-app__blur')) {
            return this.hideNav();
        }
    }

    update() {
        if (!this.touchingSideNav) {
            return;
        }

        requestAnimationFrame(this.update);

        const translateX = Math.min(0, this.currentX - this.startX);
        if ((translateX < -10) || (this.sideNavEl.style.transform !== "")) {
            this.sideNavEl.style.transform = `translateX(${translateX}px)`;
        }

        return this.setTranslateY(this.currentYTranslate - this.startY);
    }

    setTranslateY(y, limits) {
        if (limits == null) {
            limits = false;
        }
        if (limits) {
            y = Math.min(this.minLimitY, y);
            y = Math.max(this.maxLimitY, y);
        }
        this.translateY = y;
        return this.sideNavInnerEl.style.transform = `translateY(${y}px)`;
    }

    scrollTo(elem) {
        if (this.touchingSideNav) {
            return;
        }
        this.sideNavInnerEl.classList.add('xsd-nav-app__nav-inner--animate');

        this.calcLimitY();

        this.translateY = -elem.offsetTop;
        this.lastTranslateY = this.translateY;
        return this.setTranslateY(this.translateY, true);
    }
}

$(document).ready(function () {
    if (window.detectMQ('sm') && document.getElementById('xsd-nav-app')) {
        $('.xsd-nav-app__nav-item-xsd_auth').removeClass('dropdown');
        $('.xsd-nav-app__nav-item-xsd_auth .xsd-nav-app__nav-module').removeClass('dropdown-menu');
        const sideBarNav = new SideBarNav();
        return window.sideBarNav = sideBarNav;
    }
});
