import os
from .base import *  # ✅ OK — prod can import base, not the other way

from dotenv import load_dotenv

load_dotenv()

# DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
SECRET_KEY = os.environ.get("SECRET_KEY")

# print('basedir --------->>>>>>>>>>>>>>>>>>>>>>>', BASE_DIR)

# """
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "database" / "db.sqlite3",  # noqa: F405
    }
}
