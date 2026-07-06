"""XML sitemaps with django.contrib.sitemaps.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/sitemaps/
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        from myapp.models import Article
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("article-detail", args=[obj.pk])


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["home", "about", "contact"]

    def location(self, item):
        return reverse(item)


# urls.py:
#   from django.contrib.sitemaps.views import sitemap
#   sitemaps = {"articles": ArticleSitemap, "static": StaticViewSitemap}
#   path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap")
# INSTALLED_APPS += ["django.contrib.sitemaps", "django.contrib.sites"]