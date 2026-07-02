"""Query optimization helpers — find and kill N+1 queries.

Rules of thumb:
- select_related for forward FK / OneToOne (SQL JOIN).
- prefetch_related for reverse FK / ManyToMany (second query).
- .only()/.defer() to trim columns on wide tables.
- db_index=True (or Meta.indexes) for frequent filter/order fields.
"""
from contextlib import contextmanager
from django.db import connection, reset_queries


@contextmanager
def assert_max_queries(limit):
    """Fail loudly if a block runs more queries than expected.

        with assert_max_queries(2):
            list(Book.objects.select_related("author"))
    """
    reset_queries()
    yield
    executed = len(connection.queries)
    if executed > limit:
        raise AssertionError(f"{executed} queries ran, expected <= {limit}")


def explain(queryset):
    """Return the database EXPLAIN ANALYZE plan for a queryset."""
    return queryset.explain(analyze=True)


# Example optimized access pattern:
# books = (
#     Book.objects.select_related("author")
#     .prefetch_related("tags")
#     .only("title", "author__name")
# )