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