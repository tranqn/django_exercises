"""
Celery Beat — Periodic Task Scheduling

pip install django-celery-beat

settings.py:
INSTALLED_APPS += ['django_celery_beat']

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'cleanup-sessions': {
        'task': 'myapp.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    'send-daily-digest': {
        'task': 'myapp.tasks.send_daily_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week='mon-fri'),
    },
    'generate-weekly-report': {
        'task': 'myapp.tasks.generate_report',
        'schedule': crontab(hour=6, minute=0, day_of_week='monday'),
        'args': ('weekly', 'last_7_days'),
    },
}

Run Beat:
    celery -A mysite beat -l info
    celery -A mysite worker -l info
"""

from celery import shared_task
from django.utils import timezone


@shared_task
def cleanup_expired_sessions():
    from django.contrib.sessions.models import Session
    expired = Session.objects.filter(expire_date__lt=timezone.now())
    count = expired.count()
    expired.delete()
    return f"Cleaned {count} sessions"


@shared_task
def send_daily_digest():
    # Gather today's stats, send email to admins
    return "Daily digest sent"