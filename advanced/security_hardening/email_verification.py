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