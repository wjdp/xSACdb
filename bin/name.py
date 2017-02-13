import imp

settings = imp.load_source('', '/app/conf/local_settings.py')
print settings.CLUB.get('name', 'NONAME')
