from .base import *

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-IN"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 240 * 60

SESSION_IDLE_TIMEOUT = 240 * 60

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "staticfiles"]

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True
