"""
Advanced ORM — Subquery, Exists, Raw SQL, Database Functions
"""

# from django.db.models import Subquery, OuterRef, Exists

# --- Subquery: latest review date per book ---
# latest_review = Review.objects.filter(
#     book=OuterRef("pk")
# ).order_by("-created_at").values("created_at")[:1]
#
# books = Book.objects.annotate(
#     latest_review_date=Subquery(latest_review)
# )

# --- Exists: books that have at least one 5-star review ---
# five_star = Review.objects.filter(book=OuterRef("pk"), rating=5)
# books = Book.objects.annotate(has_five_star=Exists(five_star)).filter(has_five_star=True)

# --- Database Functions ---
# from django.db.models.functions import Upper, Lower, Length, Coalesce, Now
# Book.objects.annotate(title_upper=Upper("title"))
# Book.objects.annotate(title_length=Length("title")).order_by("-title_length")
# Book.objects.annotate(desc=Coalesce("description", Value("No description")))

# --- Raw SQL ---
# books = Book.objects.raw("SELECT * FROM bookstore_book WHERE pages > %s", [300])

# --- values() and values_list() ---
# Book.objects.values("title", "author__last_name")
# titles = Book.objects.values_list("title", flat=True)

# --- Indexes for performance ---
# class Book(models.Model):
#     class Meta:
#         indexes = [
#             models.Index(fields=["title"]),
#             models.Index(fields=["-publication_date"]),
#             models.Index(fields=["status", "publication_date"]),
#         ]