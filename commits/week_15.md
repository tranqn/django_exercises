# Week 15 — Advanced ORM & Database Patterns

## Commit #240
**Message:** `feat(orm): add custom model managers and querysets`
**Files:**

```file:advanced/orm_patterns/managers.py
"""Chainable custom QuerySet + Manager."""

from django.db import models
from django.utils import timezone


class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published", published_at__lte=timezone.now())

    def by_author(self, user):
        return self.filter(author=user)


class ArticleManager(models.Manager.from_queryset(ArticleQuerySet)):
    """Use as: objects = ArticleManager()."""
    pass
```

---

## Commit #241
**Message:** `feat(orm): add aggregation and annotation reports`
**Files:**

```file:advanced/orm_patterns/aggregations.py
"""Reporting queries with annotate/aggregate."""

from django.db.models import Count, Avg, Sum, Max


def author_stats(qs):
    return qs.values("author__username").annotate(
        articles=Count("id"),
        avg_words=Avg("word_count"),
        total_views=Sum("views"),
        last_post=Max("published_at"),
    ).order_by("-articles")
```

---

## Commit #242
**Message:** `feat(orm): add F() and Q() expressions for atomic updates`
**Files:**

```file:advanced/orm_patterns/expressions.py
"""Atomic field updates and complex lookups."""

from django.db.models import F, Q


def increment_views(qs, pk):
    # Atomic at the DB level — no read-modify-write race.
    qs.filter(pk=pk).update(views=F("views") + 1)


def search(qs, term):
    return qs.filter(
        Q(title__icontains=term) | Q(body__icontains=term),
        ~Q(status="draft"),
    )
```

---

## Commit #243
**Message:** `feat(orm): add bulk_create and bulk_update helpers`
**Files:**

```file:advanced/orm_patterns/bulk_ops.py
"""Batched writes to avoid per-row round trips."""


def bulk_import(model, rows, batch_size=500):
    objs = [model(**r) for r in rows]
    return model.objects.bulk_create(objs, batch_size=batch_size)


def bulk_touch(model, objs, fields, batch_size=500):
    model.objects.bulk_update(objs, fields, batch_size=batch_size)
```

---

## Commit #244
**Message:** `feat(orm): add transactions and select_for_update locking`
**Files:**

```file:advanced/orm_patterns/transactions.py
"""Transactional money transfer with row locking."""

from django.db import transaction


@transaction.atomic
def transfer(Account, from_id, to_id, amount):
    accounts = (
        Account.objects.select_for_update()
        .filter(pk__in=[from_id, to_id])
    )
    a = {acc.pk: acc for acc in accounts}
    if a[from_id].balance < amount:
        raise ValueError("insufficient funds")
    a[from_id].balance -= amount
    a[to_id].balance += amount
    Account.objects.bulk_update(a.values(), ["balance"])
```

---

## Commit #245
**Message:** `feat(orm): add Case/When conditional expressions`
**Files:**

```file:advanced/orm_patterns/conditionals.py
"""Conditional aggregation with Case/When."""

from django.db.models import Case, When, Value, IntegerField, Count


def status_breakdown(qs):
    return qs.aggregate(
        drafts=Count(Case(When(status="draft", then=Value(1)))),
        live=Count(Case(When(status="published", then=Value(1)))),
    )


def priority_order(qs):
    return qs.annotate(
        rank=Case(
            When(priority="high", then=Value(0)),
            When(priority="medium", then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by("rank")
```

---

## Commit #246
**Message:** `feat(orm): add window functions for ranking`
**Files:**

```file:advanced/orm_patterns/window_functions.py
"""Per-group ranking without subqueries."""

from django.db.models import F, Window
from django.db.models.functions import Rank, Lag


def rank_within_category(qs):
    return qs.annotate(
        rank=Window(
            expression=Rank(),
            partition_by=[F("category")],
            order_by=F("views").desc(),
        ),
        prev_views=Window(
            expression=Lag("views"),
            partition_by=[F("category")],
            order_by=F("published_at").asc(),
        ),
    )
```

---

## Commit #247
**Message:** `feat(orm): add generic relations for an activity feed`
**Files:**

```file:advanced/orm_patterns/generic_relations.py
"""Activity feed referencing any model via GenericForeignKey."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Activity(models.Model):
    actor = models.CharField(max_length=150)
    verb = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## Commit #248
**Message:** `feat(orm): add soft-delete mixin with manager`
**Files:**

```file:advanced/orm_patterns/soft_delete.py
"""Soft delete: hide rows instead of removing them."""

from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def alive(self):
        return self.filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])
```

---

## Commit #249
**Message:** `feat(orm): add database view via raw SQL migration`
**Files:**

```file:advanced/orm_patterns/db_view_migration.py
"""RunSQL migration creating a read-only reporting view."""

from django.db import migrations

SQL = """
CREATE VIEW author_summary AS
SELECT author_id, COUNT(*) AS article_count, SUM(views) AS total_views
FROM articles_article
GROUP BY author_id;
"""


class Migration(migrations.Migration):
    dependencies = [("articles", "0001_initial")]
    operations = [
        migrations.RunSQL(SQL, reverse_sql="DROP VIEW author_summary;")
    ]
```

---

## Commit #250
**Message:** `perf(orm): add filtered prefetch with Prefetch objects`
**Files:**

```file:advanced/orm_patterns/prefetch.py
"""Prefetch only the related rows you need."""

from django.db.models import Prefetch


def authors_with_recent_articles(Author, Article):
    recent = Article.objects.filter(status="published").order_by("-published_at")
    return Author.objects.prefetch_related(
        Prefetch("articles", queryset=recent, to_attr="recent_articles")
    )
```

---

## Commit #251
**Message:** `docs(week15): add advanced ORM patterns reference`
**Files:**

```file:advanced/ORM_REFERENCE.md
# Week 15 — Advanced ORM & Database Patterns

- **Managers/QuerySets** — chainable, reusable query logic (`.published()`).
- **Aggregation** — `annotate`/`aggregate` for reports.
- **F()/Q()** — atomic updates and complex boolean lookups.
- **Bulk ops** — `bulk_create`/`bulk_update` to cut round trips.
- **Transactions** — `atomic` + `select_for_update` for safe money moves.
- **Case/When** — conditional aggregation and ordering.
- **Window functions** — per-group ranking (`Rank`, `Lag`).
- **Generic relations** — polymorphic activity feed.
- **Soft delete** — abstract mixin overriding `delete()`.
- **DB views** — `RunSQL` migrations for reporting.
- **Prefetch** — filtered related fetches via `Prefetch(to_attr=...)`.
```
