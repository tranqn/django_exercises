from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, url_name):
    """Return 'active' CSS class if current URL matches url_name."""
    request = context["request"]
    try:
        current = resolve(request.path_info).url_name
        return "active" if current == url_name else ""
    except Exception:
        return ""