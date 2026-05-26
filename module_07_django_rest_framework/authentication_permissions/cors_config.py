"""
CORS Configuration for Django + Frontend (React/Vue/etc.)

pip install django-cors-headers

settings.py:
INSTALLED_APPS = [..., 'corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be near top
    'django.middleware.common.CommonMiddleware',
    ...
]

# Development: allow all
CORS_ALLOW_ALL_ORIGINS = True

# Production: specific origins only
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://app.yourdomain.com',
]

CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

CORS_ALLOW_HEADERS = [
    'accept', 'authorization', 'content-type',
    'origin', 'user-agent', 'x-requested-with',
]

CORS_ALLOW_CREDENTIALS = True
"""