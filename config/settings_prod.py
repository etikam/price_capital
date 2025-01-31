import os

import dj_database_url

from .settings import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

# Security settings
SECRET_KEY = os.environ.get("SECRET_KEY")
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"

# Let's Encrypt / ACME configuration
ACME_EMAIL = os.environ.get("ACME_EMAIL")

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

# Static and media files configuration
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"

# WhiteNoise configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add WhiteNoise middleware
    # ... other middleware
]

# WhiteNoise storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Ensure static files are collected
RUN_COLLECTSTATIC = os.environ.get("RUN_COLLECTSTATIC", "true").lower() == "true"

LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "django_error.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
