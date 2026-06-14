# Week 20 — Multi-tenancy & Scaling

## Commit #300
**Message:** `feat(scaling): add tenant model and resolver`
**Files:**

```file:advanced/scaling/tenant.py
"""Tenant model + thread-local current-tenant accessor."""

import threading

from django.db import models

_state = threading.local()


class Tenant(models.Model):
    name = models.CharField(max_length=120)
    subdomain = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)


def set_current_tenant(tenant):
    _state.tenant = tenant


def get_current_tenant():
    return getattr(_state, "tenant", None)
```

---

## Commit #301
**Message:** `feat(scaling): add tenant resolution middleware`
**Files:**

```file:advanced/scaling/tenant_middleware.py
"""Resolve tenant from subdomain on each request."""

from django.http import HttpResponseNotFound

from .tenant import Tenant, set_current_tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        sub = host.split(".")[0]
        tenant = Tenant.objects.filter(subdomain=sub, is_active=True).first()
        if tenant is None:
            return HttpResponseNotFound("unknown tenant")
        set_current_tenant(tenant)
        request.tenant = tenant
        return self.get_response(request)
```

---

## Commit #302
**Message:** `feat(scaling): add tenant-scoped manager`
**Files:**

```file:advanced/scaling/tenant_manager.py
"""Automatically filter querysets by the current tenant."""

from django.db import models

from .tenant import get_current_tenant


class TenantQuerySet(models.QuerySet):
    def for_current_tenant(self):
        tenant = get_current_tenant()
        return self.filter(tenant=tenant) if tenant else self.none()


class TenantManager(models.Manager.from_queryset(TenantQuerySet)):
    def get_queryset(self):
        return super().get_queryset().for_current_tenant()
```

---

## Commit #303
**Message:** `feat(scaling): add read-replica database router`
**Files:**

```file:advanced/scaling/db_router.py
"""Send reads to a replica, writes to primary."""

import random


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return random.choice(["replica1", "replica2"])

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, **hints):
        return db == "default"
```

---

## Commit #304
**Message:** `feat(scaling): add Celery task routing and queues`
**Files:**

```file:advanced/scaling/celery_routing.py
"""Route tasks to dedicated queues by priority/type."""

from kombu import Queue

CELERY_TASK_QUEUES = (
    Queue("default"),
    Queue("emails"),
    Queue("heavy"),
)
CELERY_TASK_ROUTES = {
    "*.send_*": {"queue": "emails"},
    "*.process_*": {"queue": "heavy"},
}
CELERY_TASK_DEFAULT_QUEUE = "default"
# Workers: celery -A mysite worker -Q heavy -c 2
```

---

## Commit #305
**Message:** `feat(scaling): add per-tenant rate limiting`
**Files:**

```file:advanced/scaling/tenant_throttle.py
"""Throttle scoped to the tenant, not just the user/IP."""

from rest_framework.throttling import SimpleRateThrottle


class TenantRateThrottle(SimpleRateThrottle):
    scope = "tenant"

    def get_cache_key(self, request, view):
        tenant = getattr(request, "tenant", None)
        if not tenant:
            return None
        return self.cache_format % {"scope": self.scope, "ident": tenant.id}
```

---

## Commit #306
**Message:** `feat(scaling): add cache-backed feature flags`
**Files:**

```file:advanced/scaling/feature_flags.py
"""Lightweight feature flags with per-tenant overrides."""

from django.core.cache import cache


def is_enabled(flag, tenant_id=None, default=False):
    if tenant_id is not None:
        override = cache.get(f"flag:{flag}:tenant:{tenant_id}")
        if override is not None:
            return override
    return cache.get(f"flag:{flag}", default)


def set_flag(flag, value, tenant_id=None):
    key = f"flag:{flag}:tenant:{tenant_id}" if tenant_id else f"flag:{flag}"
    cache.set(key, value, timeout=None)
```

---

## Commit #307
**Message:** `feat(scaling): add async task batching with chords`
**Files:**

```file:advanced/scaling/task_batching.py
"""Fan-out/fan-in with Celery groups and chords."""

from celery import chord, group, shared_task


@shared_task
def process_chunk(chunk):
    return len(chunk)


@shared_task
def summarize(results):
    return {"chunks": len(results), "items": sum(results)}


def process_large_dataset(items, size=1000):
    chunks = [items[i:i + size] for i in range(0, len(items), size)]
    return chord(group(process_chunk.s(c) for c in chunks))(summarize.s())
```

---

## Commit #308
**Message:** `feat(scaling): add pgbouncer-friendly database config`
**Files:**

```file:advanced/scaling/pgbouncer_config.py
"""Settings tuned for transaction-pooled pgbouncer."""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "CONN_MAX_AGE": 0,            # let pgbouncer own pooling
        "DISABLE_SERVER_SIDE_CURSORS": True,  # required for txn pooling
        "OPTIONS": {"options": "-c statement_timeout=15000"},
    }
}
```

---

## Commit #309
**Message:** `feat(scaling): add CDN integration for media`
**Files:**

```file:advanced/scaling/cdn.py
"""Serve media through a CDN domain with long cache lifetimes."""

import os

CDN_DOMAIN = os.environ.get("CDN_DOMAIN", "")


def cdn_url(path):
    if not CDN_DOMAIN:
        return path
    return f"https://{CDN_DOMAIN}/{path.lstrip('/')}"

# Set Cache-Control on uploads:
# AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=31536000, immutable"}
```

---

## Commit #310
**Message:** `perf(scaling): add cached_property query result layer`
**Files:**

```file:advanced/scaling/query_cache.py
"""Cache expensive, rarely-changing aggregates with explicit busting."""

from functools import wraps

from django.core.cache import cache


def cached_result(key_fn, timeout=300):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = key_fn(*args, **kwargs)
            value = cache.get(key)
            if value is None:
                value = fn(*args, **kwargs)
                cache.set(key, value, timeout)
            return value
        return wrapper
    return decorator
```

---

## Commit #311
**Message:** `docs(week20): add scaling architecture reference`
**Files:**

```file:advanced/SCALING_REFERENCE.md
# Week 20 — Multi-tenancy & Scaling

- **Multi-tenancy** — subdomain middleware, thread-local tenant,
  auto-filtering manager, per-tenant throttles & flags.
- **Database** — read-replica router, pgbouncer transaction pooling.
- **Async** — Celery queues/routing, chord fan-out/fan-in batching.
- **Caching** — query-result cache layer; CDN for immutable media.

## Scaling order of operations
1. Add indexes & fix N+1 before adding machines.
2. Cache reads (per-request → Redis → CDN).
3. Move heavy work to async queues.
4. Read replicas, then sharding/tenancy isolation.
```
