"""
django-cors-headers configuration.

pip install django-cors-headers
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE: put "corsheaders.middleware.CorsMiddleware" high up,
before CommonMiddleware.
"""

import os

CORS_ALLOWED_ORIGINS = [
    o for o in os.environ.get("CORS_ORIGINS", "").split(",") if o
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
# Never combine CORS_ALLOW_ALL_ORIGINS=True with credentials in prod.
CORS_ALLOW_ALL_ORIGINS = False