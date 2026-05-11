from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify
import logging

logger = logging.getLogger(__name__)


# Auto-generate slug on save
# @receiver(post_save, sender=Book)
# def generate_slug(sender, instance, created, **kwargs):
#     if created and not instance.slug:
#         instance.slug = slugify(instance.title)
#         instance.save(update_fields=["slug"])


# Log deletions
# @receiver(pre_delete, sender=Book)
# def log_deletion(sender, instance, **kwargs):
#     logger.warning(f"Deleting: {instance.__class__.__name__} #{instance.pk} — {instance}")