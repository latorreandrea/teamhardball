"""
Django settings for teamhardball project.

Environment variables (no library needed — set in shell or Cloud Run):
  SECRET_KEY        — Django secret key (required in production)
  DEBUG             — 'True' | 'False' (default: False)
  ALLOWED_HOSTS     — comma-separated hosts, e.g. 'myapp.run.app,localhost'
  DATABASE_URL      — postgres://user:pass@host:5432/db  (optional, fallback to SQLite)
  EMAIL_HOST_USER   — Gmail address for SMTP
  EMAIL_HOST_PASSWORD — Gmail App Password
  DEFAULT_FROM_EMAIL — displayed sender address
  SITE_URL          — full URL of the site, e.g. https://myapp.run.app
  DISCORD_LINK      — Discord invite URL
  GS_BUCKET_NAME    — GCS bucket for static files (CSS/JS/images)
  GS_MEDIA_BUCKET_NAME — GCS bucket for user-uploaded media files
"""

import mimetypes
import os
from pathlib import Path

# Register .webp mime type — Python's mimetypes module doesn't include it by
# default, so django-storages would upload .webp files as application/octet-stream.
mimetypes.add_type('image/webp', '.webp')

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================================
# SECURITY
# ========================================
_secret_key = os.environ.get('SECRET_KEY', '')
if not _secret_key:
    if os.environ.get('DEBUG', 'False') == 'True':
        # Allow a dev-only insecure key so `runserver` works without env setup
        _secret_key = 'django-insecure-local-dev-only-do-not-use-in-production'
    else:
        raise ValueError(
            'SECRET_KEY environment variable is not set. '
            'Set it before starting the server in production.'
        )
SECRET_KEY = _secret_key

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

_raw_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(',') if h.strip()]

# Trust Cloud Run / load balancer forwarded headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# In production force HTTPS cookies
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'allauth',
    'allauth.account',
    'storages',

    # Developed apps
    'home',
    'users',
    'comms',
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
            ],
        },
    },
]

# ======================================== 
# AUTHENTICATION
# ======================================== 
SITE_ID = 1
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Django-allauth configuration
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Disabilita verifica email per ora
ACCOUNT_SIGNUP_ENABLED = False  # Disabilita registrazione autonoma
ACCOUNT_LOGIN_ON_GET = False
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'  # Custom adapter to prevent default login messages

# URL di redirect dopo login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

WSGI_APPLICATION = 'teamhardball.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
_database_url = os.environ.get('DATABASE_URL', '')

if _database_url:
    import urllib.parse
    _u = urllib.parse.urlparse(_database_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _u.path.lstrip('/'),
            'USER': _u.username,
            'PASSWORD': _u.password,
            'HOST': _u.hostname,
            'PORT': _u.port or 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'da'

TIME_ZONE = 'Europe/Copenhagen'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Source static files are always read from here by collectstatic
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (user uploads — FileField / ImageField)
MEDIA_ROOT = BASE_DIR / 'media'

_gs_static_bucket = os.environ.get('GS_BUCKET_NAME', '')
_gs_media_bucket = os.environ.get('GS_MEDIA_BUCKET_NAME', '')

# ── Static storage ────────────────────────────────────────────────────────────
if _gs_static_bucket:
    STATIC_URL = f'https://storage.googleapis.com/{_gs_static_bucket}/static/'
    _staticfiles_backend = {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': _gs_static_bucket,
            'location': 'static',
            'default_acl': 'publicRead',
        },
    }
else:
    STATIC_URL = 'static/'
    _staticfiles_backend = {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    }

# ── Media storage ─────────────────────────────────────────────────────────────
if _gs_media_bucket:
    MEDIA_URL = f'https://storage.googleapis.com/{_gs_media_bucket}/media/'
    _default_backend = {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': _gs_media_bucket,
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

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================================
# EMAIL CONFIGURATION
# ========================================
_email_user = os.environ.get('EMAIL_HOST_USER', '')

if _email_user:
    # Production: Gmail SMTP via App Password
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = _email_user
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
else:
    # Development: print to console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@nsog.dk')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ========================================
# CUSTOM SETTINGS
# ========================================
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')
DISCORD_LINK = os.environ.get('DISCORD_LINK', 'https://discord.gg/nsog-airsoft')
