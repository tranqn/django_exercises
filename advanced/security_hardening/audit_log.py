"""
Lightweight audit trail for security-relevant events (logins, permission
changes, deletions). Append-only model + helper.
"""

from django.conf import settings
from django.db import models


class AuditEvent(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    action = models.CharField(max_length=64)
    target = models.CharField(max_length=255, blank=True)
    ip = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]


def record(actor, action, target="", ip=None):
    AuditEvent.objects.create(actor=actor, action=action, target=target, ip=ip)