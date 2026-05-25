"""
Django Security Hardening — Production Settings

Add to settings/prod.py:
"""

# --- HTTPS ---
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- HSTS (HTTP Strict Transport Security) ---
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# --- Cookies ---
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True

# --- Content Security ---
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = 'DENY'

# --- CORS (production) ---
# CORS_ALLOWED_ORIGINS = [
#     'https://yourdomain.com',
#     'https://app.yourdomain.com',
# ]
# CORS_ALLOW_CREDENTIALS = True

# --- Misc ---
# DEBUG = False
# ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')