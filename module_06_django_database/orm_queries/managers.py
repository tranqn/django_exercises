"""
Custom Model Managers — Reusable query logic.
"""

from django.db import models


class PublishedManager(models.Manager):
    """Manager that only returns published books."""

    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class BookQuerySet(models.QuerySet):
    """Custom QuerySet with chainable methods."""

    def published(self):
        return self.filter(status="published")

    def by_author(self, author_name):
        return self.filter(author__last_name__icontains=author_name)

    def long_books(self, min_pages=300):
        return self.filter(pages__gte=min_pages)

    def with_reviews(self):
        return self.annotate(review_count=models.Count("reviews")).filter(review_count__gt=0)


# Usage in Model:
# class Book(models.Model):
#     objects = BookQuerySet.as_manager()
#     published = PublishedManager()
#
# Book.objects.published().long_books(500)
# Book.published.all()  # Only published books