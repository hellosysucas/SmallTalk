import os

import sys

import django.core.handlers.wsgi

sys.path.append('E:/projects/django/')

sys.path.append('E:/projects/django/SmallTalk')

sys.path.append('E:/projects/django/SmallTalk/mytalk')

os.environ['DJANGO_SETTINGS_MODULE'] = 'SmallTalk.settings'

application = django.core.handlers.wsgi.WSGIHandler()