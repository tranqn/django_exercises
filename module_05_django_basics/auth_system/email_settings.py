"""
Email configuration for development and production.

Add to settings.py:
"""

# Development — print emails to console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production — SMTP
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = 'noreply@example.com'