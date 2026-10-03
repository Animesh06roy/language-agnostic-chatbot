"""
WSGI config for language_agnostic_chatbot project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_agnostic_chatbot.settings')
application = get_wsgi_application()
