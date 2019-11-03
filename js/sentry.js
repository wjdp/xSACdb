import * as Sentry from '@sentry/browser';

const g = window.g;

if (g.sentry.dsn) {
    Sentry.init({
        dsn: g.sentry.dsn,
        release: g.env.release,
        environment: g.env.name,
    });
    Sentry.setExtra("site", g.site.name);
}
