import os
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-t6ge2uc2tz-i7_^fn#zl8(y3u@7_7nca^5%$4)3jw%)4cc3y7y"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # external apps
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # optional but highly recommended
    # internet apps
    "apps.search",
    "apps.accounts",
    "apps.products",
    "apps.orders",
    "apps.carts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # corse header
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # ... after auth middleware made my me with helped
    # "components.throttling.middleware.RateLimitHeadersMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # made my me custom middleware
    "components.middleware.request_timer.RequestTimerMiddleware",
    # 👇 Add our middleware at the end (after auth)
    "components.middleware.kyc_middleware.EnforceKYCApprovalMiddleware",
]

# ROOT_URLCONF = "aliexpressapi.urls"
ROOT_URLCONF = "configs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "configs.wsgi.application"
# WSGI_APPLICATION = "aliexpressapi.wsgi.application"

# settings.py
# REST_FRAMEWORK = {
#     # "EXCEPTION_HANDLER": "components.exceptions.handlers.custom_exception_handler",
#     "EXCEPTION_HANDLER": "components.exceptions.handlers.",
# }

# REST_FRAMEWORK = {
#     "EXCEPTION_HANDLER": "components.exceptions.handlers.custom_exception_handler",
# }

# settings.py # make it true in production
ENFORCE_KYC = os.environ.get("ENFORCE_KYC", default=False)
ENFORCE_KYC = os.environ.get("ENFORCE_KYC")


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR.parent / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.parent / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AUTH_USER_MODEL = "api.User"  # 'api' should be the name of your app
AUTH_USER_MODEL = (
    "accounts.User"  # "accounts.User"  # 'accounts' should be the name of your app
)


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "components.authentication.backends.CustomJWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "EXCEPTION_HANDLER": "components.exceptions.handlers.custom_exception_handler",
}

from datetime import timedelta


# settings.py
SIMPLE_JWT = {
    "ALGORITHM": "HS256",  # Prefer RS256/ES256 + JWKS if you can manage keys
    "SIGNING_KEY": os.environ.get("JWT_SIGNING_KEY"),  # do NOT hardcode
    "VERIFYING_KEY": os.environ.get("JWT_VERIFYING_KEY", default=""),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "LEEWAY": 10,  # small clock drift
}

# Cookies (if you choose cookie-backed refresh)
JWT_REFRESH_COOKIE = "refresh_token"
JWT_ACCESS_COOKIE = ""  # keep access in header
JWT_COOKIE_SAMESITE = "Strict"  # or "Lax" for cross-subdomain UX
JWT_COOKIE_SECURE = True  # True in production (HTTPS required)
JWT_COOKIE_HTTPONLY = True

# drf 'drf_spectacular',
SPECTACULAR_SETTINGS = {
    "TITLE": "My Aliexpress E-commerce API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}
