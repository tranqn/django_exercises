# Week 18 — Payments & Third-party Integrations

## Commit #276
**Message:** `feat(payments): add Stripe checkout session`
**Files:**

```file:advanced/payments_integrations/stripe_checkout.py
"""
Create a Stripe Checkout session.

pip install stripe ; stripe.api_key = settings.STRIPE_SECRET_KEY
"""

import stripe


def create_checkout_session(price_id, customer_email, success_url, cancel_url):
    return stripe.checkout.Session.create(
        mode="payment",
        customer_email=customer_email,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
    )
```

---

## Commit #277
**Message:** `feat(payments): add Stripe webhook handler`
**Files:**

```file:advanced/payments_integrations/stripe_webhook.py
"""Verify and dispatch Stripe webhook events."""

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest("invalid signature")

    if event["type"] == "checkout.session.completed":
        pass  # fulfill order
    return HttpResponse(status=200)
```

---

## Commit #278
**Message:** `feat(payments): add subscription models`
**Files:**

```file:advanced/payments_integrations/subscription_models.py
"""Billing models linked to Stripe identifiers."""

from django.conf import settings
from django.db import models


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        PAST_DUE = "past_due"
        CANCELED = "canceled"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=64)
    stripe_subscription_id = models.CharField(max_length=64)
    status = models.CharField(max_length=20, choices=Status.choices)
    current_period_end = models.DateTimeField(null=True)

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE
```

---

## Commit #279
**Message:** `feat(integrations): add S3 media storage backend`
**Files:**

```file:advanced/payments_integrations/s3_storage.py
"""
S3 media storage with django-storages.

pip install django-storages boto3
"""

import os

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.environ["AWS_STORAGE_BUCKET_NAME"],
            "region_name": os.environ.get("AWS_S3_REGION", "eu-central-1"),
            "querystring_auth": True,
            "default_acl": "private",
        },
    },
}
```

---

## Commit #280
**Message:** `feat(integrations): add transactional email service`
**Files:**

```file:advanced/payments_integrations/email_service.py
"""Provider-agnostic email helper using Django's email backend."""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_templated_email(to, subject, template, context):
    text = render_to_string(f"email/{template}.txt", context)
    html = render_to_string(f"email/{template}.html", context)
    msg = EmailMultiAlternatives(subject, text, to=[to])
    msg.attach_alternative(html, "text/html")
    return msg.send()
```

---

## Commit #281
**Message:** `feat(integrations): add Twilio SMS notifications`
**Files:**

```file:advanced/payments_integrations/sms.py
"""
Send SMS via Twilio.

pip install twilio
"""

from django.conf import settings
from twilio.rest import Client


def send_sms(to_number, body):
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=to_number, from_=settings.TWILIO_FROM, body=body
    )
    return message.sid
```

---

## Commit #282
**Message:** `feat(integrations): add OAuth social login`
**Files:**

```file:advanced/payments_integrations/social_login.py
"""
Social auth with django-allauth.

pip install django-allauth
INSTALLED_APPS += ["allauth", "allauth.account",
                   "allauth.socialaccount",
                   "allauth.socialaccount.providers.google"]
"""

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
SOCIALACCOUNT_PROVIDERS = {
    "google": {"SCOPE": ["profile", "email"], "AUTH_PARAMS": {"access_type": "online"}}
}
```

---

## Commit #283
**Message:** `feat(integrations): add webhook delivery with retries`
**Files:**

```file:advanced/payments_integrations/webhook_delivery.py
"""Outbound webhooks delivered via Celery with exponential backoff."""

import hashlib
import hmac
import json

import requests
from celery import shared_task


def sign(secret, body):
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def deliver_webhook(self, url, secret, event):
    body = json.dumps(event).encode()
    try:
        resp = requests.post(
            url, data=body,
            headers={"X-Signature": sign(secret, body)}, timeout=10,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

---

## Commit #284
**Message:** `feat(integrations): add resilient API client with backoff`
**Files:**

```file:advanced/payments_integrations/api_client.py
"""HTTP client with retries, timeouts and a connection pool."""

import requests
from requests.adapters import HTTPAdapter, Retry


def make_session():
    session = requests.Session()
    retries = Retry(
        total=3, backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries, pool_maxsize=20))
    return session
```

---

## Commit #285
**Message:** `feat(payments): add invoice PDF generation`
**Files:**

```file:advanced/payments_integrations/invoice_pdf.py
"""
Render an HTML invoice to PDF.

pip install weasyprint
"""

from django.template.loader import render_to_string
from weasyprint import HTML


def render_invoice_pdf(invoice):
    html = render_to_string("invoices/invoice.html", {"invoice": invoice})
    return HTML(string=html).write_pdf()
```

---

## Commit #286
**Message:** `test(payments): add Stripe webhook signature tests`
**Files:**

```file:advanced/payments_integrations/test_webhook.py
"""Webhook endpoint rejects bad signatures."""

from django.test import TestCase, Client


class StripeWebhookTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_missing_signature_is_rejected(self):
        resp = self.client.post(
            "/webhooks/stripe/", data=b"{}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)
```

---

## Commit #287
**Message:** `docs(week18): add integrations reference`
**Files:**

```file:advanced/INTEGRATIONS_REFERENCE.md
# Week 18 — Payments & Third-party Integrations

- **Stripe** — Checkout sessions, signed webhooks, subscription models.
- **Storage** — private S3 media via django-storages.
- **Messaging** — templated transactional email, Twilio SMS.
- **Auth** — Google OAuth via allauth.
- **Outbound webhooks** — HMAC-signed, retried with exponential backoff.
- **HTTP** — pooled `requests.Session` with retry/backoff.
- **Documents** — WeasyPrint HTML→PDF invoices.

## Golden rules
- Verify every inbound webhook signature; respond 2xx fast, process async.
- Keep all keys in env; never log full payment payloads.
- Make outbound calls idempotent and always time-bounded.
```
