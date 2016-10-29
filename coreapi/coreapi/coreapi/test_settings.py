
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


DATABASES = {

    'default': {
         'NAME':'machadalo',
         'ENGINE': 'django.db.backends.mysql',
         'HOST': 'localhost',
         'USER': 'root',
         'PASSWORD': 'root',
         'OPTIONS': { 'init_command' : 'SET default_storage_engine=MEMORY'}
      }

}



# INNODB
#
# # set sqlite db for fast tests
# DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'sqlitedb',
#         'HOST': 'localhost'
#     }


