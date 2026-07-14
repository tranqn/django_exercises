"""OpenAPI schema with drf-spectacular.

pip install drf-spectacular
settings: DEFAULT_SCHEMA_CLASS = 'drf_spectacular.openapi.AutoSchema'
"""
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView,
)

SPECTACULAR_SETTINGS = {
    "TITLE": "Blog API",
    "DESCRIPTION": "Posts, categories, tags and comments.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

schema_urls = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema")),
]