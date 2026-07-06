"""The sites framework — manage multiple sites from one database.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/sites/
"""
from django.contrib.sites.models import Site


def current_site_info(request):
    # Uses SITE_ID, or resolves from the request's Host header.
    site = Site.objects.get_current(request)
    return {"domain": site.domain, "name": site.name}


# Associate model rows with one or more sites:
#   class Article(models.Model):
#       title = models.CharField(max_length=200)
#       sites = models.ManyToManyField(Site)
#
#   # Only this site's articles:
#   Article.objects.filter(sites__id=settings.SITE_ID)

# settings.py:
#   INSTALLED_APPS += ["django.contrib.sites"]
#   SITE_ID = 1
# CurrentSiteManager auto-filters a model by the active site:
#   from django.contrib.sites.managers import CurrentSiteManager
#   on_site = CurrentSiteManager()