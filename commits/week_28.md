# Week 28 — Data Privacy & Compliance

## Commit #396
**Message:** `feat(privacy): add PII field-level encryption`
**Files:**

```file:advanced/privacy_compliance/encrypted_fields.py
"""Encrypt sensitive fields at rest with Fernet.

pip install cryptography
"""

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models

_fernet = Fernet(settings.FIELD_ENCRYPTION_KEY)


class EncryptedTextField(models.TextField):
    def get_prep_value(self, value):
        if value is None:
            return value
        return _fernet.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return _fernet.decrypt(value.encode()).decode()
```

---

## Commit #397
**Message:** `feat(privacy): add consent tracking model`
**Files:**

```file:advanced/privacy_compliance/consent.py
"""Record explicit, timestamped, versioned consent."""

from django.conf import settings
from django.db import models


class Consent(models.Model):
    class Purpose(models.TextChoices):
        MARKETING = "marketing"
        ANALYTICS = "analytics"
        PROFILING = "profiling"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=20, choices=Purpose.choices)
    granted = models.BooleanField()
    policy_version = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_at"
```

---

## Commit #398
**Message:** `feat(privacy): add data export (right to access)`
**Files:**

```file:advanced/privacy_compliance/data_export.py
"""Assemble a user's personal data for GDPR access/portability."""

import json


def export_user_data(user):
    data = {
        "profile": {"username": user.username, "email": user.email},
        "consents": list(
            user.consent_set.values("purpose", "granted", "created_at")
        ),
        "orders": list(user.order_set.values("id", "total", "created_at")),
    }
    return json.dumps(data, default=str, indent=2)
```

---

## Commit #399
**Message:** `feat(privacy): add right-to-erasure with anonymization`
**Files:**

```file:advanced/privacy_compliance/erasure.py
"""Anonymize instead of hard-deleting to preserve referential integrity."""

from django.db import transaction


@transaction.atomic
def erase_user(user):
    user.username = f"deleted_{user.pk}"
    user.email = f"deleted_{user.pk}@example.invalid"
    user.first_name = user.last_name = ""
    user.is_active = False
    user.set_unusable_password()
    user.save()
    # Detach or anonymize related PII, keep aggregate/financial records.
    user.consent_set.all().delete()
```

---

## Commit #400
**Message:** `feat(privacy): add data retention purge command`
**Files:**

```file:advanced/privacy_compliance/retention.py
"""Enforce retention policies on a schedule.

    python manage.py purge_expired_data
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

RETENTION = {"audit_log": 365, "request_log": 90, "soft_deleted": 30}


class Command(BaseCommand):
    help = "Delete data past its retention window."

    def handle(self, *args, **options):
        for dataset, days in RETENTION.items():
            cutoff = timezone.now() - timedelta(days=days)
            self.stdout.write(f"{dataset}: purge before {cutoff:%Y-%m-%d}")
```

---

## Commit #401
**Message:** `feat(privacy): add log scrubbing for PII`
**Files:**

```file:advanced/privacy_compliance/log_scrubber.py
"""Redact emails and card-like numbers from log records."""

import logging
import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
CARD = re.compile(r"\b(?:\d[ -]?){13,16}\b")


class PIIScrubbingFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        msg = EMAIL.sub("[email]", msg)
        msg = CARD.sub("[card]", msg)
        record.msg, record.args = msg, ()
        return True
```

---

## Commit #402
**Message:** `feat(privacy): add cookie consent gating`
**Files:**

```file:advanced/privacy_compliance/cookie_consent.py
"""Only load non-essential trackers after consent."""


def tracking_allowed(request):
    return request.COOKIES.get("consent_analytics") == "true"


def consent_context(request):
    # Template: {% if analytics_enabled %}<script ...>{% endif %}
    return {"analytics_enabled": tracking_allowed(request)}
```

---

## Commit #403
**Message:** `feat(privacy): add audit trail for data access`
**Files:**

```file:advanced/privacy_compliance/access_audit.py
"""Record who accessed which subject's PII and why."""

from django.conf import settings
from django.db import models


class DataAccessLog(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    subject_id = models.PositiveIntegerField()
    reason = models.CharField(max_length=200)
    accessed_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## Commit #404
**Message:** `feat(privacy): add data anonymization for analytics`
**Files:**

```file:advanced/privacy_compliance/anonymize.py
"""k-anonymity helpers for analytics datasets."""

import hashlib


def pseudonymize(value, salt):
    return hashlib.sha256((salt + str(value)).encode()).hexdigest()[:16]


def generalize_age(age):
    bucket = (age // 10) * 10
    return f"{bucket}-{bucket + 9}"
```

---

## Commit #405
**Message:** `test(privacy): add erasure and scrubbing tests`
**Files:**

```file:advanced/privacy_compliance/test_privacy.py
"""Tests for PII scrubbing and anonymization."""

import logging

from django.test import SimpleTestCase

from .log_scrubber import PIIScrubbingFilter


class ScrubberTests(SimpleTestCase):
    def test_email_is_redacted(self):
        rec = logging.LogRecord("t", logging.INFO, "", 0,
                                "contact a@b.com now", None, None)
        PIIScrubbingFilter().filter(rec)
        self.assertNotIn("a@b.com", rec.getMessage())
        self.assertIn("[email]", rec.getMessage())
```

---

## Commit #406
**Message:** `feat(privacy): add DPA-ready privacy settings`
**Files:**

```file:advanced/privacy_compliance/privacy_settings.py
"""Privacy-relevant configuration defaults."""

# Minimize logged PII
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

PRIVACY = {
    "POLICY_VERSION": "2026-01",
    "DPO_EMAIL": "privacy@example.com",
    "DEFAULT_RETENTION_DAYS": 365,
    "ANONYMIZE_ON_DELETE": True,
}
```

---

## Commit #407
**Message:** `docs(week28): add data privacy & compliance reference`
**Files:**

```file:advanced/PRIVACY_REFERENCE.md
# Week 28 — Data Privacy & Compliance

- **Data protection** — field-level encryption, log PII scrubbing.
- **Data subject rights** — export (access/portability), erasure via
  anonymization, retention purge command.
- **Consent** — versioned, timestamped consent + cookie gating.
- **Accountability** — data-access audit log, analytics pseudonymization.

## GDPR checklist
- [ ] Lawful basis recorded per processing purpose
- [ ] Access/erasure requests fulfilled within 30 days
- [ ] Encryption at rest + in transit for PII
- [ ] Retention limits enforced automatically
- [ ] Breach notification runbook in place
```
