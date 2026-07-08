"""Custom managers and QuerySets.

Docs: https://docs.djangoproject.com/en/stable/topics/db/managers/
Encapsulate reusable query logic instead of repeating .filter() chains.
"""
from django.db import models


class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published")

    def by_author(self, author):
        return self.filter(author=author)


class Article(models.Model):
    status = models.CharField(max_length=20, default="draft")

    objects = models.Manager()                            # default manager
    items = ArticleQuerySet.as_manager()                  # chainable manager


# Chainable on both the manager and the queryset:
#   Article.items.published().by_author(me)