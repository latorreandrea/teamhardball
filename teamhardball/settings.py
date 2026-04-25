"""
Django settings for teamhardball project.

Environment variables (no library needed — set in shell or Cloud Run):
  SECRET_KEY            — Django secret key (required in production)
  DEBUG                 — 'True' | 'False' (default: False)
  ALLOWED_HOSTS         — comma-separated hosts, e.g. 'localhost,127.0.0.1'
  CSRF_TRUSTED_ORIGINS  — comma-separated origins, e.g. 'https://example.com'
  DATABASE_URL          — postgres://user:pass@host:5432/db (required in production)
  EMAIL_HOST_USER       — Gmail address for SMTP
  EMAIL_HOST_PASSWORD   — Gmail App Password
  DEFAULT_FROM_EMAIL    — displayed sender address
  SITE_URL              — full URL of the site, e.g. https://myapp.run.app
  DISCORD_URL           — Discord invite URL
  GS_BUCKET_NAME        — GCS bucket for static files (CSS/JS/images)
  GS_MEDIA_BUCKET_NAME  — GCS bucket for user-uploaded media files
"""

import mimetypes
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Register .webp mime type — Python's mimetypes module doesn't include it by
# default, so django-storages would upload .webp files as application/octet-stream.
mimetypes.add_type('image/webp', '.webp')

BASE_DIR = Path(__file__).resolve().parent.parent


def get_env_list(var_name, default=''):
    """Read a comma-separated environment variable and return a cleaned list."""
    raw_value = os.environ.get(var_name, default)
    return [item.strip() for item in raw_value.split(',') if item.strip()]


# ========================================
# CORE
# ========================================
SECRET_KEY = os.environ.get('SECRET_KEY', '')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

if not SECRET_KEY and DEBUG:
    SECRET_KEY = 'django-insecure-local-dev-only-do-not-use-in-production'

ALLOWED_HOSTS = get_env_list('ALLOWED_HOSTS', 'localhost,127.0.0.1')
CSRF_TRUSTED_ORIGINS = get_env_list('CSRF_TRUSTED_ORIGINS', '')

if not DEBUG and not SECRET_KEY:
    raise ImproperlyConfigured('SECRET_KEY environment variable is required in production.')

if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured('ALLOWED_HOSTS environment variable is required in production.')

# Trust Cloud Run / load balancer forwarded headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# ========================================
# DATABASE
# ========================================
DATABASE_URL = os.environ.get('DATABASE_URL', '')

if DATABASE_URL:
    import urllib.parse

    _parsed_db = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _parsed_db.path.lstrip('/'),
            'USER': _parsed_db.username,
            'PASSWORD': _parsed_db.password,
            'HOST': _parsed_db.hostname,
            'PORT': _parsed_db.port or 5432,
        }
    }
else:
    if not DEBUG:
        raise ImproperlyConfigured('DATABASE_URL environment variable is required in production.')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ========================================
# AUTH
# ========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Third-party apps
    'allauth',
    'allauth.account',
    'storages',

    # Developed apps
    'home',
    'users',
    'comms',
    'manuals',
    'achievements',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'teamhardball.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'teamhardball.context_processors.global_urls',
            ],
        },
    },
]

SITE_ID = 1
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_ENABLED = False
ACCOUNT_LOGIN_ON_GET = False
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

WSGI_APPLICATION = 'teamhardball.wsgi.application'


# ========================================
# STORAGE (GCP)
# ========================================
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME', '')
GS_MEDIA_BUCKET_NAME = os.environ.get('GS_MEDIA_BUCKET_NAME', '')

if GS_BUCKET_NAME:
    STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
    _staticfiles_backend = {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': GS_BUCKET_NAME,
            'location': 'static',
            'default_acl': 'publicRead',
        },
    }
else:
    STATIC_URL = '/static/'
    _staticfiles_backend = {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    }

if GS_MEDIA_BUCKET_NAME:
    MEDIA_URL = f'https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/media/'
    _default_backend = {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': GS_MEDIA_BUCKET_NAME,
            'location': 'media',
            'default_acl': 'publicRead',
        },
    }
else:
    MEDIA_URL = '/media/'
    _default_backend = {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    }

STORAGES = {
    'default': _default_backend,
    'staticfiles': _staticfiles_backend,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========================================
# EMAIL
# ========================================
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')

if EMAIL_HOST_USER:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# ========================================
# CUSTOM
# ========================================
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')
DISCORD_URL = os.environ.get(
    'DISCORD_URL',
    os.environ.get('DISCORD_LINK', 'https://discord.gg/rxBf8D4x6P'),
)
DISCORD_LINK = DISCORD_URL
