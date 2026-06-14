# Week 21 — Internationalization, Content & SEO

## Commit #312
**Message:** `feat(i18n): add translation configuration`
**Files:**

```file:advanced/i18n_content/i18n_settings.py
"""Enable Django i18n. Run makemessages/compilemessages to build catalogs."""

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("de", "Deutsch"),
    ("vi", "Tiếng Việt"),
]
LOCALE_PATHS = ["locale"]
```

---

## Commit #313
**Message:** `feat(i18n): add locale middleware and language switcher`
**Files:**

```file:advanced/i18n_content/language_switch.py
"""Persist the chosen language via Django's set_language view.

MIDDLEWARE must include 'django.middleware.locale.LocaleMiddleware'
after SessionMiddleware and before CommonMiddleware.
"""

from django.urls import path
from django.views.i18n import set_language

urlpatterns = [
    path("i18n/setlang/", set_language, name="set_language"),
]

# Template:
# {% load i18n %}
# {% get_current_language as LANG %}
# <form action="{% url 'set_language' %}" method="post">...</form>
```

---

## Commit #314
**Message:** `feat(i18n): add timezone-aware datetime helpers`
**Files:**

```file:advanced/i18n_content/timezones.py
"""Activate the user's timezone per request."""

from zoneinfo import ZoneInfo

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = getattr(getattr(request, "user", None), "timezone", None)
        if tzname:
            timezone.activate(ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
```

---

## Commit #315
**Message:** `feat(content): add flatpages-style CMS model`
**Files:**

```file:advanced/i18n_content/pages.py
"""Editable static pages stored in the DB."""

from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

---

## Commit #316
**Message:** `feat(content): add safe markdown rendering`
**Files:**

```file:advanced/i18n_content/markdown_render.py
"""Render user markdown to sanitized HTML.

pip install markdown bleach
"""

import bleach
import markdown

ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "ol", "li",
                "a", "code", "pre", "blockquote", "h2", "h3"]
ALLOWED_ATTRS = {"a": ["href", "title", "rel"]}


def render_markdown(text):
    html = markdown.markdown(text, extensions=["fenced_code"])
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
```

---

## Commit #317
**Message:** `feat(content): add tagging system`
**Files:**

```file:advanced/i18n_content/tagging.py
"""Reusable tags with a through model for counts."""

from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="items")
    object_id = models.PositiveIntegerField()
```

---

## Commit #318
**Message:** `feat(content): add comment moderation queue`
**Files:**

```file:advanced/i18n_content/moderation.py
"""Hold comments for review based on simple heuristics."""

import re

LINK_RE = re.compile(r"https?://", re.I)
BANNED = {"casino", "viagra"}


def needs_moderation(text):
    lowered = text.lower()
    if len(LINK_RE.findall(text)) > 2:
        return True
    return any(word in lowered for word in BANNED)


class CommentState:
    PENDING, APPROVED, REJECTED = "pending", "approved", "rejected"
```

---

## Commit #319
**Message:** `feat(content): add sitemap generation`
**Files:**

```file:advanced/i18n_content/sitemaps.py
"""XML sitemaps via django.contrib.sitemaps."""

from django.contrib.sitemaps import Sitemap


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        from .pages import Page
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

# urls.py:
# path("sitemap.xml", sitemap, {"sitemaps": {"pages": PageSitemap}})
```

---

## Commit #320
**Message:** `feat(content): add RSS feed`
**Files:**

```file:advanced/i18n_content/feeds.py
"""Syndication feed with django.contrib.syndication."""

from django.contrib.syndication.views import Feed


class LatestArticlesFeed(Feed):
    title = "MySite — Latest Articles"
    link = "/feed/"
    description = "Newest published articles"

    def items(self):
        from articles.models import Article
        return Article.objects.filter(status="published").order_by("-published_at")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary
```

---

## Commit #321
**Message:** `feat(seo): add meta tags and Open Graph block`
**Files:**

```file:advanced/i18n_content/_seo_meta.html
{% load static %}
<meta name="description" content="{{ meta_description|default:'MySite' }}">
<link rel="canonical" href="{{ request.build_absolute_uri }}">

<meta property="og:title" content="{{ meta_title|default:title }}">
<meta property="og:description" content="{{ meta_description }}">
<meta property="og:type" content="{{ og_type|default:'website' }}">
<meta property="og:image" content="{{ og_image|default:'/static/og-default.png' }}">
<meta name="twitter:card" content="summary_large_image">
```

---

## Commit #322
**Message:** `feat(seo): add robots.txt view`
**Files:**

```file:advanced/i18n_content/robots.py
"""Serve robots.txt with environment-aware rules."""

from django.conf import settings
from django.http import HttpResponse


def robots_txt(request):
    if settings.DEBUG:
        lines = ["User-agent: *", "Disallow: /"]
    else:
        lines = ["User-agent: *", "Disallow: /admin/", "Allow: /",
                 f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"]
    return HttpResponse("\n".join(lines), content_type="text/plain")
```

---

## Commit #323
**Message:** `docs(week21): add i18n and content reference`
**Files:**

```file:advanced/I18N_CONTENT_REFERENCE.md
# Week 21 — Internationalization, Content & SEO

- **i18n/l10n** — language list, locale middleware, switcher, per-user TZ.
- **Content** — DB-backed pages, safe markdown (bleach), tagging,
  comment moderation queue.
- **SEO** — sitemaps, RSS feed, canonical + Open Graph meta, robots.txt.

## Workflow
- `makemessages -l de` → translate `.po` → `compilemessages`.
- Wrap UI strings in `{% trans %}` / `gettext`.
- Always sanitize user HTML; never trust markdown output raw.
```
