"""
Basic ORM Query Examples — filter, exclude, order_by, get

Run: python manage.py shell
"""

# from bookstore.models import Book, Author, Category

# --- Filter (WHERE clause) ---
# Book.objects.filter(status="published")
# Book.objects.filter(title__icontains="django")
# Book.objects.filter(pages__gt=300)
# Book.objects.filter(pages__range=(200, 500))
# Book.objects.filter(publication_date__year=2026)
# Book.objects.filter(author__last_name="Müller")

# --- Exclude (NOT) ---
# Book.objects.exclude(status="draft")

# --- Get (single object) ---
# Book.objects.get(pk=1)             # raises DoesNotExist or MultipleObjectsReturned
# Book.objects.get(isbn="9783161484100")

# --- Order By ---
# Book.objects.order_by("title")     # ASC
# Book.objects.order_by("-title")    # DESC
# Book.objects.order_by("author__last_name", "title")

# --- Slicing (LIMIT/OFFSET) ---
# Book.objects.all()[:5]             # LIMIT 5
# Book.objects.all()[5:10]           # OFFSET 5 LIMIT 5

# --- Chaining ---
# Book.objects.filter(status="published").exclude(pages__lt=100).order_by("-publication_date")[:10]

# --- Existence/Count ---
# Book.objects.filter(status="published").exists()  # True/False
# Book.objects.filter(status="published").count()   # int