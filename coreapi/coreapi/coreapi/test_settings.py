
from settings import *

# make tests faster

# no need of authentication
REST_FRAMEWORK = {
    # other settings...
    'DEFAULT_AUTHENTICATION_CLASSES': [

        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',

    ],
    'DEFAULT_PERMISSION_CLASSES': [
    ],
}


# set sqlite db for fast tests
DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb',
        'HOST': 'localhost'
    }


