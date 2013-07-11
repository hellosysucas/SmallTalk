#!/usr/bin/env python

#Jiahao Added
#<<<<<<< HEAD
import os
import sys
 
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmallTalk.settings")
 
    from django.core.management import execute_from_command_line
 
    execute_from_command_line(sys.argv)

#Wangtao Added
# =======

# from django.core.management import execute_manager
# import imp
# try:
#     imp.find_module('settings') # Assumed to be in the same directory.
# except ImportError:
#     import sys
#     sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
#     sys.exit(1)
# 
# import settings
# 
# if __name__ == "__main__":
#     execute_manager(settings)
# # >>>>>>> a9ce19d7a17c5cf829ae482f296681c2838498a4
