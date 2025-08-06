import os
from .base import *  # ✅ OK — prod can import base, not the other way

from dotenv import load_dotenv

load_dotenv()

# DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
SECRET_KEY = os.environ.get("SECRET_KEY")

# """
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "database" / "db.sqlite3",  # noqa: F405
    }
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "tiktokapi",
#         "USER": "admin",
#         "PASSWORD": "admin",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

"""
# CSRF_TRUSTED_ORIGINS = [
#     "https://web-production-9fcc5.up.railway.app",  # ✅ Add production domain here
# ]


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # Add your frontend's URL
#     "http://127.0.0.1:3000",  # If you're using localhost
# ]
"""

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
