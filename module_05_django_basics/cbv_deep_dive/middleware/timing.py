import time
import logging

logger = logging.getLogger(__name__)


class RequestTimingMiddleware:
    """Log request processing time."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        response["X-Request-Duration"] = f"{duration:.4f}s"
        logger.info(f"{request.method} {request.path} — {response.status_code} — {duration:.4f}s")
        return response