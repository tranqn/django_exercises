# Week 23 — GraphQL APIs with Strawberry

## Commit #336
**Message:** `feat(graphql): add Strawberry schema and Django view`
**Files:**

```file:advanced/graphql_api/schema.py
"""
GraphQL with strawberry-graphql.

pip install strawberry-graphql[django]
urls: path("graphql/", AsyncGraphQLView.as_view(schema=schema))
"""

import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"


schema = strawberry.Schema(query=Query)
```

---

## Commit #337
**Message:** `feat(graphql): add query resolvers for articles`
**Files:**

```file:advanced/graphql_api/queries.py
"""Typed queries returning Django model data."""

from typing import List

import strawberry


@strawberry.type
class ArticleType:
    id: strawberry.ID
    title: str
    summary: str


@strawberry.type
class Query:
    @strawberry.field
    def articles(self, limit: int = 20) -> List[ArticleType]:
        from articles.models import Article
        return list(Article.objects.published()[:limit])

    @strawberry.field
    def article(self, id: strawberry.ID) -> ArticleType | None:
        from articles.models import Article
        return Article.objects.filter(pk=id).first()
```

---

## Commit #338
**Message:** `feat(graphql): add mutations`
**Files:**

```file:advanced/graphql_api/mutations.py
"""Create/update mutations with input types."""

import strawberry


@strawberry.input
class CreateArticleInput:
    title: str
    body: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_article(self, data: CreateArticleInput) -> strawberry.ID:
        from articles.models import Article
        article = Article.objects.create(title=data.title, body=data.body)
        return strawberry.ID(str(article.pk))
```

---

## Commit #339
**Message:** `perf(graphql): add DataLoader to fix N+1`
**Files:**

```file:advanced/graphql_api/dataloaders.py
"""Batch related lookups within a single request."""

from collections import defaultdict

from strawberry.dataloader import DataLoader


async def batch_authors(keys):
    from accounts.models import User
    users = {u.id: u async for u in User.objects.filter(id__in=keys)}
    return [users.get(k) for k in keys]


def make_author_loader():
    return DataLoader(load_fn=batch_authors)
```

---

## Commit #340
**Message:** `feat(graphql): add Relay-style cursor pagination`
**Files:**

```file:advanced/graphql_api/pagination.py
"""Relay connection pagination helpers."""

import base64
from typing import List

import strawberry


def encode_cursor(offset: int) -> str:
    return base64.b64encode(f"cursor:{offset}".encode()).decode()


def decode_cursor(cursor: str) -> int:
    return int(base64.b64decode(cursor).decode().split(":")[1])


@strawberry.type
class PageInfo:
    has_next_page: bool
    end_cursor: str | None
```

---

## Commit #341
**Message:** `feat(graphql): add authentication permission`
**Files:**

```file:advanced/graphql_api/permissions.py
"""Field-level auth via a Strawberry permission class."""

import typing

import strawberry
from strawberry.permission import BasePermission


class IsAuthenticated(BasePermission):
    message = "Authentication required"

    def has_permission(self, source, info, **kwargs) -> bool:
        request = info.context["request"]
        return request.user.is_authenticated


@strawberry.type
class SecureQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self) -> str:
        return "current user"
```

---

## Commit #342
**Message:** `feat(graphql): add subscriptions over websockets`
**Files:**

```file:advanced/graphql_api/subscriptions.py
"""Real-time subscriptions (requires an ASGI server)."""

import asyncio
from typing import AsyncGenerator

import strawberry


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 5) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(1)
```

---

## Commit #343
**Message:** `feat(graphql): add typed error handling`
**Files:**

```file:advanced/graphql_api/errors.py
"""Return errors as part of the typed schema (union results)."""

import strawberry


@strawberry.type
class ValidationError:
    field: str
    message: str


@strawberry.type
class ArticleSuccess:
    id: strawberry.ID


Result = strawberry.union("ArticleResult", (ArticleSuccess, ValidationError))
```

---

## Commit #344
**Message:** `feat(graphql): add file upload scalar`
**Files:**

```file:advanced/graphql_api/uploads.py
"""Handle multipart file uploads in mutations."""

import strawberry
from strawberry.file_uploads import Upload


@strawberry.type
class UploadMutation:
    @strawberry.mutation
    def upload_avatar(self, file: Upload) -> str:
        content = file.read()
        # store content via default storage...
        return f"received {len(content)} bytes"
```

---

## Commit #345
**Message:** `feat(graphql): add query complexity/depth limiting`
**Files:**

```file:advanced/graphql_api/complexity.py
"""Reject overly deep/expensive queries to prevent abuse."""

from strawberry.extensions import QueryDepthLimiter, MaxTokensLimiter

EXTENSIONS = [
    QueryDepthLimiter(max_depth=10),
    MaxTokensLimiter(max_token_count=2000),
]

# schema = strawberry.Schema(query=Query, extensions=EXTENSIONS)
```

---

## Commit #346
**Message:** `test(graphql): add schema execution tests`
**Files:**

```file:advanced/graphql_api/test_schema.py
"""Execute queries against the schema directly."""

from django.test import TestCase

from .schema import schema


class SchemaTests(TestCase):
    def test_ping(self):
        result = schema.execute_sync("{ ping }")
        self.assertIsNone(result.errors)
        self.assertEqual(result.data["ping"], "pong")
```

---

## Commit #347
**Message:** `docs(week23): add GraphQL reference`
**Files:**

```file:advanced/GRAPHQL_REFERENCE.md
# Week 23 — GraphQL APIs with Strawberry

- **Schema** — typed Query/Mutation/Subscription with `@strawberry`.
- **Performance** — DataLoaders batch related lookups (kill N+1).
- **Pagination** — Relay cursor connections.
- **Security** — permission classes, depth + token limits.
- **Realtime** — websocket subscriptions (ASGI).
- **Errors** — model as union result types, not exceptions.
- **Uploads** — multipart `Upload` scalar.

## REST vs GraphQL
- GraphQL shines for varied client shapes and graph-like data.
- Keep DRF for simple CRUD, webhooks and file-heavy endpoints.
```
