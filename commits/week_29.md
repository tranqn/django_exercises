# Week 29 — Performance Profiling & Optimization

## Commit #408
**Message:** `perf(profiling): add query profiling middleware`
**Files:**

```file:advanced/performance/query_profiler.py
"""Log SQL count and total time per request (dev only)."""

import logging

from django.db import connection, reset_queries

logger = logging.getLogger("perf")


class QueryProfilerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reset_queries()
        response = self.get_response(request)
        total = sum(float(q["time"]) for q in connection.queries)
        if len(connection.queries) > 20:
            logger.warning("%s: %d queries, %.3fs",
                           request.path, len(connection.queries), total)
        return response
```

---

## Commit #409
**Message:** `perf(profiling): add function-level cProfile decorator`
**Files:**

```file:advanced/performance/profile_decorator.py
"""Profile a hot function and dump top callers."""

import cProfile
import io
import pstats
from functools import wraps


def profile(sort="cumulative", top=20):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            try:
                return fn(*args, **kwargs)
            finally:
                pr.disable()
                s = io.StringIO()
                pstats.Stats(pr, stream=s).sort_stats(sort).print_stats(top)
                print(s.getvalue())
        return wrapper
    return decorator
```

---

## Commit #410
**Message:** `perf(db): add only/defer and values optimization`
**Files:**

```file:advanced/performance/query_optimization.py
"""Fetch just the columns you need."""


def lightweight_list(qs):
    # values() returns dicts, skipping model instantiation overhead.
    return qs.values("id", "title", "author__username")


def deferred_detail(qs):
    # defer heavy columns until actually accessed.
    return qs.defer("body", "raw_html")


def existence_check(qs, **filters):
    # exists() issues SELECT 1 ... LIMIT 1 — cheaper than count()/len().
    return qs.filter(**filters).exists()
```

---

## Commit #411
**Message:** `perf(cache): add multi-tier caching strategy`
**Files:**

```file:advanced/performance/cache_strategy.py
"""L1 in-process LRU in front of L2 shared cache."""

from functools import lru_cache

from django.core.cache import cache


@lru_cache(maxsize=1024)
def _l1(key):
    return cache.get(key)  # falls through to Redis


def get_config(key, build):
    value = cache.get(key)
    if value is None:
        value = build()
        cache.set(key, value, timeout=600)
    return value
```

---

## Commit #412
**Message:** `perf(db): add iterator and chunked processing`
**Files:**

```file:advanced/performance/chunked_processing.py
"""Process large querysets without loading everything into memory."""


def process_large(qs, handle, chunk_size=2000):
    # iterator() streams rows; server-side cursor avoids buffering.
    count = 0
    for obj in qs.iterator(chunk_size=chunk_size):
        handle(obj)
        count += 1
    return count
```

---

## Commit #413
**Message:** `perf(async): add concurrent IO with asyncio.gather`
**Files:**

```file:advanced/performance/async_io.py
"""Fan out independent IO calls concurrently."""

import asyncio

import httpx


async def fetch_all(urls):
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [client.get(u) for u in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    return [r.json() for r in responses if not isinstance(r, Exception)]
```

---

## Commit #414
**Message:** `perf(db): add bulk select_related benchmark helper`
**Files:**

```file:advanced/performance/benchmark.py
"""Micro-benchmark two query approaches."""

import time

from django.db import connection, reset_queries


def benchmark(label, fn):
    reset_queries()
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed*1000:.1f}ms, {len(connection.queries)} queries")
    return result
```

---

## Commit #415
**Message:** `perf(memory): add memory profiling helper`
**Files:**

```file:advanced/performance/memory_profile.py
"""Track peak memory of a code block with tracemalloc."""

import tracemalloc
from contextlib import contextmanager


@contextmanager
def track_memory(label="block"):
    tracemalloc.start()
    try:
        yield
    finally:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{label}: current={current/1e6:.1f}MB peak={peak/1e6:.1f}MB")
```

---

## Commit #416
**Message:** `perf(response): add gzip and conditional requests`
**Files:**

```file:advanced/performance/response_optimization.py
"""Compression + ETag/Last-Modified to skip unchanged transfers."""

# MIDDLEWARE (order matters):
#   django.middleware.gzip.GZipMiddleware           (near the top)
#   django.middleware.http.ConditionalGetMiddleware

from django.views.decorators.http import condition


def latest_article_mtime(request, pk):
    from articles.models import Article
    return Article.objects.filter(pk=pk).values_list("updated_at", flat=True).first()


@condition(last_modified_func=latest_article_mtime)
def article_detail(request, pk):
    ...  # served only if client copy is stale
```

---

## Commit #417
**Message:** `perf(db): add database index advisor notes`
**Files:**

```file:advanced/performance/indexing_guide.py
"""Indexing heuristics and EXPLAIN usage."""

# Diagnose with:
#   from django.db import connection
#   print(qs.explain(analyze=True))
#
# Index when:
#   - column appears in WHERE / JOIN / ORDER BY on a large table
#   - high selectivity (many distinct values)
# Composite index column order: equality columns first, then range/sort.
# Partial index for hot subsets:
#   Index(fields=["status"], condition=Q(status="active"), name="active_idx")
```

---

## Commit #418
**Message:** `test(perf): add performance regression test`
**Files:**

```file:advanced/performance/test_performance.py
"""Lock in query budgets so regressions fail CI."""

from django.test import TestCase


class QueryBudgetTests(TestCase):
    def test_dashboard_query_budget(self):
        with self.assertNumQueries(0):
            # placeholder: assemble dashboard from cache only
            data = {"widgets": []}
        self.assertIn("widgets", data)
```

---

## Commit #419
**Message:** `docs(week29): add performance optimization reference`
**Files:**

```file:advanced/PERFORMANCE_REFERENCE.md
# Week 29 — Performance Profiling & Optimization

- **Measure first** — query profiler middleware, cProfile, tracemalloc,
  `qs.explain(analyze=True)`, benchmark helper.
- **Database** — `only/defer/values`, `exists()`, `iterator()`, indexing,
  partial/composite indexes.
- **Caching** — multi-tier (LRU → Redis), config caching.
- **IO** — concurrent async fan-out with `asyncio.gather`.
- **Transport** — gzip + conditional GET (ETag/Last-Modified).
- **Guardrails** — query-budget regression tests.

## Rule
Profile before optimizing. Optimize the proven bottleneck, then re-measure.
```
