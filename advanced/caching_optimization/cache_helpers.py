"""
Low-level caching patterns. Configure a Redis backend in settings:

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
        }
    }
"""

from django.core.cache import cache


def get_expensive_report(report_id, builder, timeout=300):
    """Return a cached report, computing it via `builder` on a miss."""
    key = f"report:{report_id}"
    return cache.get_or_set(key, builder, timeout)


def invalidate_report(report_id):
    cache.delete(f"report:{report_id}")


def bump_view_counter(page_id):
    """Atomic increment that survives concurrent requests."""
    key = f"views:{page_id}"
    try:
        return cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=None)
        return 1