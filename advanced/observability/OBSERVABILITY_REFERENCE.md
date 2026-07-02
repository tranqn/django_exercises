# Observability & Performance Reference

## The Three Pillars
| Pillar | Question it answers | Django tooling |
|---|---|---|
| Logs | What happened? | structured JSON logging |
| Metrics | How much / how often? | django-prometheus, statsd |
| Traces | Where did time go? | OpenTelemetry, Sentry |

## Endpoints
- /healthz/ — liveness: is the process up?
- /readyz/  — readiness: are DB and cache reachable?

## Finding Slow Code
- django-debug-toolbar in dev shows per-request SQL and timing.
- Log django.db.backends at DEBUG to see every query.
- Wrap suspect code in assert_max_queries() to catch N+1 in tests.
- queryset.explain(analyze=True) shows the database plan.

## Caching Layers (cheapest first)
1. Per-view cache (@cache_page).
2. Template fragment cache.
3. Low-level cache API (cache.get/set) for expensive computed values.
4. select_related / prefetch_related to avoid the query entirely.

## Production Checklist
- [ ] JSON logs to stdout, shipped to an aggregator.
- [ ] Error tracking (Sentry) with release + environment tags.
- [ ] /healthz and /readyz wired behind the load balancer.
- [ ] Slow-query logging enabled on the database.
- [ ] p95 latency and error-rate dashboards with alerts.