"""
Django Session Configuration

Add to settings.py:
"""

# Session engine options
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'       # Default: database
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'    # Cache-based
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db' # Cache + DB fallback

# Session cookie settings
# SESSION_COOKIE_AGE = 1209600  # 2 weeks (default)
# SESSION_COOKIE_SECURE = True  # Only send over HTTPS (production)
# SESSION_COOKIE_HTTPONLY = True  # Prevent JS access (default True)
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Persistent sessions (default)
# SESSION_SAVE_EVERY_REQUEST = False  # Only save when modified (default)