import * as Sentry from '@sentry/browser';
import {Global} from '@/types';

const g = (window as any).g as Global;

if (g.sentry.dsn) {
    Sentry.init({
        dsn: g.sentry.dsn,
        release: g.env.sentryRelease || undefined,
        environment: g.env.name,
    });
    Sentry.setExtra("site", g.site.name);
}
