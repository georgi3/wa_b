"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('django', 'SECRET_KEY')
DJANGO_ENV = config.get('django', "DJANGO_ENV")
MY_APP_DOMAIN = config.get('django', 'MY_APP_DOMAIN')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DJANGO_ENV == "development"

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "djoser",
    "corsheaders",
    'social_django',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "/static/"
MEDIA_URL = '/images/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_ROOT = "static/images"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Google Staff
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config.get('google', 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config.get('google', 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'api.pipelines.custom_social_user',  # replacing to create new acc: 'social_core.pipeline.social_auth.social_user',
    'api.pipelines.email_as_username',  # replace to use email as username # 'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'api.pipelines.user_details',  # protects first, last names from changing 'social_core.pipeline.user.user_details',
    'api.pipelines.generate_token',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'prompt': 'select_account'
}
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': "password-reset/done/{uid}/{token}/",
    'PASSWORD_RESET_CONFIRM_REVERSE': False,
}

# Email Config
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = config.get("sendgrid", "SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config.get("email", "EMAIL_SENDER")

if DJANGO_ENV == "development":
    # Development settings
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    LOGIN_REDIRECT_URL = '/accounts/login/google-oauth2/complete/'
    LOGOUT_REDIRECT_URL = 'http://localhost:3000/'

    # DJOSER CONFIG for development
    DOMAIN = 'localhost:3000'
    SITE_NAME = 'localhost:3000'

else:
    # Production settings
    ALLOWED_HOSTS = [f'{MY_APP_DOMAIN}']

    CORS_ALLOWED_ORIGINS = [
        f"https://{MY_APP_DOMAIN}",
    ]

    LOGIN_REDIRECT_URL = f'/accounts/login/google-oauth2/complete/'
    LOGOUT_REDIRECT_URL = f'https://{MY_APP_DOMAIN}/'

    # DJOSER CONFIG for production
    DOMAIN = f'{MY_APP_DOMAIN}'
    SITE_NAME = f'{MY_APP_DOMAIN}'
