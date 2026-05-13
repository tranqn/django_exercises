"""
Query Optimization — Preventing N+1 queries.
"""

# BAD — N+1 queries
# books = Book.objects.all()          # 1 query
# for book in books:
#     print(book.author.name)          # N queries (one per book!)

# GOOD — select_related (SQL JOIN, for FK/O2O)
# books = Book.objects.select_related("author", "publisher").all()  # 1 query
# for book in books:
#     print(book.author.name)          # No additional query!

# GOOD — prefetch_related (separate query, for M2M/reverse FK)
# books = Book.objects.prefetch_related("categories", "reviews").all()  # 3 queries
# for book in books:
#     print(book.categories.all())     # Already prefetched!

# Custom Prefetch with filtering
# from django.db.models import Prefetch
# books = Book.objects.prefetch_related(
#     Prefetch("reviews", queryset=Review.objects.filter(rating__gte=4), to_attr="top_reviews")
# )

# only() / defer() — Load specific fields
# books = Book.objects.only("title", "author")  # Only load these fields
# books = Book.objects.defer("description")      # Load all except description

# Bulk operations
# books = [Book(title=f"Book {i}", pages=100) for i in range(1000)]
# Book.objects.bulk_create(books, batch_size=100)