# Week 12 — Production Readiness: Signals, Middleware, Caching & Deployment

## Commit #201
**Message:** `feat(signals): add model signals for profile auto-creation`
**Files:**

```file:advanced/signals_and_hooks/signals.py
"""
Django signals — decouple side effects from model save logic.

Wire these up in the app's AppConfig.ready() so they are registered
once at startup (see apps.py).
"""

import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile the first time a User is created."""
    if not created:
        return
    # Imported lazily to avoid AppRegistryNotReady at import time.
    from .models import Profile

    Profile.objects.get_or_create(user=instance)
    logger.info("Created profile for user %s", instance.pk)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Keep the related Profile in sync on every User save."""
    if hasattr(instance, "profile"):
        instance.profile.save()
```

---

## Commit #202
**Message:** `chore(signals): register signal handlers in AppConfig.ready`
**Files:**

```file:advanced/signals_and_hooks/apps.py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Importing the module connects the @receiver handlers.
        from . import signals  # noqa: F401
```

---

## Commit #203
**Message:** `feat(middleware): add request timing middleware`
**Files:**

```file:advanced/custom_middleware/timing_middleware.py
"""
Custom middleware that records how long each request takes and exposes
it via the X-Request-Duration response header. Useful for spotting slow
endpoints in production logs without a full APM stack.
"""

import time
import logging

logger = logging.getLogger("request.timing")


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000

        response["X-Request-Duration"] = f"{duration_ms:.1f}ms"
        if duration_ms > 500:
            logger.warning(
                "Slow request: %s %s took %.1fms",
                request.method, request.path, duration_ms,
            )
        return response
```

---

## Commit #204
**Message:** `feat(middleware): add structured request logging middleware`
**Files:**

```file:advanced/custom_middleware/logging_middleware.py
"""
Structured access logging — one JSON line per request. Plays nicely
with log shippers (Loki, CloudWatch, Datadog) that parse JSON.
"""

import json
import logging

logger = logging.getLogger("request.access")


class StructuredLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        logger.info(json.dumps({
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "user": getattr(request.user, "id", None),
            "ip": request.META.get("REMOTE_ADDR"),
        }))
        return response
```

---

## Commit #205
**Message:** `feat(commands): add custom management command to prune sessions`
**Files:**

```file:advanced/management_commands/prune_expired_sessions.py
"""
Custom management command:

    python manage.py prune_expired_sessions --dry-run

Place under <app>/management/commands/prune_expired_sessions.py.
"""

from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone


class Command(BaseCommand):
    help = "Delete expired sessions from the database session store."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be deleted without deleting.",
        )

    def handle(self, *args, **options):
        expired = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired.count()

        if options["dry_run"]:
            self.stdout.write(f"[dry-run] {count} expired sessions would be removed")
            return

        expired.delete()
        self.stdout.write(self.style.SUCCESS(f"Removed {count} expired sessions"))
```

---

## Commit #206
**Message:** `feat(commands): add seed_demo_data command for local dev`
**Files:**

```file:advanced/management_commands/seed_demo_data.py
"""
Seed deterministic demo data for local development and CI fixtures:

    python manage.py seed_demo_data --users 10
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo users for local development."

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=5)

    def handle(self, *args, **options):
        created = 0
        for i in range(options["users"]):
            _, was_created = User.objects.get_or_create(
                username=f"demo_user_{i}",
                defaults={"email": f"demo_user_{i}@example.com"},
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new users"))
```

---

## Commit #207
**Message:** `feat(caching): add low-level cache helpers with get_or_set`
**Files:**

```file:advanced/caching_optimization/cache_helpers.py
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
```

---

## Commit #208
**Message:** `perf(caching): add per-view cache and queryset optimization notes`
**Files:**

```file:advanced/caching_optimization/view_caching.py
"""
View-level caching and ORM optimization patterns.
"""

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Article


@method_decorator(cache_page(60 * 5), name="dispatch")
class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"

    def get_queryset(self):
        # select_related: FK joins in one query (avoids N+1).
        # prefetch_related: separate query for M2M/reverse FK.
        return (
            Article.objects
            .select_related("author")
            .prefetch_related("tags")
            .only("title", "summary", "author__username")
        )
```

---

## Commit #209
**Message:** `feat(docker): add multi-stage Dockerfile for Django app`
**Files:**

```file:advanced/docker_deployment/Dockerfile
# syntax=docker/dockerfile:1

# ---- build stage ----
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- runtime stage ----
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Run as a non-root user.
RUN useradd --create-home appuser
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .
RUN python manage.py collectstatic --noinput
USER appuser

EXPOSE 8000
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

---

## Commit #210
**Message:** `feat(docker): add docker-compose with web, db and redis services`
**Files:**

```file:advanced/docker_deployment/docker-compose.yml
services:
  web:
    build: .
    command: gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
    env_file: .env
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mysite
      POSTGRES_USER: mysite
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

---

## Commit #211
**Message:** `chore(docker): add gunicorn config and dockerignore`
**Files:**

```file:advanced/docker_deployment/gunicorn.conf.py
"""Gunicorn production configuration."""

import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
timeout = 60
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

```file:advanced/docker_deployment/.dockerignore
__pycache__/
*.pyc
.git/
.venv/
venv/
*.sqlite3
.env
.pytest_cache/
htmlcov/
```

---

## Commit #212
**Message:** `ci(github): add CI workflow with tests and linting`
**Files:**

```file:advanced/ci_cd_pipeline/django-ci.yml
# Place at .github/workflows/django-ci.yml
name: Django CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready --health-interval 10s
          --health-timeout 5s --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - name: Lint
        run: ruff check .
      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db
        run: python manage.py test --verbosity 2
```

---

## Commit #213
**Message:** `docs(week12): add production readiness and deployment overview`
**Files:**

```file:advanced/DEPLOYMENT_REFERENCE.md
# Week 12 — Production Readiness & Deployment

A summary of the patterns added this week for taking a Django project
from "runs on my machine" to "runs in production".

## Signals & hooks
- `post_save` receivers decouple side effects (profile creation) from views.
- Register handlers in `AppConfig.ready()` so they load exactly once.

## Custom middleware
- `RequestTimingMiddleware` — adds `X-Request-Duration`, logs slow requests.
- `StructuredLoggingMiddleware` — one JSON access-log line per request.

## Management commands
- `prune_expired_sessions` — housekeeping for the DB session store.
- `seed_demo_data` — deterministic fixtures for dev/CI.

## Caching & query optimization
- `cache.get_or_set` for expensive reports; atomic `incr` for counters.
- `cache_page` plus `select_related`/`prefetch_related`/`only` to kill N+1.

## Containerization
- Multi-stage `Dockerfile` running as non-root, `collectstatic` baked in.
- `docker-compose.yml` wiring web + Postgres + Redis.
- `gunicorn.conf.py` sizing workers to CPU count.

## CI/CD
- GitHub Actions: spin up Postgres, lint with ruff, run the test suite
  on every push and pull request.

## Checklist before going live
- [ ] `DEBUG = False` and `ALLOWED_HOSTS` set
- [ ] Secrets via environment, never committed
- [ ] `SECURE_SSL_REDIRECT`, HSTS, secure cookies enabled
- [ ] Static files served by WhiteNoise / CDN
- [ ] Database backups scheduled
```
