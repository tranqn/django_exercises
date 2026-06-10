"""
Django signals — decouple side effects from model save logic.

Wire these up in the app's AppConfig.ready() so they are registered
once at startup (see apps.py).
"""

import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile the first time a User is created."""
    if not created:
        return
    # Imported lazily to avoid AppRegistryNotReady at import time.
    from .models import Profile

    Profile.objects.get_or_create(user=instance)
    logger.info("Created profile for user %s", instance.pk)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Keep the related Profile in sync on every User save."""
    if hasattr(instance, "profile"):
        instance.profile.save()