from __future__ import print_function

import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = '!5myuh^d23p9$$lo5k$39x&ji!vceayg+wwt472!bgs$0!i3k4'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'drf_hstore',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    },
}

ALLOWED_HOSTS = []

ROOT_URLCONF = 'tests.urls'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = '%s/media/' % SITE_ROOT
MEDIA_URL = '/media/'
STATIC_ROOT = '%s/static/' % SITE_ROOT
STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_hstore',
    'rest_framework',
    'tests',
)

try:
    from testsettings_local import *
except ImportError:
    pass
