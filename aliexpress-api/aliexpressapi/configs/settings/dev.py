import os

from .base import *


DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-development-key-change-me")
SIMPLE_JWT["SIGNING_KEY"] = os.getenv("JWT_SIGNING_KEY", SECRET_KEY)
ALLOWED_HOSTS = env_csv("ALLOWED_HOSTS", ("localhost", "127.0.0.1"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "database" / "db.sqlite3",
    }
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env_csv(
    "CORS_ALLOWED_ORIGINS", ("http://localhost:3000", "http://127.0.0.1:3000")
)
CSRF_TRUSTED_ORIGINS = env_csv(
    "CSRF_TRUSTED_ORIGINS", ("http://localhost:3000", "http://127.0.0.1:3000")
)

JWT_COOKIE_SECURE = False
JWT_COOKIE_SAMESITE = "Lax"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
REGION = "local"
