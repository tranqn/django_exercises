"""
Q Objects — Complex Queries with OR, AND, NOT

from django.db.models import Q
"""

# OR: published OR 500+ pages
# Book.objects.filter(Q(status="published") | Q(pages__gte=500))

# AND: published AND 300+ pages
# Book.objects.filter(Q(status="published") & Q(pages__gte=300))

# NOT: not draft
# Book.objects.filter(~Q(status="draft"))

# Complex: (published OR archived) AND pages > 200
# Book.objects.filter(
#     (Q(status="published") | Q(status="archived")) & Q(pages__gt=200)
# )

# Dynamic Q objects (build query from user input)
def build_search_query(search_term, status=None, min_pages=None):
    """Build dynamic Q query from parameters."""
    query = Q(title__icontains=search_term) | Q(description__icontains=search_term)

    if status:
        query &= Q(status=status)
    if min_pages:
        query &= Q(pages__gte=min_pages)

    return query
    # Usage: Book.objects.filter(build_search_query("django", status="published"))