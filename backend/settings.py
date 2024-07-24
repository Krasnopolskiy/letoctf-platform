from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()

# Django
# ______________________________________________________________________________________________________________________

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="django-insecure-l877hlus+3(@==crfz0$+mc^+4hdu#%&z=8&v*9^s)j!")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=())

CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=())

CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=())

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # installed
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "admin_searchable_dropdown",
    # apps
    "backend.user",
    "backend.auth.jwt",
    "backend.auth.telegram",
    "backend.storage",
    "backend.challenge",
    "backend.event",
    "backend.notifications",
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "backend.urls"

TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ),
        },
    },
)

WSGI_APPLICATION = "backend.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": (),
}

# Databases
# ______________________________________________________________________________________________________________________

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": env.str("MYSQL_HOST", default="127.0.0.1"),
        "PORT": env.int("MYSQL_PORT", default=3306),
        "USER": env.str("MYSQL_USER", default="user"),
        "PASSWORD": env.str("MYSQL_PASSWORD", default="password"),
        "NAME": env.str("MYSQL_DATABASE", default="ctf"),
    }
}

# Security
# ______________________________________________________________________________________________________________________

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

AUTH_PASSWORD_VALIDATORS = (
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
)

AUTH_USER_MODEL = "user.User"

# Localization
# ______________________________________________________________________________________________________________________

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Static files
# ______________________________________________________________________________________________________________________

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

# S3 Storage
# ______________________________________________________________________________________________________________________

MINIO_HOST = env.str("MINIO_HOST", default="http://127.0.0.1:9000/")

MINIO_REGION = env.str("MINIO_REGION", default="us-east-1")

MINIO_BUCKET_NAME = env.str("MINIO_BUCKET_NAME", default="assets")

MINIO_ROOT_USER = env.str("MINIO_ROOT_USER", default="user")

MINIO_ROOT_PASSWORD = env.str("MINIO_ROOT_PASSWORD", default="password")
