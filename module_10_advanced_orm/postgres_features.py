"""PostgreSQL-specific features (django.contrib.postgres).

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/postgres/
Needs the postgresql backend + 'django.contrib.postgres' in INSTALLED_APPS.
"""
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=30), blank=True, default=list)
    specs = models.JSONField(default=dict)

    class Meta:
        indexes = [GinIndex(fields=["tags"])]


def full_text_search(term):
    # Weighted full-text search, ranked by relevance:
    vector = SearchVector("name", weight="A") + SearchVector("description", weight="B")
    query = SearchQuery(term)
    return (
        Product.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gte=0.1)
        .order_by("-rank")
    )


# Array / JSON lookups:
#   Product.objects.filter(tags__contains=["sale"])
#   Product.objects.filter(specs__color="red")