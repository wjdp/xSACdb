import os
import re
from typing import Optional


def get_version() -> Optional[str]:
    """Version is either the release or the release + sha1 tail, e.g. v0.8.0-26-gea9f8a4"""
    return os.environ.get('VCS_REV', None) or None


g_sha_matcher = re.compile('-\d+-g\w+$')


def get_release() -> Optional[str]:
    """Release name only changes after a release, e.g. v0.8.0"""
    if not get_version():
        return None

    # turn v0.8.0-26-gea9f8a4 → 0.8.0
    return g_sha_matcher.sub('', get_version())


def get_sentry_release() -> Optional[str]:
    """xsacdb@0.8.0, includes project name as sentry releases want to be unique"""
    if not get_release():
        return None
    return f"xsacdb@{get_release().lstrip('v')}"


VERSION = get_version()
RELEASE = get_release()
RELEASE_SENTRY = get_sentry_release()
