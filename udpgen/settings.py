# Copyright 2012 Ben Cordero.
#
# This file is part of udpgen.
#
# udpgen is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# udpgen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with udpgen.  If not, see <http://www.gnu.org/licenses/>.

import os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True if os.environ.get('DEBUG') == 'True' else False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Ben Cordero', 'bmc@linux.com'),
)

MANAGERS = ADMINS

import dj_database_url
DATABASES = { 'default': dj_database_url.config(default='sqlite:///db.sqlite3') }

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(ROOT, 'media'))
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(ROOT, 'static'))
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
import uuid
SECRET_KEY = uuid.uuid4()

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'udpgen.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'udpgen.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
	    'formatter': 'verbose',
        },
	'syslog': {
	    'level': 'INFO',
	    'class': 'logging.handlers.SysLogHandler',
            'formatter': 'simple',
	},
    },
    'formatters': {
        'verbose': {
	    'format': '%(levelname)s %(asctime)s %(module)s %(lineno)s: %(message)s',
	},
	'simple': {
	    'format': '%(asctime)s: %(message)s',
	},
    },
    'loggers': {
        'django': {
	    'handlers': ['stream'],
	    'level': 'INFO' if DEBUG else 'WARNING',
	    'propagate': True,
	},
        'udpgen': {
            'handlers': ['stream', 'syslog'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['stream'],
	'level': 'DEBUG' if DEBUG else 'INFO',
    },
}
import logging.config
logging.config.dictConfig(LOGGING)

# Write to this socket to control the generation daemon.
# For starting and stopping udp streams.
UDPGEN_CONTROL_SOCKET = os.environ.get('UDPGEN_CONTROL_SOCKET', os.path.join(ROOT, 'udpgenctl.sock'))

# Specify a port, or use a random port to receive udp streams.
UDPGEN_LISTEN_PORT = os.environ.get('UDPGEN_LISTEN_PORT', 0)
