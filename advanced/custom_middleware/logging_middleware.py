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