import os
from .base import *  # ✅ OK — prod can import base, not the other way

from dotenv import load_dotenv

load_dotenv()

# DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
SECRET_KEY = os.environ.get("SECRET_KEY")

# print('basedir --------->>>>>>>>>>>>>>>>>>>>>>>', BASE_DIR.parent)

# """
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "database" / "db.sqlite3",  # noqa: F405
    }
}

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",  # Frontend origin
    "http://127.0.0.1:3000",  # Frontend origin
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Add your frontend's URL
    "http://127.0.0.1:3000",  # If you're using localhost
]

# If you want to allow all origins (NOT recommended for production)
# CORS_ALLOW_ALL_ORIGINS = True  # ❌ Don't use this with credentials

# Allow headers (optional, but often needed)
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Resion Set into this server
REGION = "Nepal-01"  # Example: India / Singapore data center
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
