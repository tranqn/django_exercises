# Week 17 — Frontend Integration: Templates, HTMX & Static Assets

## Commit #264
**Message:** `feat(frontend): add base template with reusable blocks`
**Files:**

```file:advanced/frontend_integration/base.html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}MySite{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/app.css' %}">
  <script src="https://unpkg.com/htmx.org@2"></script>
</head>
<body>
  {% include "partials/_nav.html" %}
  <main>{% block content %}{% endblock %}</main>
  {% block scripts %}{% endblock %}
</body>
</html>
```

---

## Commit #265
**Message:** `feat(frontend): add HTMX partial update view`
**Files:**

```file:advanced/frontend_integration/htmx_views.py
"""Return a partial template for HTMX requests, full page otherwise."""

from django.shortcuts import render


def toggle_like(request, pk):
    liked = request.POST.get("liked") != "true"
    # ... persist like state ...
    return render(request, "partials/_like_button.html",
                  {"pk": pk, "liked": liked})


def article_list(request):
    template = "partials/_articles.html" if request.htmx else "articles.html"
    return render(request, template, {"articles": []})
```

---

## Commit #266
**Message:** `feat(frontend): add crispy form rendering`
**Files:**

```file:advanced/frontend_integration/forms.py
"""Bootstrap-styled forms with crispy-forms.

pip install crispy-bootstrap5 django-crispy-forms
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Send"))
```

---

## Commit #267
**Message:** `feat(frontend): add WhiteNoise static files pipeline`
**Files:**

```file:advanced/frontend_integration/static_settings.py
"""
Serve hashed, compressed static files straight from Django.

pip install whitenoise
Add 'whitenoise.middleware.WhiteNoiseMiddleware' right after SecurityMiddleware.
"""

STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = ["assets"]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

---

## Commit #268
**Message:** `feat(frontend): add custom template tags and filters`
**Files:**

```file:advanced/frontend_integration/templatetags.py
"""Place under <app>/templatetags/app_extras.py."""

from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def humanize_age(value):
    return f"{timesince(value)} ago"


@register.simple_tag(takes_context=True)
def active(context, url_name):
    return "active" if context["request"].resolver_match.url_name == url_name else ""
```

---

## Commit #269
**Message:** `feat(frontend): add context processors for globals`
**Files:**

```file:advanced/frontend_integration/context_processors.py
"""Inject site-wide values into every template.

settings: TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'advanced.frontend_integration.context_processors.site_globals'
]
"""

from django.conf import settings


def site_globals(request):
    return {
        "SITE_NAME": "MySite",
        "SUPPORT_EMAIL": "support@example.com",
        "DEBUG": settings.DEBUG,
        "unread_count": getattr(request.user, "unread_count", 0),
    }
```

---

## Commit #270
**Message:** `feat(frontend): add reusable pagination partial`
**Files:**

```file:advanced/frontend_integration/_pagination.html
{% if page_obj.has_other_pages %}
<nav class="pagination" aria-label="Pagination">
  {% if page_obj.has_previous %}
    <a href="?page={{ page_obj.previous_page_number }}">&laquo; Prev</a>
  {% endif %}
  <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
  {% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">Next &raquo;</a>
  {% endif %}
</nav>
{% endif %}
```

---

## Commit #271
**Message:** `feat(frontend): add HTMX infinite scroll`
**Files:**

```file:advanced/frontend_integration/_infinite_scroll.html
{% for item in items %}
  <article>{{ item.title }}</article>
{% endfor %}

{% if page_obj.has_next %}
  <div hx-get="?page={{ page_obj.next_page_number }}"
       hx-trigger="revealed"
       hx-swap="outerHTML">
    <span class="loading">Loading more…</span>
  </div>
{% endif %}
```

---

## Commit #272
**Message:** `feat(frontend): add Alpine.js dropdown component`
**Files:**

```file:advanced/frontend_integration/_dropdown.html
<div x-data="{ open: false }" class="dropdown">
  <button @click="open = !open" :aria-expanded="open">
    Menu
  </button>
  <ul x-show="open" @click.outside="open = false" x-transition>
    <li><a href="/profile/">Profile</a></li>
    <li><a href="/settings/">Settings</a></li>
    <li><a href="/logout/">Logout</a></li>
  </ul>
</div>
<script src="https://unpkg.com/alpinejs@3" defer></script>
```

---

## Commit #273
**Message:** `feat(frontend): add server-sent events for live updates`
**Files:**

```file:advanced/frontend_integration/sse_view.py
"""Stream live updates over SSE (no WebSocket needed for one-way data)."""

import json
import time

from django.http import StreamingHttpResponse


def event_stream():
    while True:
        payload = {"ts": time.time(), "online": 42}
        yield f"data: {json.dumps(payload)}\n\n"
        time.sleep(5)


def notifications(request):
    resp = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    resp["Cache-Control"] = "no-cache"
    return resp
```

---

## Commit #274
**Message:** `feat(frontend): add client-side validation hints`
**Files:**

```file:advanced/frontend_integration/_validated_form.html
<form hx-post="/contact/" hx-target="#result" novalidate>
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required
         aria-describedby="email-help">
  <small id="email-help">We'll never share your email.</small>

  <label for="msg">Message</label>
  <textarea id="msg" name="message" required minlength="10"></textarea>

  <button type="submit">Send</button>
  <div id="result" role="status" aria-live="polite"></div>
</form>
```

---

## Commit #275
**Message:** `docs(week17): add frontend integration notes`
**Files:**

```file:advanced/FRONTEND_REFERENCE.md
# Week 17 — Frontend Integration

- **Templates** — base layout with blocks, reusable partials/includes.
- **HTMX** — partial swaps, infinite scroll, `request.htmx` branching.
- **Alpine.js** — light client-side interactivity (dropdowns, toggles).
- **SSE** — one-way live updates without a WebSocket.
- **Forms** — crispy-forms styling + native + ARIA validation hints.
- **Static** — WhiteNoise compressed manifest storage; `collectstatic`.
- **Reuse** — custom template tags/filters and context processors.

## Tips
- Keep partials in `templates/partials/` and prefix with `_`.
- Use `hx-trigger="revealed"` for infinite scroll, `hx-target` for swaps.
```
