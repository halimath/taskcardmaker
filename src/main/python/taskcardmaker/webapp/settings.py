import os.path

###########################################################################
# APPLICATION SPECIFIC SETTINGS
###########################################################################

###########################################################################
# DJANGO SPECIFIC SETTINGS
###########################################################################

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Alexander Metzner', 'alexander.metzner@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'en-en'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = ''

MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'l(j_(2w2@5q7j&f&in$t8c1ouxa01w1gmo4%xtka3rtoc(lcs%'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'taskcardmaker.webapp.urls'

TEMPLATE_DIRS = (
    os.path.dirname(__file__) + "/templates"
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'taskcardmaker.webapp'
)
