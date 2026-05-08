import json
from django.http import JsonResponse


class JSONErrorMiddleware:
    """Convert exceptions to JSON for API endpoints."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if request.path.startswith("/api/"):
            return JsonResponse(
                {"error": str(exception), "type": type(exception).__name__},
                status=500,
            )
        return None