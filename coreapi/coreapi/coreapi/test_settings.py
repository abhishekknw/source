to_exclude = ['REST_FRAMEWORK']

from settings import *

for name in to_exclude:
    del globals()[name]

# make tests faster
DATABASES = {

    'default':  {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb',
        'HOST': 'localhost'
    }

}
