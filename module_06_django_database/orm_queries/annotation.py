"""
Annotation — Add computed columns to each object in QuerySet.

from django.db.models import Count, Avg, F, Value
"""

# Add review count to each book
# books = Book.objects.annotate(review_count=Count("reviews"))
# for book in books:
#     print(f"{book.title}: {book.review_count} reviews")

# Add average rating
# books = Book.objects.annotate(avg_rating=Avg("reviews__rating"))

# Top authors by book count
# authors = Author.objects.annotate(
#     book_count=Count("books")
# ).order_by("-book_count")

# Annotate with conditional values
# from django.db.models import Case, When, CharField
# books = Book.objects.annotate(
#     price_tier=Case(
#         When(price__lt=10, then=Value("Budget")),
#         When(price__lt=30, then=Value("Standard")),
#         default=Value("Premium"),
#         output_field=CharField(),
#     )
# )

# Filter on annotations
# popular_authors = Author.objects.annotate(
#     book_count=Count("books")
# ).filter(book_count__gte=5)