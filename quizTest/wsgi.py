"""
WSGI config for quizTest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os,sys

# Add the app's directory to the PYTHONPATH
#sys.path.append('C:\Users\osama\Desktop\ex\quiz\quizTest')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizTest.settings')

application = get_wsgi_application()
