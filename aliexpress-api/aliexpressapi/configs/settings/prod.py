import os
from .base import *  # ✅ OK — prod can import base, not the other way

from dotenv import load_dotenv

load_dotenv()

# DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
SECRET_KEY = os.environ.get("SECRET_KEY")

# """

REGION = "America-01"  # Example: India / Singapore data center

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",  # Frontend origin
    "http://127.0.0.1:3000",  # Frontend origin
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Add your frontend's URL
    "http://127.0.0.1:3000",  # If you're using localhost
]

# Set CSRF cookie SameSite policy to "Lax" for moderate cross-site protection
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


ASGI_APPLICATION = "configs.asgi.application"
