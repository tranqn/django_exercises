from django import template

register = template.Library()


@register.inclusion_tag("components/pagination.html")
def show_pagination(page_obj):
    """Render pagination controls for a paginated view."""
    return {"page_obj": page_obj}