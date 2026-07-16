"""Signals: stamp completion time when a task is marked done."""
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.utils import timezone
from .models import Task


@receiver(pre_save, sender=Task)
def set_completed_at(sender, instance, **kwargs):
    if instance.status == Task.Status.DONE and instance.completed_at is None:
        instance.completed_at = timezone.now()
    if instance.status != Task.Status.DONE:
        instance.completed_at = None


# Wire up in apps.py:
#   class TasksConfig(AppConfig):
#       def ready(self):
#           from . import signals  # noqa