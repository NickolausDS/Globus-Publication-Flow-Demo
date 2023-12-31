"""
Django settings for acdc_portal project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import globus_sdk
from gdss.app import SEARCH_INDEXES

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-88l+57j$(g9h#9y!4h_=w2#y-jwundp0ixb!@-q=lh+ep3hg$2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Required identity provider for adding group user access
# Currently set to University of Chicago
REQUIRED_IDENTITY_PROVIDER = "0dcf5063-bffd-40f7-b403-24f97e32fa47"
FLOW_GROUP = "85cacba8-7505-11ee-8903-f7056ea5e4f0"
FLOW_ID = "cb9bae3e-fc41-4a14-a600-6842a91ed553"
if not FLOW_ID:
    raise ValueError(
        "Please set FLOW_ID in your settings.py. Find your flow id by running flow.py"
    )
# This dictates which scopes will be requested on each user login
FLOW_SCOPE_NAME = f"flow_{FLOW_ID.replace('-', '_')}_user"
SOCIAL_AUTH_GLOBUS_SCOPE = [
    "openid",
    "profile",
    "email",
    "urn:globus:auth:scope:search.api.globus.org:all",
    "urn:globus:auth:scope:groups.api.globus.org:view_my_groups_and_memberships",  # noqa
    globus_sdk.SpecificFlowClient(FLOW_ID).scopes.url_scope_string(FLOW_SCOPE_NAME),
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'crispy_forms',
    'crispy_bootstrap4',
    "gdss",
    "globus_portal_framework",
    "social_django",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "globus_portal_framework.middleware.ExpiredTokenMiddleware",
    "globus_portal_framework.middleware.GlobusAuthExceptionMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

# Authentication backends setup OAuth2 handling and where user data should be
# stored
AUTHENTICATION_BACKENDS = [
    "globus_portal_framework.auth.GlobusOpenIdConnect",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "testing.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "globus_portal_framework.context_processors.globals",
            ],
        },
    },
]

WSGI_APPLICATION = "testing.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "stream": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["stream"], "level": "INFO"},
        "django.db.backends": {"handlers": ["stream"], "level": "WARNING"},
        "globus_portal_framework": {"handlers": ["stream"], "level": "INFO"},
        "gdss": {
            "handlers": ["stream"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

try:
    from .local_settings import *
except ImportError:
    pass
