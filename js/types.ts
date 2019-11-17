export interface GlobalEnv {
    name: string
    release: string | null
    sentryRelease: string | null
}

export interface GlobalSite {
    name: string
}

export interface GlobalSentry {
    dsn: string | null
}

export interface GlobalUser {
    id: string
    username: string
    email: string
}

export interface Global {
    env: GlobalEnv
    site: GlobalSite
    sentry: GlobalSentry
    user: GlobalUser | null
}
