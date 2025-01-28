import os

import dj_database_url

from .settings import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Security settings
SECRET_KEY = os.environ.get("SECRET_KEY")
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database configuration using dj-database-url
DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://localhost/defaultdb", conn_max_age=600, conn_health_checks=True, ssl_require=True
    )
}

# Ensure database connection is secure and performant
DATABASES["default"]["OPTIONS"] = {
    "sslmode": "require",
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 10,
    "keepalives_count": 5,
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "/app/logs/django_error.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
