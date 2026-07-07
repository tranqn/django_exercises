"""Aggregation and annotation.

Docs: https://docs.djangoproject.com/en/stable/topics/db/aggregation/
"""
from django.db.models import Count, Avg, Sum, Max, F


def examples():
    from myapp.models import Book, Author

    # aggregate() -> a dict computed over the whole queryset:
    Book.objects.aggregate(Avg("price"), Max("price"), total=Sum("price"))

    # annotate() -> add a per-row computed field:
    authors = Author.objects.annotate(num_books=Count("book"))
    for a in authors:
        print(a.name, a.num_books)

    # Filter on an annotation:
    prolific = Author.objects.annotate(n=Count("book")).filter(n__gte=5)

    # GROUP BY via values().annotate():
    Book.objects.values("genre").annotate(avg_price=Avg("price"))

    # F() references a column in the DB (no Python round-trip):
    Book.objects.update(price=F("price") * 1.1)

    return prolific