# Week 26 — Testing Mastery

## Commit #372
**Message:** `test(factories): add model factories with traits`
**Files:**

```file:advanced/testing_mastery/factories.py
"""factory_boy factories with reusable traits."""

import factory

from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")

    class Params:
        admin = factory.Trait(is_staff=True, is_superuser=True)
```

---

## Commit #373
**Message:** `test(fixtures): add reusable pytest fixtures`
**Files:**

```file:advanced/testing_mastery/conftest.py
"""Shared fixtures: api client, authed client, frozen time."""

import pytest
from rest_framework.test import APIClient

from .factories import UserFactory


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def authed_api(api):
    user = UserFactory()
    api.force_authenticate(user)
    return api, user
```

---

## Commit #374
**Message:** `test(property): add Hypothesis property-based tests`
**Files:**

```file:advanced/testing_mastery/test_property.py
"""Property-based testing with Hypothesis.

pip install hypothesis
"""

from hypothesis import given, strategies as st

from advanced.orm_patterns.expressions import search


@given(st.text(min_size=1, max_size=20))
def test_search_never_crashes(term):
    # Roundtrip the query-building logic on arbitrary input.
    class FakeQS:
        def filter(self, *a, **k):
            return self
    assert search(FakeQS(), term) is not None
```

---

## Commit #375
**Message:** `test(parametrize): add parametrized edge-case tests`
**Files:**

```file:advanced/testing_mastery/test_parametrized.py
"""Table-driven tests for a price formatter."""

import pytest


def format_price(cents):
    return f"${cents / 100:.2f}"


@pytest.mark.parametrize("cents,expected", [
    (0, "$0.00"),
    (5, "$0.05"),
    (199, "$1.99"),
    (100000, "$1000.00"),
])
def test_format_price(cents, expected):
    assert format_price(cents) == expected
```

---

## Commit #376
**Message:** `test(mock): add tests with mocked external services`
**Files:**

```file:advanced/testing_mastery/test_mocking.py
"""Isolate code from network calls with unittest.mock."""

from unittest.mock import patch

from django.test import SimpleTestCase


class PaymentTests(SimpleTestCase):
    @patch("advanced.payments_integrations.stripe_checkout.stripe")
    def test_checkout_calls_stripe(self, mock_stripe):
        from advanced.payments_integrations.stripe_checkout import (
            create_checkout_session,
        )
        create_checkout_session("price_1", "a@b.c", "/ok", "/no")
        mock_stripe.checkout.Session.create.assert_called_once()
```

---

## Commit #377
**Message:** `test(snapshot): add response snapshot tests`
**Files:**

```file:advanced/testing_mastery/test_snapshot.py
"""Snapshot-style assertion on a serialized payload."""

import json

from django.test import SimpleTestCase


def serialize_article(a):
    return {"id": a["id"], "title": a["title"], "tags": sorted(a["tags"])}


class SnapshotTests(SimpleTestCase):
    def test_article_shape_is_stable(self):
        out = serialize_article({"id": 1, "title": "Hi", "tags": ["b", "a"]})
        expected = '{"id": 1, "title": "Hi", "tags": ["a", "b"]}'
        self.assertEqual(json.dumps(out), expected)
```

---

## Commit #378
**Message:** `test(db): add transactional and constraint tests`
**Files:**

```file:advanced/testing_mastery/test_db_constraints.py
"""Verify DB-level constraints actually fire."""

from django.db import IntegrityError, transaction
from django.test import TestCase

from .factories import UserFactory


class ConstraintTests(TestCase):
    def test_duplicate_username_rejected(self):
        UserFactory(username="dup")
        with self.assertRaises(IntegrityError), transaction.atomic():
            UserFactory(username="dup")
```

---

## Commit #379
**Message:** `test(coverage): add coverage configuration`
**Files:**

```file:advanced/testing_mastery/.coveragerc
[run]
branch = True
source = .
omit =
    */migrations/*
    */tests/*
    */venv/*
    manage.py

[report]
show_missing = True
skip_covered = True
fail_under = 85
```

---

## Commit #380
**Message:** `test(perf): add query count regression assertions`
**Files:**

```file:advanced/testing_mastery/test_query_count.py
"""Guard against N+1 regressions with assertNumQueries."""

from django.test import TestCase

from .factories import UserFactory


class QueryCountTests(TestCase):
    def test_list_uses_constant_queries(self):
        for _ in range(5):
            UserFactory()
        from django.contrib.auth import get_user_model
        with self.assertNumQueries(1):
            list(get_user_model().objects.all())
```

---

## Commit #381
**Message:** `test(contract): add API schema contract test`
**Files:**

```file:advanced/testing_mastery/test_contract.py
"""Fail the build if the OpenAPI schema can't be generated/validated."""

from django.test import TestCase
from django.core.management import call_command


class ContractTests(TestCase):
    def test_openapi_schema_generates(self):
        # drf-spectacular's command exits non-zero on schema errors.
        try:
            call_command("spectacular", "--validate", "--fail-on-warn")
        except SystemExit as exc:
            self.assertEqual(exc.code, 0)
```

---

## Commit #382
**Message:** `test(ci): add tox multi-version configuration`
**Files:**

```file:advanced/testing_mastery/tox.ini
[tox]
envlist = py311, py312, lint

[testenv]
deps = -r requirements-dev.txt
commands = pytest --cov --cov-report=term-missing

[testenv:lint]
deps = ruff
commands =
    ruff check .
    ruff format --check .
```

---

## Commit #383
**Message:** `docs(week26): add testing strategy reference`
**Files:**

```file:advanced/TESTING_REFERENCE.md
# Week 26 — Testing Mastery

- **Data** — factory_boy factories with traits; shared pytest fixtures.
- **Techniques** — parametrized tables, Hypothesis property tests,
  mocking external services, snapshot assertions.
- **Database** — constraint tests, `assertNumQueries` N+1 guards.
- **Quality gates** — coverage (`fail_under`), OpenAPI contract test,
  tox across Python versions.

## The pyramid
- Many fast unit tests, fewer integration tests, a thin E2E layer.
- Test behavior and contracts, not implementation details.
- Every bug fix ships with a regression test.
```
