from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings
from health_check.plugins import plugin_dir

from xSACdb.health.rq import RQWorkerHealthCheck, RQSchedulerHealthCheck
from xSACdb.scheduler import init_scheduler

class FrontendConfig(AppConfig):
    name = 'xsd_frontend'
    verbose_name = 'Frontend'

    def ready(self):
        # This really is a backend thing, but as we bundle backend with the project dir can only be done here
        plugin_dir.register(RQWorkerHealthCheck)
        plugin_dir.register(RQSchedulerHealthCheck)
        if settings.ENVIRONMENT in ('DEVELOPMENT', 'PRODUCTION'):
            init_scheduler()
