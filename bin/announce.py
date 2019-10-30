import imp

settings = imp.load_source('', '/app/conf/local_settings.py')
print("------------------------------------------------------------------------")
print(" xSACdb console for <{}>".format(settings.CLUB['name']))
print(" You are on a root shell, exercise caution")
print("------------------------------------------------------------------------")
