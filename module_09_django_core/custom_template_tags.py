"""Custom template tags and filters.

Docs: https://docs.djangoproject.com/en/stable/howto/custom-template-tags/
Place in <app>/templatetags/myapp_extras.py (the folder needs __init__.py).
"""
from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def currency(value, symbol="$"):
    """Usage: {{ price|currency:'EUR ' }}"""
    return f"{symbol}{value:,.2f}"


@register.simple_tag
def now_year():
    """Usage: {% now_year %}"""
    return timezone.now().year


@register.inclusion_tag("myapp/_card.html")
def render_card(title, body):
    """Usage: {% render_card "Hi" "Body" %} -> renders _card.html"""
    return {"title": title, "body": body}


# Template usage:
#   {% load myapp_extras %}
#   {{ product.price|currency }}
#   (c) {% now_year %}