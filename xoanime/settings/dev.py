from .config import *

ALLOWED_HOSTS = []

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECRET_KEY = "django-insecure-9@jipfeauz1ptrwvc5f$n@thjtw4kqkp7@-x#@=@)^ntu+td#8"
