"""
WSGI config for coreapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import sys
import os
import site

# project starts where django's manage.py file is located
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the app's directory to the PYTHONPATH
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'coreapi'))

# django virtualenv has the env stuff one level up from the project
PROJECT_ENV = os.path.join(os.path.dirname(PROJECT_DIR), "env")

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(os.path.join(PROJECT_ENV, 'lib/python2.7/site-packages'))
# Activate your virtual env
activate_this = os.path.expanduser(os.path.join(PROJECT_ENV, "bin/activate_this.py"))
execfile(activate_this, dict(__file__=activate_this))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coreapi.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
