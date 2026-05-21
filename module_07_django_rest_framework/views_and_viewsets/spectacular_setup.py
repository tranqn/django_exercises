"""
drf-spectacular Setup — Auto-generate OpenAPI/Swagger docs.

pip install drf-spectacular

settings.py:
INSTALLED_APPS = [..., 'drf_spectacular']

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Django Exercise API',
    'DESCRIPTION': 'API for Django learning exercises',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

urls.py:
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
"""