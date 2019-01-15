"""
Django settings for coreapi project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from __future__ import absolute_import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime
from django.utils import timezone
from .config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ewis(omy!u-rgpf%9hp1^3@8ivz!upuwc&tp!0trx%#vjqs!&2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Config.DEBUG if hasattr(Config, 'DEBUG') else True

ALLOWED_HOSTS = ['13.232.210.224', 'localhost','13.127.154.33', 'api.machadalo.com', 'platform.machadalo.com',
                 '127.0.0.1', 'devapi.machadalo.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_extensions',
    'rest_framework',
    'rest_jwt',
    'corsheaders',
    'v0',
    'drf_generators',
    'rest_framework_swagger',
    'djcelery',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coreapi.urls'

SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(SETTINGS_PATH, '../v0/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'coreapi.wsgi.application'


DATABASES = {
        'default': {
            'NAME': Config.DATABASE['NAME'],
            'ENGINE': Config.DATABASE['ENGINE'],
            'HOST': Config.DATABASE['HOST'],
            'USER': Config.DATABASE['USER'],
            'PASSWORD': Config.DATABASE['PASSWORD'],
        }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

# path on the filesystem to the directory containing your static media.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# URL that makes the static media accessible over HTTP
MEDIA_URL = '/'


REST_FRAMEWORK = {
     'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        ),
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_jwt.authentication.JSONWebTokenAuthentication',
        ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}


# CORS headers
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)


# Authentication
JWT_AUTH = {
      'JWT_ENCODE_HANDLER':
      'rest_jwt.utils.jwt_encode_handler',

      'JWT_DECODE_HANDLER':
      'rest_jwt.utils.jwt_decode_handler',

      'JWT_PAYLOAD_HANDLER':
      'rest_jwt.utils.myjwt_payload_handler',

      'JWT_PAYLOAD_GET_USER_ID_HANDLER':
      'rest_jwt.utils.jwt_get_user_id_from_payload_handler',

      'JWT_RESPONSE_PAYLOAD_HANDLER':
      'rest_jwt.utils.myjwt_response_payload_handler',

      'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),

      'JWT_ALLOW_REFRESH': True,
      'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

      'JWT_VERIFY_EXPIRATION': False,
      }


BASE_URL = Config.BASE_URL

MONGO_DB = Config.MONGO_DB if hasattr(Config, 'MONGO_DB') else 'machadalo'
MONGO_DB_TEST = Config.MONGO_DB_TEST if hasattr(Config,'MONGO_DB_TEST') else 'mdtest'
DEFAULT_CC_EMAILS = Config.DEFAULT_CC_EMAILS if hasattr(Config,'DEFAULT_CC_EMAILS') else []
# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'businessdevelopment@machadalo.com'
EMAIL_HOST_PASSWORD = 'Bdshapwd#126'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_EMAIL_FROM = EMAIL_HOST_USER

# User settings. These fields will be populated for all existing records when u run migration on a model
# containing an FK to a USER.
DEFAULT_USER_ID = 1  # make sure a user with this id exists in the db
DEFAULT_USER_CODE = '0'  # default code for this user is '0'. which means a user with that id has to an admin
AUTH_USER_MODEL = 'v0.BaseUser'  # refer all references to User model by this name

# This is default datetime which populates on existing rows of the tables when migrated. it acts as a NULL
# datetime because when the Model instance is saved, this value is checked. if found, that means it was NULL
# and hence the

date_string = '2016-12-1'
format = '%Y-%m-%d'
DEFAULT_DATE = timezone.make_aware(datetime.datetime.strptime(date_string, format), timezone.get_default_timezone())

# AWS settings.
AWS_ACCESS_KEY_ID = 'AKIAJITJYDRLJ5N5CG5Q'
AWS_SECRET_ACCESS_KEY = '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'

BUCKET_NAME = 'mdimages-test'

ANDROID_BUCKET_NAME = 'androidtokyo'

# app name
APP_NAME = 'v0'

# CELERY STUFF

# BROKER_URL = 'redis://coreapi-test.3j6wudg4pu.ap-southeast-1.elasticbeanstalk.com:6379'

BROKER_URL = 'redis://localhost:6379'
CELERY_IMPORTS = ['v0.ui.website.tasks']
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'

# sends mail to developer about errors in api if this is true. usually set it to true  when deploying.
TEST_DEPLOYED = True

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        "KEY_PREFIX": "machadalo"
    }
}

CACHE_TTL = 60 * 60
