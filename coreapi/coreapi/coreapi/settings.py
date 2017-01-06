"""
Django settings for coreapi project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ewis(omy!u-rgpf%9hp1^3@8ivz!upuwc&tp!0trx%#vjqs!&2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'true'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django_extensions',
    'rest_framework',
    'corsheaders',
    'rest_jwt',
    'v0',
    'drf_generators',
    'rest_framework_swagger',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'coreapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },

    'default': {
        'NAME':'machadalo',
         'ENGINE': 'django.db.backends.mysql',
         'HOST': 'localhost',
         'USER': 'root',
         'PASSWORD': 'root',
      }

    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

# settings for Django Rest Framework

# REST_FRAMEWORK = {
#     # other settings...
#     'DEFAULT_AUTHENTICATION_CLASSES': [],
#     'DEFAULT_PERMISSION_CLASSES': [],
# }



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

BASE_URL = 'http://localhost:8000/'

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
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
import datetime
from django.utils import timezone
date_string = '2016-12-1'
format = '%Y-%m-%d'
DEFAULT_DATE = timezone.make_aware(datetime.datetime.strptime(date_string, format), timezone.get_default_timezone())

# AWS settings.
AWS_ACCESS_KEY_ID = 'AKIAIIGRT3EJEDSRVSFQ'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'mdimages-test'