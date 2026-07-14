import os

from .base import *


DEBUG = False
SECRET_KEY = require_env("SECRET_KEY")
SIMPLE_JWT["SIGNING_KEY"] = require_env("JWT_SIGNING_KEY")
ALLOWED_HOSTS = env_csv("ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS must be configured in production")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": require_env("DB_NAME"),
        "USER": require_env("DB_USER"),
        "PASSWORD": require_env("DB_PASS"),
        "HOST": require_env("DB_HOST"),
        "PORT": require_env("DB_PORT"),
        "CONN_MAX_AGE": 60,
    }
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env_csv("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env_csv("CSRF_TRUSTED_ORIGINS")

JWT_COOKIE_SECURE = True
JWT_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
REGION = os.getenv("REGION", "production")
