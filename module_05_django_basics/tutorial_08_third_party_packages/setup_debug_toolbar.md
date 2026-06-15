# Django Debug Toolbar Setup

## Install
pip install django-debug-toolbar

## settings.py
INSTALLED_APPS = [
    "debug_toolbar",
    ...
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    ...
]

INTERNAL_IPS = ["127.0.0.1"]

## urls.py
from django.urls import include, path

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    ...
]

## Panels Available
- SQL: See all DB queries per request
- Templates: Template rendering times
- Cache: Cache hits/misses
- Signals: Signal dispatching
- Profiling: CPU profiling
- Headers: Request/response headers