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