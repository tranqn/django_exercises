"""Complex lookups with Q objects.

Docs: https://docs.djangoproject.com/en/stable/topics/db/queries/
"""
from django.db.models import Q


def search(term, include_drafts=False):
    from myapp.models import Article

    # OR across fields:
    qs = Article.objects.filter(
        Q(title__icontains=term) | Q(body__icontains=term)
    )
    # AND + negation:
    if not include_drafts:
        qs = qs.filter(~Q(status="draft"))
    return qs


def dynamic_filters(filters: dict):
    from myapp.models import Article
    q = Q()
    for field, value in filters.items():
        q &= Q(**{field: value})  # AND-combine dynamically
    return Article.objects.filter(q)


# Field lookup cheat-sheet:
#   __exact __iexact __contains __icontains __in __gt __gte __lt __lte
#   __startswith __endswith __range __date __year __isnull __regex