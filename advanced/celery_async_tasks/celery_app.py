"""
mysite/celery.py — Celery application configuration.

Requirements: pip install celery redis django-celery-results
Redis: brew install redis && brew services start redis
"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = Celery("mysite")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")