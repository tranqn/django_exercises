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