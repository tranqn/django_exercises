"""
Token Authentication Setup

settings.py:
INSTALLED_APPS = [..., 'rest_framework.authtoken']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

After adding authtoken: python manage.py migrate

Generate token:
    python manage.py shell
    >>> from rest_framework.authtoken.models import Token
    >>> from django.contrib.auth.models import User
    >>> token, _ = Token.objects.get_or_create(user=User.objects.get(username='admin'))
    >>> print(token.key)

Usage:
    curl -H "Authorization: Token <key>" http://localhost:8000/api/markets/
"""