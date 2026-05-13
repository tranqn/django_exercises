"""
Aggregation — Compute values across entire QuerySet.

from django.db.models import Count, Avg, Sum, Max, Min
"""

# Single aggregate values (returns dict)
# Book.objects.aggregate(
#     total=Count("id"),
#     avg_pages=Avg("pages"),
#     total_pages=Sum("pages"),
#     max_price=Max("price"),
#     min_price=Min("price"),
# )
# → {"total": 42, "avg_pages": 350.5, "total_pages": 14721, ...}

# Conditional aggregation
# from django.db.models import Q
# Book.objects.aggregate(
#     published_count=Count("id", filter=Q(status="published")),
#     draft_count=Count("id", filter=Q(status="draft")),
# )

# Aggregate on related models
# Author.objects.aggregate(
#     total_books=Count("books"),
#     avg_book_pages=Avg("books__pages"),
# )