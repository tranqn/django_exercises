"""Liveness and readiness endpoints for load balancers and k8s probes.

    path("healthz/", liveness),    # process is up
    path("readyz/", readiness),    # dependencies (db, cache) are reachable
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
        checks["database"] = "ok"
    except Exception as exc:
        checks["database"] = f"error: {exc}"

    try:
        cache.set("_healthcheck", "1", 5)
        checks["cache"] = "ok" if cache.get("_healthcheck") == "1" else "error"
    except Exception as exc:
        checks["cache"] = f"error: {exc}"

    healthy = all(v == "ok" for v in checks.values())
    return JsonResponse(
        {"status": "ok" if healthy else "degraded", "checks": checks},
        status=200 if healthy else 503,
    )