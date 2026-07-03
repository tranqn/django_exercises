"""Syndication feeds — RSS/Atom with the syndication framework.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/syndication/
"""
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed


class LatestArticlesFeed(Feed):
    title = "My Blog"
    link = "/articles/"
    description = "Latest articles from the blog."

    def items(self):
        from myapp.models import Article
        return Article.objects.order_by("-pub_date")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return reverse("article-detail", args=[item.pk])


class AtomArticlesFeed(LatestArticlesFeed):
    feed_type = Atom1Feed
    subtitle = LatestArticlesFeed.description


# urls.py:
#   path("feed/rss/", LatestArticlesFeed()),
#   path("feed/atom/", AtomArticlesFeed()),