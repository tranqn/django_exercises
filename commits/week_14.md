# Week 14 — Observability, Testing & Performance

## Commit #227
**Message:** `test(setup): add pytest configuration and shared fixtures`
**Files:**

```file:advanced/observability/conftest.py
"""
pytest + pytest-django setup.

pip install pytest pytest-django factory_boy
pytest.ini:
    [pytest]
    DJANGO_SETTINGS_MODULE = mysite.settings
    python_files = test_*.py
"""

import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("tester", password="pw-12345!")


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client
```

---

## Commit #228
**Message:** `test(api): add API integration tests with factory_boy`
**Files:**

```file:advanced/observability/factories.py
"""factory_boy factories for fast, readable test data."""

import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    is_active = True
```

```file:advanced/observability/test_api.py
import pytest

pytestmark = pytest.mark.django_db


def test_protected_endpoint_requires_auth(client):
    resp = client.get("/api/profile/")
    assert resp.status_code in (401, 403)


def test_profile_endpoint_returns_user(auth_client):
    resp = auth_client.get("/api/profile/")
    assert resp.status_code == 200
```

---

## Commit #229
**Message:** `feat(observability): add structured logging configuration`
**Files:**

```file:advanced/observability/logging_config.py
"""
JSON logging config for settings.LOGGING. Pairs with log shippers
that parse structured output.

pip install python-json-logger
"""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"level": "WARNING", "propagate": True},
    },
}
```

---

## Commit #230
**Message:** `feat(observability): add Sentry error tracking integration`
**Files:**

```file:advanced/observability/sentry_setup.py
"""
Sentry integration. Add to settings.py.

pip install "sentry-sdk[django]"
"""

import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


def init_sentry():
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        return
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=os.environ.get("ENVIRONMENT", "production"),
    )
```

---

## Commit #231
**Message:** `feat(observability): add Prometheus metrics endpoint`
**Files:**

```file:advanced/observability/metrics.py
"""
Expose application metrics for Prometheus scraping.

pip install prometheus-client
Wire `metrics_view` to GET /metrics (restrict to internal network).
"""

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency", ["endpoint"]
)


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
```

---

## Commit #232
**Message:** `feat(health): add liveness and readiness probe endpoints`
**Files:**

```file:advanced/observability/health.py
"""
Health endpoints for load balancers / Kubernetes probes.
  - /healthz  : liveness  (process is up)
  - /readyz   : readiness (DB + cache reachable)
"""

from django.db import connections
from django.core.cache import cache
from django.http import JsonResponse


def liveness(request):
    return JsonResponse({"status": "ok"})


def readiness(request):
    checks = {}
    try:
        connections["default"].cursor().execute("SELECT 1")
        checks["db"] = "ok"
    except Exception as exc:  # pragma: no cover
        checks["db"] = f"error: {exc}"
    cache.set("readyz", "1", 5)
    checks["cache"] = "ok" if cache.get("readyz") == "1" else "error"

    healthy = all(v == "ok" for v in checks.values())
    return JsonResponse({"status": "ok" if healthy else "degraded", **checks},
                        status=200 if healthy else 503)
```

---

## Commit #233
**Message:** `perf(db): add connection pooling and composite indexes`
**Files:**

```file:advanced/observability/db_optimization.py
"""
Database performance settings and indexing guidance.
"""

# settings.py — persistent connections + Postgres pooling (Django 5.1+)
DATABASES_TUNING = {
    "default": {
        "CONN_MAX_AGE": 60,            # reuse connections for 60s
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {"pool": True},     # built-in pool (psycopg 3)
    }
}

# Example model Meta with a composite index for a common filter+sort:
#
# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20)
#
#     class Meta:
#         indexes = [
#             models.Index(fields=["customer", "-created_at"]),
#             models.Index(fields=["status"], name="order_status_idx"),
#         ]
```

---

## Commit #234
**Message:** `feat(search): add PostgreSQL full-text search`
**Files:**

```file:advanced/observability/full_text_search.py
"""
Full-text search with Postgres (no Elasticsearch needed for most apps).
"""

from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank,
)


def search_articles(queryset, term):
    """Rank articles by relevance to `term` across title + body."""
    vector = SearchVector("title", weight="A") + SearchVector("body", weight="B")
    query = SearchQuery(term, search_type="websearch")
    return (
        queryset.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0.05)
        .order_by("-rank")
    )

# For large tables, persist a SearchVectorField + GinIndex and keep it
# updated with a trigger or in save() to avoid recomputing on every query.
```

---

## Commit #235
**Message:** `feat(api): add pagination and filtering defaults`
**Files:**

```file:advanced/observability/api_pagination.py
"""
DRF pagination + django-filter setup.

pip install django-filter
"""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 200


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS":
        "advanced.observability.api_pagination.StandardResultsSetPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
}
```

---

## Commit #236
**Message:** `feat(api): add URL-path API versioning`
**Files:**

```file:advanced/observability/api_versioning.py
"""
URL-path versioning so v1 clients keep working as the API evolves.

settings.py:
    REST_FRAMEWORK["DEFAULT_VERSIONING_CLASS"] = \
        "rest_framework.versioning.URLPathVersioning"
    REST_FRAMEWORK["ALLOWED_VERSIONS"] = ["v1", "v2"]
"""

from django.urls import path, include

urlpatterns = [
    path("api/<str:version>/", include("api.urls")),
]

# In a view: request.version -> "v1" / "v2"; branch serializers accordingly.
```

---

## Commit #237
**Message:** `test(perf): add Locust load test scenario`
**Files:**

```file:advanced/observability/locustfile.py
"""
Load test with Locust:
    pip install locust
    locust -f locustfile.py --host https://staging.example.com
"""

from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/api/token/",
                         json={"username": "load", "password": "pw"})

    @task(3)
    def list_articles(self):
        self.client.get("/api/v1/articles/?page_size=25")

    @task(1)
    def view_article(self):
        self.client.get("/api/v1/articles/1/")
```

---

## Commit #238
**Message:** `ci(cd): add deployment workflow with staging gate`
**Files:**

```file:advanced/ci_cd_pipeline/deploy.yml
# Place at .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Build and push image
        run: echo "docker build / push to registry"
      - name: Run migrations
        run: echo "kubectl/ssh run python manage.py migrate"

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production   # requires manual approval gate in repo settings
    steps:
      - uses: actions/checkout@v4
      - name: Promote to production
        run: echo "promote previously verified image"
```

---

## Commit #239
**Message:** `docs(week14): add observability and testing reference`
**Files:**

```file:advanced/OBSERVABILITY_REFERENCE.md
# Week 14 — Observability, Testing & Performance

## Testing
- pytest + pytest-django, shared fixtures, factory_boy for data.
- API integration tests assert auth and response contracts.
- Locust load tests run against staging before promotion.

## Observability
- Structured JSON logging for log shippers.
- Sentry for errors (10% trace sampling, PII off).
- Prometheus `/metrics`; `/healthz` + `/readyz` probes for orchestrators.

## Performance
- Persistent DB connections + psycopg pool; composite indexes for hot paths.
- Postgres full-text search with weighted vectors + GIN index.
- Pagination, filtering and API versioning baked into DRF defaults.

## Delivery
- CI lints + tests on every PR; deploy gates production behind staging
  with a manual approval environment.

## Next steps
- Add tracing (OpenTelemetry) and SLO/alerting dashboards.
```
