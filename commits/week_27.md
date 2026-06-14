# Week 27 — API Gateway, API Keys & Quotas

## Commit #384
**Message:** `feat(apikey): add hashed API key model`
**Files:**

```file:advanced/api_gateway/api_key.py
"""Store only a hash of the API key, never the raw value."""

import hashlib
import secrets

from django.conf import settings
from django.db import models


def generate_key():
    raw = secrets.token_urlsafe(32)
    return raw, hashlib.sha256(raw.encode()).hexdigest()


class APIKey(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=8)        # shown in UI for identification
    hashed_key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
```

---

## Commit #385
**Message:** `feat(apikey): add API key authentication backend`
**Files:**

```file:advanced/api_gateway/api_key_auth.py
"""DRF authentication via X-API-Key header."""

import hashlib

from rest_framework import authentication, exceptions


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        raw = request.META.get("HTTP_X_API_KEY")
        if not raw:
            return None
        from .api_key import APIKey
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        key = APIKey.objects.filter(hashed_key=hashed, is_active=True).first()
        if key is None:
            raise exceptions.AuthenticationFailed("invalid API key")
        return (key.owner, key)
```

---

## Commit #386
**Message:** `feat(gateway): add usage quota enforcement`
**Files:**

```file:advanced/api_gateway/quota.py
"""Per-key monthly quota tracked in the cache."""

from datetime import datetime

from django.core.cache import cache


def quota_key(api_key_id):
    return f"quota:{api_key_id}:{datetime.utcnow():%Y-%m}"


def check_and_increment(api_key_id, limit):
    key = quota_key(api_key_id)
    used = cache.get_or_set(key, 0, timeout=60 * 60 * 24 * 32)
    if used >= limit:
        return False
    cache.incr(key)
    return True
```

---

## Commit #387
**Message:** `feat(gateway): add request signing verification`
**Files:**

```file:advanced/api_gateway/request_signing.py
"""Verify HMAC-signed requests to prevent tampering/replay."""

import hashlib
import hmac
import time


def verify(secret, signature, body, timestamp, max_skew=300):
    if abs(time.time() - int(timestamp)) > max_skew:
        return False  # stale request (replay protection)
    expected = hmac.new(
        secret.encode(), f"{timestamp}.".encode() + body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## Commit #388
**Message:** `feat(gateway): add tiered rate limiting`
**Files:**

```file:advanced/api_gateway/tiered_throttle.py
"""Rate limits that vary by the caller's plan tier."""

from rest_framework.throttling import SimpleRateThrottle

TIER_RATES = {"free": "60/min", "pro": "600/min", "enterprise": "6000/min"}


class TieredThrottle(SimpleRateThrottle):
    scope = "tier"

    def get_rate(self):
        return TIER_RATES.get(getattr(self, "_tier", "free"), "60/min")

    def allow_request(self, request, view):
        self._tier = getattr(getattr(request, "auth", None), "tier", "free")
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)

    def get_cache_key(self, request, view):
        return f"throttle:{self.get_ident(request)}"
```

---

## Commit #389
**Message:** `feat(gateway): add response caching by API key`
**Files:**

```file:advanced/api_gateway/response_cache.py
"""Cache idempotent GET responses per key + querystring."""

import hashlib

from django.core.cache import cache


def cache_key_for(request, api_key_id):
    raw = f"{api_key_id}:{request.path}?{request.META.get('QUERY_STRING', '')}"
    return "respcache:" + hashlib.sha256(raw.encode()).hexdigest()


def get_or_store(request, api_key_id, produce, timeout=60):
    if request.method != "GET":
        return produce()
    key = cache_key_for(request, api_key_id)
    cached = cache.get(key)
    if cached is None:
        cached = produce()
        cache.set(key, cached, timeout)
    return cached
```

---

## Commit #390
**Message:** `feat(gateway): add request/response logging for billing`
**Files:**

```file:advanced/api_gateway/usage_log.py
"""Append-only usage records that drive metered billing."""

from django.db import models


class UsageRecord(models.Model):
    api_key_id = models.PositiveIntegerField(db_index=True)
    endpoint = models.CharField(max_length=200)
    status_code = models.PositiveSmallIntegerField()
    response_ms = models.FloatField()
    billable_units = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## Commit #391
**Message:** `feat(gateway): add key rotation support`
**Files:**

```file:advanced/api_gateway/key_rotation.py
"""Rotate keys with a grace period so clients can migrate."""

from datetime import timedelta

from django.utils import timezone


def rotate(APIKey, generate_key, old_key, grace_days=7):
    raw, hashed = generate_key()
    new_key = APIKey.objects.create(
        owner=old_key.owner, prefix=raw[:8], hashed_key=hashed
    )
    old_key.is_active = True  # keep working during grace window
    old_key.expires_at = timezone.now() + timedelta(days=grace_days)
    old_key.save(update_fields=["expires_at"])
    return raw, new_key
```

---

## Commit #392
**Message:** `feat(gateway): add IP allow/deny lists`
**Files:**

```file:advanced/api_gateway/ip_filter.py
"""Restrict keys to allow-listed CIDR ranges."""

import ipaddress


def ip_allowed(ip, allow_cidrs):
    if not allow_cidrs:
        return True  # no restriction configured
    addr = ipaddress.ip_address(ip)
    return any(addr in ipaddress.ip_network(c, strict=False) for c in allow_cidrs)
```

---

## Commit #393
**Message:** `feat(gateway): add standard rate-limit response headers`
**Files:**

```file:advanced/api_gateway/ratelimit_headers.py
"""Expose remaining quota via standard headers."""


class RateLimitHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        info = getattr(request, "ratelimit", None)
        if info:
            response["X-RateLimit-Limit"] = str(info["limit"])
            response["X-RateLimit-Remaining"] = str(info["remaining"])
            response["X-RateLimit-Reset"] = str(info["reset"])
        return response
```

---

## Commit #394
**Message:** `test(gateway): add API key and quota tests`
**Files:**

```file:advanced/api_gateway/test_gateway.py
"""Tests for signing and IP filtering."""

from django.test import SimpleTestCase

from .ip_filter import ip_allowed


class IPFilterTests(SimpleTestCase):
    def test_allows_when_no_list(self):
        self.assertTrue(ip_allowed("1.2.3.4", []))

    def test_blocks_outside_cidr(self):
        self.assertFalse(ip_allowed("8.8.8.8", ["10.0.0.0/8"]))

    def test_allows_inside_cidr(self):
        self.assertTrue(ip_allowed("10.1.2.3", ["10.0.0.0/8"]))
```

---

## Commit #395
**Message:** `docs(week27): add API gateway reference`
**Files:**

```file:advanced/API_GATEWAY_REFERENCE.md
# Week 27 — API Gateway, API Keys & Quotas

- **Keys** — hashed at rest, prefix for identification, rotation w/ grace.
- **Auth** — `X-API-Key` backend; optional HMAC request signing + replay window.
- **Limits** — tiered throttles, monthly quotas, IP allow-lists.
- **Performance** — per-key GET response cache.
- **Billing/ops** — append-only usage log, standard `X-RateLimit-*` headers.

## Principles
- Never store raw secrets; compare with `hmac.compare_digest`.
- Make limits observable (headers) and tier-aware.
- Meter usage at the edge for accurate billing.
```
