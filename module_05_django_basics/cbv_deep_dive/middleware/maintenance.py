from django.http import JsonResponse


class MaintenanceModeMiddleware:
    """Return 503 when MAINTENANCE_MODE is True in settings."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        if getattr(settings, "MAINTENANCE_MODE", False):
            if not request.path.startswith("/admin/"):
                return JsonResponse(
                    {"message": "Service under maintenance. Try again later."},
                    status=503,
                )
        return self.get_response(request)