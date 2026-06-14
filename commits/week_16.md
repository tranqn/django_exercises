# Week 16 — Advanced DRF & API Design

## Commit #252
**Message:** `feat(drf): add nested serializers with writable relations`
**Files:**

```file:advanced/drf_advanced/nested_serializers.py
"""Writable nested serializer (order with line items)."""

from rest_framework import serializers


class LineItemSerializer(serializers.Serializer):
    sku = serializers.CharField()
    qty = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.Serializer):
    customer = serializers.CharField()
    items = LineItemSerializer(many=True)

    def create(self, validated_data):
        items = validated_data.pop("items")
        order = self.context["repo"].create_order(**validated_data)
        self.context["repo"].add_items(order, items)
        return order
```

---

## Commit #253
**Message:** `feat(drf): add ViewSets and DefaultRouter wiring`
**Files:**

```file:advanced/drf_advanced/viewsets.py
"""ModelViewSet + router for full CRUD with little code."""

from rest_framework import viewsets
from rest_framework.routers import DefaultRouter


def build_router(ArticleViewSet):
    router = DefaultRouter()
    router.register(r"articles", ArticleViewSet, basename="article")
    return router


class BaseModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

---

## Commit #254
**Message:** `feat(drf): add cross-field serializer validation`
**Files:**

```file:advanced/drf_advanced/validation.py
"""Field-level and object-level validation."""

from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    def validate_start(self, value):
        return value

    def validate(self, data):
        if data["end"] <= data["start"]:
            raise serializers.ValidationError("end must be after start")
        return data
```

---

## Commit #255
**Message:** `feat(drf): add SerializerMethodField computed values`
**Files:**

```file:advanced/drf_advanced/method_fields.py
"""Read-only computed fields."""

from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    full_name = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_is_online(self, obj):
        return self.context.get("online_ids", set()).__contains__(obj.id)
```

---

## Commit #256
**Message:** `feat(drf): add dynamic field selection mixin`
**Files:**

```file:advanced/drf_advanced/dynamic_fields.py
"""?fields=id,title to trim payloads (sparse fieldsets)."""

from rest_framework import serializers


class DynamicFieldsMixin:
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            fields = request.query_params.get("fields")
        if fields:
            allowed = set(fields.split(","))
            for name in set(self.fields) - allowed:
                self.fields.pop(name)
```

---

## Commit #257
**Message:** `feat(drf): add image upload serializer with validation`
**Files:**

```file:advanced/drf_advanced/upload_serializer.py
"""Validate size and content type of uploaded images."""

from rest_framework import serializers

MAX_BYTES = 5 * 1024 * 1024
ALLOWED = {"image/png", "image/jpeg", "image/webp"}


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, f):
        if f.size > MAX_BYTES:
            raise serializers.ValidationError("file too large (max 5MB)")
        if f.content_type not in ALLOWED:
            raise serializers.ValidationError("unsupported type")
        return f
```

---

## Commit #258
**Message:** `feat(drf): add OpenAPI schema with drf-spectacular`
**Files:**

```file:advanced/drf_advanced/openapi_schema.py
"""
Auto-generated OpenAPI 3 docs.

pip install drf-spectacular
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
"""

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
```

---

## Commit #259
**Message:** `feat(drf): add cursor pagination for large datasets`
**Files:**

```file:advanced/drf_advanced/cursor_pagination.py
"""Cursor pagination — stable under inserts, scales to huge tables."""

from rest_framework.pagination import CursorPagination


class TimelinePagination(CursorPagination):
    page_size = 50
    ordering = "-created_at"
    cursor_query_param = "cursor"
```

---

## Commit #260
**Message:** `feat(drf): add custom exception handler`
**Files:**

```file:advanced/drf_advanced/exception_handler.py
"""Uniform error envelope for all API errors."""

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "error": {
                "status": response.status_code,
                "detail": response.data,
            }
        }
    return response
```

---

## Commit #261
**Message:** `feat(drf): add throttled action with @action decorator`
**Files:**

```file:advanced/drf_advanced/custom_actions.py
"""Extra routes on a ViewSet via @action."""

from rest_framework.decorators import action
from rest_framework.response import Response


class ArticleActionsMixin:
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        article = self.get_object()
        article.status = "published"
        article.save(update_fields=["status"])
        return Response({"status": "published"})

    @action(detail=False)
    def trending(self, request):
        qs = self.get_queryset().order_by("-views")[:10]
        return Response(self.get_serializer(qs, many=True).data)
```

---

## Commit #262
**Message:** `test(drf): add APITestCase for article endpoints`
**Files:**

```file:advanced/drf_advanced/test_api.py
"""DRF endpoint tests."""

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class ArticleAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("a", password="pw-12345!")
        self.client.force_authenticate(self.user)

    def test_list_returns_200(self):
        resp = self.client.get("/api/articles/")
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_title(self):
        resp = self.client.post("/api/articles/", {}, format="json")
        self.assertEqual(resp.status_code, 400)
```

---

## Commit #263
**Message:** `docs(week16): add API design guidelines`
**Files:**

```file:advanced/API_DESIGN_REFERENCE.md
# Week 16 — Advanced DRF & API Design

- **ViewSets + routers** — CRUD with minimal boilerplate; `@action` for extras.
- **Serializers** — writable nested, cross-field validation, method fields,
  sparse fieldsets (`?fields=`), validated uploads.
- **Schema** — drf-spectacular OpenAPI + Swagger UI.
- **Pagination** — cursor pagination for large/append-heavy datasets.
- **Errors** — single custom exception handler → consistent envelope.
- **Testing** — `APITestCase` with `force_authenticate`.

## Conventions
- Plural, lowercase resource names; version in the URL path.
- 201 on create, 204 on delete, 400 with field errors on validation.
```
