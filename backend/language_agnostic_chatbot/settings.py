"""
Django Settings for Language Agnostic AI Chatbot
Smart India Hackathon 2025 — Problem Statement 25104
"""

import os
from pathlib import Path

try:  # optional: load backend/.env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')
except ImportError:
    pass

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'django-insecure-sih2025-language-agnostic-chatbot-key-dev-only'
)
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',          # Django REST Framework
    'corsheaders',             # CORS for React frontend
    'chatbot',                 # Our chatbot app
]

# Middleware — our custom language middleware is added here
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',         # Must be first for CORS
    'django.middleware.common.CommonMiddleware',
    'chatbot.middleware.language_middleware.LanguageMiddleware',  # Our custom middleware
]

# URL config
ROOT_URLCONF = 'language_agnostic_chatbot.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'language_agnostic_chatbot.wsgi.application'

# Database — SQLite (simple, no setup needed)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'

# CORS Settings — allow React frontend on port 3000
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_HEADERS = [
    'content-type',
    'accept',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# Rasa server URL (running separately on port 5005)
RASA_SERVER_URL = os.environ.get('RASA_SERVER_URL', 'http://localhost:5005')

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
