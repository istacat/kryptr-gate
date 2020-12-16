from .settings import *  # noqa F401, 403


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_database",
    }
}
