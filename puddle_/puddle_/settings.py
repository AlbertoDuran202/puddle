from pathlib import Path
import os
import sys
from dotenv import load_dotenv
load_dotenv()

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-hu(32imi+z&(9@n3pnu@s0#5x#ad23-%nzvp4j-ueln&sbr)^+"

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'albertoduran202-silver-garbanzo-9xwppqj4p74c7gxw.github.dev',
    '127.0.0.1',
]

# Añadir esta línea para configurar los orígenes CSRF confiables
CSRF_TRUSTED_ORIGINS = [
    'https://localhost:8000',
    'https://albertoduran202-silver-garbanzo-9xwppqj4p74c7gxw-8000.preview.app.github.dev',
    'https://bookish-parakeet-qx6ww9pgrp9c9q5-8000.app.github.dev',
]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "item",
    'mathfilters',
    'instagram',
    'widget_tweaks',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "puddle_.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = "puddle_.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join (BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEBUG = True

LOGIN_REDIRECT_URL = 'index'

# Añadir esta línea para utilizar el modelo CustomUser
AUTH_USER_MODEL = 'item.CustomUser'

sys.path.append(os.path.abspath("puddle_/core/templatetags"))

load_dotenv()
INSTAGRAM_USERNAME = os.environ['INSTAGRAM_USERNAME']
INSTAGRAM_PASSWORD = os.environ['INSTAGRAM_PASSWORD']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
        'item': {  # Asegúrate de reemplazar 'item' con el nombre de tu aplicación Django
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
