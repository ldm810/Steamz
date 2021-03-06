"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
PROJ_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJ_NAME + ".settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
