# Django ORM Cheatsheet

## Lookup Types
| Lookup | SQL | Example |
|---|---|---|
| `exact` | `= value` | `title__exact="Django"` |
| `iexact` | `ILIKE value` | `title__iexact="django"` |
| `contains` | `LIKE %val%` | `title__contains="Dj"` |
| `icontains` | `ILIKE %val%` | `title__icontains="dj"` |
| `startswith` | `LIKE val%` | `title__startswith="Dj"` |
| `endswith` | `LIKE %val` | `title__endswith="go"` |
| `gt / gte` | `> / >=` | `pages__gt=300` |
| `lt / lte` | `< / <=` | `pages__lt=100` |
| `in` | `IN (...)` | `id__in=[1,2,3]` |
| `range` | `BETWEEN` | `pages__range=(100,500)` |
| `isnull` | `IS NULL` | `author__isnull=True` |
| `year/month/day` | date parts | `pub_date__year=2026` |
| `regex` | `REGEXP` | `title__regex=r'^Dj'` |

## QuerySet API
| Method | Returns | SQL |
|---|---|---|
| `.all()` | QuerySet | `SELECT *` |
| `.filter()` | QuerySet | `WHERE` |
| `.exclude()` | QuerySet | `WHERE NOT` |
| `.get()` | Object | `WHERE ... LIMIT 1` |
| `.first()` | Object/None | `ORDER BY ... LIMIT 1` |
| `.count()` | int | `COUNT(*)` |
| `.exists()` | bool | `EXISTS` |
| `.values()` | list[dict] | `SELECT col1, col2` |
| `.annotate()` | QuerySet | `SELECT ..., computed` |
| `.aggregate()` | dict | `SELECT AGG(...)` |
| `.order_by()` | QuerySet | `ORDER BY` |
| `.distinct()` | QuerySet | `DISTINCT` |
| `.select_related()` | QuerySet | `JOIN` |
| `.prefetch_related()` | QuerySet | separate query |