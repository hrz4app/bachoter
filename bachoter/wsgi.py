"""
WSGI config for bachoter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bachoter.settings")

try:
    from whitenoise.django import DjangoWhiteNoise

    application = DjangoWhiteNoise(get_wsgi_application())
except ImportError:
    application = get_wsgi_application()