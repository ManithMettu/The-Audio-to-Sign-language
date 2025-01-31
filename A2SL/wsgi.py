"""
WSGI config for A2SL project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')

application = get_wsgi_application()
application = WhiteNoise(application)

# Get port from environment variable or default to 8000
port = int(os.getenv('PORT', 8000))
#manith