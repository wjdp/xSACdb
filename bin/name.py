import imp
import os

settings = imp.load_source('', '/app/conf/local_settings.py')
print getattr(settings.CLUB, 'name', 'NONAME')
