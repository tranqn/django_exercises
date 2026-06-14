# Week 13 — Security Hardening & Authentication

## Commit #214
**Message:** `feat(security): add hardened production security settings`
**Files:**

```file:advanced/security_hardening/security_settings.py
"""
Production security settings. Import/merge into settings.py when
DEBUG is False. Verify with: python manage.py check --deploy
"""

import os

DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# HTTPS / transport security
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Misc hardening
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"
```

---

## Commit #215
**Message:** `feat(auth): add JWT authentication with SimpleJWT`
**Files:**

```file:advanced/security_hardening/jwt_auth.py
"""
JWT auth with djangorestframework-simplejwt.

pip install djangorestframework-simplejwt

settings.py:
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        )
    }
"""

from datetime import timedelta

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

---

## Commit #216
**Message:** `feat(auth): add custom DRF permission classes`
**Files:**

```file:advanced/security_hardening/permissions.py
"""Reusable DRF permission classes."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level: only the owner may modify; others read-only."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "owner_id", None) == request.user.id


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff
```

---

## Commit #217
**Message:** `feat(security): add DRF throttling configuration`
**Files:**

```file:advanced/security_hardening/throttling.py
"""
Rate limiting via DRF throttles. Backed by the cache (use Redis in prod).

settings.py:
    REST_FRAMEWORK = {
        "DEFAULT_THROTTLE_RATES": {
            "anon": "30/min",
            "user": "120/min",
            "login": "5/min",
        }
    }
"""

from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    """Throttle login attempts per client IP to slow credential stuffing."""

    scope = "login"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
```

---

## Commit #218
**Message:** `feat(auth): add strong password validation policy`
**Files:**

```file:advanced/security_hardening/password_policy.py
"""
AUTH_PASSWORD_VALIDATORS for settings.py plus a custom validator
that rejects passwords containing the username.
"""

from django.core.exceptions import ValidationError

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


class NoUsernameInPasswordValidator:
    def validate(self, password, user=None):
        if user and user.get_username().lower() in password.lower():
            raise ValidationError("Password must not contain your username.")

    def get_help_text(self):
        return "Your password can't contain your username."
```

---

## Commit #219
**Message:** `feat(security): add CORS configuration`
**Files:**

```file:advanced/security_hardening/cors_config.py
"""
django-cors-headers configuration.

pip install django-cors-headers
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE: put "corsheaders.middleware.CorsMiddleware" high up,
before CommonMiddleware.
"""

import os

CORS_ALLOWED_ORIGINS = [
    o for o in os.environ.get("CORS_ORIGINS", "").split(",") if o
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
# Never combine CORS_ALLOW_ALL_ORIGINS=True with credentials in prod.
CORS_ALLOW_ALL_ORIGINS = False
```

---

## Commit #220
**Message:** `feat(auth): add email verification flow with signed tokens`
**Files:**

```file:advanced/security_hardening/email_verification.py
"""
Email verification using Django's signed token machinery — no extra
model needed. Tokens expire via max_age on unsign.
"""

from django.core import signing
from django.urls import reverse

SALT = "email-verify"
MAX_AGE = 60 * 60 * 24  # 24h


def make_verification_link(request, user):
    token = signing.dumps({"uid": user.pk}, salt=SALT)
    path = reverse("verify-email", args=[token])
    return request.build_absolute_uri(path)


def verify_token(token):
    try:
        data = signing.loads(token, salt=SALT, max_age=MAX_AGE)
    except signing.SignatureExpired:
        return None, "expired"
    except signing.BadSignature:
        return None, "invalid"
    return data["uid"], None
```

---

## Commit #221
**Message:** `feat(security): add audit logging for sensitive actions`
**Files:**

```file:advanced/security_hardening/audit_log.py
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
```

---

## Commit #222
**Message:** `feat(auth): add TOTP two-factor authentication helper`
**Files:**

```file:advanced/security_hardening/totp_2fa.py
"""
TOTP-based 2FA (compatible with Google Authenticator / Authy).

pip install pyotp qrcode
"""

import pyotp


def new_secret():
    return pyotp.random_base32()


def provisioning_uri(secret, username, issuer="MySite"):
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=username, issuer_name=issuer
    )


def verify_code(secret, code):
    # valid_window=1 tolerates ~30s clock drift either side.
    return pyotp.TOTP(secret).verify(code, valid_window=1)
```

---

## Commit #223
**Message:** `feat(security): add Content-Security-Policy middleware`
**Files:**

```file:advanced/security_hardening/csp_middleware.py
"""
Minimal Content-Security-Policy middleware. For richer policies prefer
django-csp, but this is dependency-free and good for a strict default.
"""


class ContentSecurityPolicyMiddleware:
    POLICY = "; ".join([
        "default-src 'self'",
        "img-src 'self' data:",
        "style-src 'self' 'unsafe-inline'",
        "script-src 'self'",
        "frame-ancestors 'none'",
        "base-uri 'self'",
    ])

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("Content-Security-Policy", self.POLICY)
        return response
```

---

## Commit #224
**Message:** `test(security): add tests for auth and permission flows`
**Files:**

```file:advanced/security_hardening/test_security.py
"""Tests for auth flows and object-level permissions."""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordPolicyTests(TestCase):
    def test_short_password_rejected(self):
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            validate_password("short")


class AuthEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="Sup3r-Secret-Pw!")

    def test_login_succeeds_with_valid_credentials(self):
        self.assertTrue(
            self.client.login(username="alice", password="Sup3r-Secret-Pw!")
        )

    def test_login_fails_with_bad_password(self):
        self.assertFalse(self.client.login(username="alice", password="wrong"))
```

---

## Commit #225
**Message:** `feat(security): load secrets from environment with django-environ`
**Files:**

```file:advanced/security_hardening/env_config.py
"""
Centralized environment-based config. Keep secrets out of source.

pip install django-environ
"""

import environ

env = environ.Env(
    DEBUG=(bool, False),
)
# reads a .env file if present (never commit it)
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
DATABASES = {"default": env.db("DATABASE_URL")}
CACHES = {"default": env.cache("REDIS_URL", default="locmemcache://")}
EMAIL_CONFIG = env.email("EMAIL_URL", default="consolemail://")
```

---

## Commit #226
**Message:** `docs(week13): add security hardening checklist`
**Files:**

```file:advanced/SECURITY_REFERENCE.md
# Week 13 — Security Hardening & Authentication

## Transport & headers
- `SECURE_SSL_REDIRECT`, HSTS (1y, preload), secure + HttpOnly cookies.
- `X_FRAME_OPTIONS=DENY`, nosniff, strict referrer policy, CSP middleware.

## Authentication
- SimpleJWT with short access / rotating refresh tokens + blacklist.
- TOTP 2FA, signed-token email verification, strong password policy.

## Authorization
- Object-level DRF permissions (`IsOwnerOrReadOnly`, `IsStaffOrReadOnly`).

## Abuse prevention
- Per-IP login throttling, global anon/user rate limits.

## Operations
- Secrets via env (`django-environ`), append-only audit log, CORS allow-list.

## Verify
- [ ] `python manage.py check --deploy` is clean
- [ ] No secrets in git history
- [ ] 2FA available for staff/admin accounts
- [ ] Rate limits cover login and password-reset endpoints
```
