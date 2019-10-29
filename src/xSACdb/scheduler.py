

import datetime
from collections import defaultdict

import django_rq

def periodic_test():
    return "Periodic Test"

def init_scheduler():
    scheduler = django_rq.get_scheduler('default')

    jobs = scheduler.get_jobs()
    functions = defaultdict(lambda: list())

    list(map(lambda x: functions[x.func].append(x.meta.get('interval')), jobs))

    now = datetime.datetime.now()

    def schedule_once(func, interval):
        """
        Schedule job once or reschedule when interval changes
        """
        if not func in functions or not interval in functions[func] \
                or len(functions[func]) > 1:
            # clear all scheduled jobs for this function
            list(map(scheduler.cancel, [x for x in jobs if x.func == func]))

            # schedule with new interval
            scheduler.schedule(now + datetime.timedelta(seconds=interval), func,
                               interval=interval, result_ttl=interval*7)

    schedule_once(periodic_test, interval=60)
