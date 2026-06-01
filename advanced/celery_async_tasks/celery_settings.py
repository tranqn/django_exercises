"""
Add to settings.py:
"""

# Celery Configuration
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Europe/Berlin'
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 300  # 5 minutes

# mysite/__init__.py:
# from .celery import app as celery_app
# __all__ = ("celery_app",)

# INSTALLED_APPS += ['django_celery_results']