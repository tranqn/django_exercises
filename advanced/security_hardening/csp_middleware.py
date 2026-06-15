"""
Minimal Content-Security-Policy middleware. For richer policies prefer
django-csp, but this is dependency-free and good for a strict default.
"""


class ContentSecurityPolicyMiddleware:
    POLICY = "; ".join([
        "default-src 'self'",
        "img-src 'self' data:",
        "style-src 'self' 'unsafe-inline'",
        "script-src 'self'",
        "frame-ancestors 'none'",
        "base-uri 'self'",
    ])

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("Content-Security-Policy", self.POLICY)
        return response