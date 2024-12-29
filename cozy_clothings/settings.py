"""
Django settings for cozy_clothings project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os

from pathlib import Path

from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-d_39ia!w4urefj6$0l9%vdmn3m*ibqh_l3@l$4gxlwk*cuw6m6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "user_management",
    "product",
    "auction",
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

ROOT_URLCONF = "cozy_clothings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

ASGI_APPLICATION = "cozy_clothings.asgi.application"
WSGI_APPLICATION = "cozy_clothings.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TRACK_STARTED = True
CELERY_ACKS_LATE = True
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://localhost:6379/0"],
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# payment gateway configurations
TRANSACTION_REDIRECT_URL = os.getenv("TRANSACTION_REDIRECT_URL")
WEBSITE_URL = os.getenv("WEBSITE_URL")

# khalti configurations
KHALTI_CUSTOMER_NAME = os.getenv("KHALTI_CUSTOMER_NAME")
KHALTI_CUSTOMER_EMAIL = os.getenv("KHALTI_CUSTOMER_EMAIL")
KHALTI_CUSTOMER_PHONE = os.getenv("KHALTI_CUSTOMER_PHONE")
KHALTI_MERCHANT_USERNAME = os.getenv("KHALTI_MERCHANT_USERNAME")
KHALTI_AUTH = os.getenv("KHALTI_AUTH")
KHALTI_URL = os.getenv("KHALTI_URL")
KHALTI_LOOKUP_URL = os.getenv("KHALTI_LOOKUP_URL")

# esewa configurations
ESEWA_SECRET_KEY = os.getenv("ESEWA_SECRET_KEY")
ESEWA_LOOKUP_URL = os.getenv("ESEWA_LOOKUP_URL")


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Jazzmin Configs
JAZZMIN_SETTINGS = {
    "site_title": "Library Admin",
    "site_header": "Library",
    "site_brand": "Cozy Clothings",
    "site_logo": "site_logo/logo.jpg",
    "site_logo_classes": "custom-logo",
    "css": ["css/admin.css"],
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-warning",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cyborg",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


# Celery Beat Schedules
CELERY_BEAT_SCHEDULE = {
    "end-auction-task": {
        "task": "auction.tasks.end_auction",  # Path to the task
        "schedule": crontab(minute="*", hour="*"),  # Runs every minute
    },
}
